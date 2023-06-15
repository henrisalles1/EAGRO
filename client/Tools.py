import shutil, tempfile
import matplotlib.pyplot as plt


def incluir_linha(nome_arquivo, numero_linha, conteudo):
    with open(nome_arquivo) as orig, tempfile.NamedTemporaryFile('w', delete=False) as out:
        for i, line in enumerate(orig):
            if i == numero_linha - 1:
                out.write(f'{conteudo}\n')
            out.write(line)

    shutil.move(out.name, nome_arquivo)


def ler_linha(nome_arquivo, numero_linha) -> str:
    file = open(nome_arquivo)
    conteudo = file.readlines()
    conteudo_limpo = []
    for string in conteudo:
        string = string.rstrip()
        conteudo_limpo.append(string)
    return conteudo_limpo[numero_linha]


def escolhe_cor(p: str) -> str:
    if p.lower().find('milho') != -1:
        return '#FFFF00'
    elif p.lower().find('cafe') != -1:
        return '#643843'
    elif p.lower().find('tomate') != -1:
        return '#CD1818'
    elif p.lower().find('soja') != -1:
        return '#F7F5EB'