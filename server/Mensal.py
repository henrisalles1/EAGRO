from datetime import datetime
from server.main import E_AGRO
from server.conSQL import relatorio_mensal, cursor


def mensal():
    hoje = datetime.now()
    hora = hoje.hour
    minutos = hoje.minute
    dia = hoje.day
    mes = str(hoje.month)
    ano = str(hoje.year)
    if len(mes) == 1:
        mes = f'0{mes}'
    mes_ano = f'{mes}/{ano[2:]}'
    if hora == 0 and minutos == 0 and dia == 1:
        relatorio_mensal(mes_ano, 'all')


def forca_mensal(id):
    hoje = datetime.now()
    mes = str(hoje.month)
    ano = str(hoje.year)
    if len(mes) == 1:
        mes = f'0{mes}'
    mes_ano = f'{mes}/{ano[2:]}'
    relatorio_mensal(mes_ano, id)

