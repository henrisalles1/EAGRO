import pyodbc
import pandas as pd

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
    x = pd.read_sql(f"""SELECT * FROM Users_ WHERE DOC = '{email}';""", conexao)
    try:
        if email == str(x['EMAIL'][0]):
            return True
        else:
            return False
    except KeyError:
        return False
