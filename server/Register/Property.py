from server.Tools import valida_cep
from server.conSQL import insert_property, select_last_property_id, delete_property, cursor


def create_property_id():
    caracteres = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
                  'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                  'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    d = []
    z = []
    ultimo_id = select_last_property_id()
    if not ultimo_id:
        return '00000000'
    for x in ultimo_id[::-1]:
        d.append(caracteres.index(x))
    for x in range(len(d)):
        i = 0
        c = d[x]
        if c < 35:
            c += 1
            i += 1
            z.append(c)
            break
        else:
            c = 0
            z.append(c)
    for x in range(len(z)):
        d[x] = z[x]
    i = 0
    for x in d:
        d[i] = caracteres[x]
        i += 1
    new_id = ''.join(d)
    new_id = new_id[::-1]
    return new_id


class Property:
    def __init__(self, nome: str, user_doc: str, cep: str, numero: str, complemento: str, exists: bool):
        self.__nome = nome.title()
        self.__user_doc = user_doc
        self.__cep = valida_cep(cep)
        self.__id = create_property_id()
        if not exists:
            insert_property(self.__id, self.__nome, self.__user_doc, self.__cep, numero, complemento)
            cursor.commit()

    def delete_this_property(self):
        delete_property(self.__id)
