import matplotlib.pyplot as plt
from server.conSQL import puxa_relatorio_mensal_user, puxa_relatorio_mensal


def graph_linha_temporal_estoque(typ: str, key: str, ax, nome, cor, bkg):
    stock_geral = False
    sem_estoque = False
    # -- Seleciona produto --
    if nome == 'all':
        stock_geral = True
        name_sql = 'all'
    else:
        if nome == 'milho':
            name_sql = 'T_MILHO'
        elif nome == 'cafe':
            name_sql = 'T_CAFE'
        elif nome == 'soja':
            name_sql = 'T_SOJA'
        elif nome == 'tomate':
            name_sql = 'T_TOMATE'
        else:
            raise ValueError('Verifique o nome de prod em graph_linha_temporal_estoque')

        # -- Tipo de Estoque Geral/Simples --
    if typ == 'user':
        df = puxa_relatorio_mensal_user(key, name_sql, stock_geral)
    elif typ == 'id':
        df = puxa_relatorio_mensal(key, name_sql, stock_geral)
    else:
        raise ValueError('Olhe os parametros da função graph_linha_temporal_estoque')
    if stock_geral:
        a, b = df.axes
        for column in b:
            if str(column) == 'USER_DOC' or str(column) == 'MES':
                pass
            else:
                from client.Tools import escolhe_cor
                cor = escolhe_cor(str(column))
                x = df[['MES', column]].groupby('MES').sum()
                try:
                    graph = x.plot(kind='line', ax=ax, color=cor, marker='o', fontsize=15, legend=True)
                    graph.legend(facecolor=bkg, frameon=False, labelcolor='#FFFFFF', fontsize=15)
                except:
                    sem_estoque = True

    else:
        df = df[['MES', name_sql]].groupby('MES').sum()
        graph = df.plot(kind='line', ax=ax, color=cor, marker='o', fontsize=15, legend=True)
        graph.legend(facecolor=bkg, frameon=False, labelcolor='#FFFFFF', fontsize=15)

    # -- Pega valor max --
    x = df.max()
    max = 0
    for v in x:
        if type(v) == str:
            pass
        else:
            if v >= max:
                max = v
    return max