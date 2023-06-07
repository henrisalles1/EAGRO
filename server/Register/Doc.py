import re
from server.Tools import digitos_iguais


def valida_doc(doc: str):
    doc = limpa_doc(doc)
    if len(doc) == 11:
        tipo_pessoa = 'PF'
        if cpf_valido(doc):
            return doc, tipo_pessoa, True
        else:
            return None, None, False
    elif len(doc) == 14:
        tipo_pessoa = 'PJ'
        if cnpj_valido(doc):
            return doc, tipo_pessoa, True
        else:
            return None, None, False
    else:
        return None, None, False


def limpa_doc(doc):
    doc = re.sub('[-./]','', doc)
    return doc


# --------------- CPF ---------------
def cpf_valido(cpf) -> bool:
    if valida_p_soma_cpf(cpf):
        if valida_primeiro_digito_cpf(cpf):
            if valida_segundo_digito_cpf(cpf):
                if digitos_iguais(cpf):
                    return False
                else:
                    return True


def valida_p_soma_cpf(cpf):
    soma_digitos = 0
    for x in range(0, len(cpf)):
        soma_digitos += int(cpf[x])
    soma_digitos = str(soma_digitos)
    digito_1 = soma_digitos[0]
    digito_2 = soma_digitos[1]
    if digito_1 == digito_2:
        return True
    else:
        return False


def valida_primeiro_digito_cpf(cpf):
    if digitos_validadores_cpf(9, 10, cpf):
        return True
    else:
        return False


def valida_segundo_digito_cpf(cpf):
    if digitos_validadores_cpf(10, 11, cpf):
        return True
    else:
        return False


def digitos_validadores_cpf(index_digito: int, multiplicador_inicial: int, cpf):
    digito_verificador: str = cpf[index_digito]
    soma_digitos: int = 0
    multiplicador: int = multiplicador_inicial
    lista_digitos: list = []
    if multiplicador == 11:
        limite = 10
    elif multiplicador == 10:
        limite = 9
    else:
        raise ValueError('Erro em função digitos_validadores')
    for x in range(0, limite):
        digito = int(cpf[x])
        digito_multiplicado = digito * multiplicador
        multiplicador -= 1
        lista_digitos.append(digito_multiplicado)
    for digito_multiplicado in lista_digitos:
        soma_digitos += digito_multiplicado
    result = str((soma_digitos * 10) % 11)
    if digito_verificador == result:
        return True
    else:
        return False


# --------------- CNPJ ---------------
def cnpj_valido(cnpj):
    if primeiro_digito_cnpj(cnpj):
        if segundo_digito_cnpj(cnpj):
            if digitos_iguais(cnpj):
                return False
            else:
                return True


def primeiro_digito_cnpj(cnpj):
    if digito_verificador_cnpj(int(cnpj[12]), 12, 4, 5, cnpj):
        return True
    else:
        return False


def segundo_digito_cnpj(cnpj):
    if digito_verificador_cnpj(int(cnpj[13]), 13, 5, 6, cnpj):
        return True
    else:
        return False


def digito_verificador_cnpj(digito: int, limite1: int, limite2: int, m1: int, cnpj: str):
    digitos = []
    soma_digitos: int = 0
    for x in range(0, limite1):
        digitos.append(int(cnpj[x]))
    for x in range(0, limite2):
        digitos[x] *= m1
        m1 -= 1
    m2 = 9
    for x in range(limite2, len(digitos)):
        digitos[x] *= m2
        m2 -= 1
    for x in range(0, len(digitos)):
        soma_digitos += digitos[x]
    resultado = soma_digitos % 11
    if resultado < 2:
        resultado = 0
    else:
        resultado = 11 - resultado
    if resultado == digito:
        return True
    else:
        return False

