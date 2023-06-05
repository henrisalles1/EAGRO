import re


def digitos_iguais(x: str):
    d = []
    for i in range(len(x)):
        d.append(x[i])
        if len(set(d)) == 1:
            return False
        else:
            return True


def f_nome(x: str):
    if x.isalpha():
        x = x.title()
        return x
    else:
        raise ValueError('Aceitos nomes apenas compostos por letras')


def f_email(email: str):
    padrao = re.search(r'[a-zA-Z0-9_.-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}(.[\w]{2,4})?$', email)
    if padrao:
        return email
    else:
        raise ValueError('Email incorreto !')


def f_senha(s):
    if 8 <= len(s) <= 30:
        if s.islower():
            raise ValueError('A senha deve ter aomenos uma letra maiúscula !')
        elif not re.search('[0-9]', s):
            raise ValueError('A senha deve ter ao menos um número !')
        elif s.isalnum():
            raise ValueError('A senha deve ter ao menos um carcter especial !')
        else:
            return s
    else:
        raise ValueError('A senha deve ter entre 8 a 30 caracteres !')


def f_telefone(t):
    t = re.sub('[()+-]','', t)
    padrao_telefone = re.compile('([+][0-9]{2})?([(][0-9]{2}[)])|([0-9]{2})[0-9]{5}[-]?[0-9]{4}')
    if re.search(padrao_telefone, t):
        return t
    else:
        raise ValueError('Número de telefone incorreto !')


def format_telefone(t):
    if len(t) == 13:
        f = '+{}({}){}-{}'.format(
            t[:2],
            t[2:4],
            t[4:9],
            t[9:]
        )
        return f
    elif len(t) == 11:
        f = '({}){}-{}'.format(
            t[:2],
            t[2:7],
            t[7:]
        )
        return f
    else:
        raise ValueError('Telefone não se encontra aos padrões !')


def valida_cep(c):
    if len(c) == 8:
        if c.isnumeric():
            return c
        else:
            raise ValueError('CEP inválido !')
    else:
        raise ValueError('CEP inválido !')