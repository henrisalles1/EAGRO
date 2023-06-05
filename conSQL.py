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


def select_last_property_id():
    x = pd.read_sql('''SELECT TOP(1) ID FROM Propertys_ ORDER BY ID DESC;''', conexao)
    y = x['ID']
    id = y.get(0)
    return id


def delete_property(id):
    command = f"""DELETE FROM Propertys_ WHERE ID = '{id}';"""
    cursor.execute(command)

