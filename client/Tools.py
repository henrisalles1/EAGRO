import shutil, tempfile


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
    return conteudo[numero_linha]
