import pyodbc
import pandas as pd

# -------- ATENÇÃO --------
# Nenhuma das funçoes ultiliza o cursor.commit()
# Você mesmo deve importar o cursor e fazer o commit após a função se necessario !

dados_conexao = (
    'Driver={SQL Server};'
    'Server=RedNitro;'
    'Database=E_AGRO;'
)

conexao = pyodbc.connect(dados_conexao)

cursor = conexao.cursor()


def insert_user(doc: str, nome: str, email: str, password: str, telefone: str, tipo_pessoa: str):
    command = f"""INSERT INTO Users_(DOC, NOME, EMAIL, PASSWORD, TELEFONE, TIPO_PESSOA)
    VALUES ('{doc}','{nome}','{email}','{password}','{telefone}','{tipo_pessoa}');"""
    cursor.execute(command)


def insert_property(id: str, nome_prop: str, user_doc: str, cep: str, numero: str, complemento: str):
    command = f"""INSERT INTO Propertys_(ID, NOME, USER_DOC, CEP, NUMERO, COMPLEMENTO)
    VALUES ('{id}','{nome_prop}','{user_doc}','{cep}','{numero}','{complemento}');"""
    cursor.execute(command)


def select_last_property_id() -> str:
    x = pd.read_sql('''SELECT TOP(1) ID FROM Propertys_ ORDER BY ID DESC;''', conexao)
    y = x['ID']
    id = y.get(0)
    return id


def delete_property(id):
    command = f"""DELETE FROM Propertys_ WHERE ID = '{id}';"""
    cursor.execute(command)


def puxa_senha_sql(email: str) -> str:
    email = email.lower()
    try:
        x = pd.read_sql(f"""SELECT * FROM Users_ WHERE EMAIL = '{email}';""", conexao)
    except Exception:
        return 'emailincorreto'
    senha_sql = str(x['PASSWORD'][0])
    return senha_sql


def doc_ja_cadastrado(doc: str) -> bool:
    x = pd.read_sql(f"""SELECT * FROM Users_ WHERE DOC = '{doc}';""", conexao)
    try:
        if doc == str(x['DOC'][0]):
            return True
        else:
            return False
    except KeyError:
        return False


def email_ja_cadastrado(email: str) -> bool:
    x = pd.read_sql(f"""SELECT * FROM Users_ WHERE EMAIL = '{email}';""", conexao)
    try:
        if email == str(x['EMAIL'][0]):
            return True
        else:
            return False
    except KeyError:
        return False


def relatorio_mensal(mes_ano: str, id: str):
    if id != 'all':
        command = f"""INSERT INTO Relatorios_mensais (ID, MES, T_MILHO, T_CAFE)
        SELECT Propertys_.ID, '{mes_ano}', Propertys_.T_MILHO, Propertys_.T_CAFE
        FROM Propertys_ WHERE ID = '{id}';"""
        cursor.execute(command)
    else:
        df = pd.read_sql(f"""SELECT ID FROM Propertys_""", conexao)
        for index, line in df.iterrows():
            ids = [line.ID]
            for id in ids:
                print(id)
                command = f"""INSERT INTO Relatorios_mensais (ID, MES, T_MILHO, T_CAFE)
                SELECT Propertys_.ID, '{mes_ano}', Propertys_.T_MILHO, Propertys_.T_CAFE
                FROM Propertys_ WHERE ID = '{id}';"""
                cursor.execute(command)


def puxa_relatorio_mensal(id: str, prod: str, geral: bool) -> list:
    relatorio = []
    if geral:
        x = pd.read_sql(f"""SELECT * FROM Relatorios_mensais WHERE ID = '{id}';""", conexao)
        for i in range(len(x)):
            y = i + 2
            mes = []
            mes_ano = x[2][i]
            prod = x[y][i]
            mes.append(mes_ano)
            mes.append(prod)
            relatorio.append(mes)

    x = pd.read_sql(f"""SELECT MES, {prod} FROM Relatorios_mensais WHERE ID = '{id}';""", conexao)

    for i in range(len(x)):
        mes = []
        mes_ano = x.MES[i]
        prod = x[f"'{prod}'"][i]
        mes.append(mes_ano)
        mes.append(prod)
        relatorio.append(mes)
    return relatorio


def puxa_doc_user(email: str, senha: str):
    email = email.lower()
    x = pd.read_sql(f"""SELECT * FROM Users_ WHERE EMAIL = '{email}' AND PASSWORD = '{senha}';""", conexao)
    return x['DOC'][0]


def puxa_propertys(user_doc: str) -> list:
    x = pd.read_sql(f"""SELECT ID FROM Propertys_ WHERE USER_DOC = '{user_doc}';""", conexao)
    return list(x['ID'])


def puxa_relatorio_mensal_user(user_doc: str, prod: str, geral: bool) -> iter:
    if geral:
        x = pd.read_sql(f"""SELECT * FROM Relatorios_mensais""", conexao)
        a, b = x.axes

        string = ''
        for column in b:
            if str(column) == 'ID' or str(column) == 'MES':
                pass
            else:
                string = f'{string}SUM(R.{column}) AS {column}, '
        string = string.removesuffix(', ')

        x = pd.read_sql(f"""SELECT P.USER_DOC AS USER_DOC, R.MES AS MES, {string}
                            FROM Relatorios_mensais AS R
                            INNER JOIN Propertys_ AS P ON R.ID = P.ID
                            WHERE P.USER_DOC = {user_doc}
                            GROUP BY P.USER_DOC, R.MES; """, conexao)
    else:
        x = pd.read_sql(f"""SELECT P.USER_DOC AS USER_DOC, R.MES AS MES, SUM(R.{prod}) AS {prod}
                        FROM Relatorios_mensais AS R
                        INNER JOIN Propertys_ AS P ON R.ID = P.ID
                        WHERE P.USER_DOC = {user_doc}
                        GROUP BY P.USER_DOC, R.MES;""", conexao)
    return x
