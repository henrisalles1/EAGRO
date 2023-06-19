from server.Register.Doc import valida_doc
from server.Register.Property import Property
from server.Tools import f_nome, f_email, f_senha, f_telefone, format_telefone
from server.conSQL import insert_user, cursor, puxa_propertys_id


class User:
    def __init__(self, doc: str, email: str, senha: str, telefone: str, exists: bool, nome: str, sobrenome=None):
        # -- Verifica dados --
        self.__doc, self.__tipo_pessoa, validated = valida_doc(doc)
        if not validated:
            raise ValueError('Documento com erro ou inválido !')
        nome, validated1 = f_nome(nome)
        if sobrenome:
            sobrenome, validated2 = f_nome(sobrenome)
        else:
            sobrenome = ''
            validated2 = True
        if not validated1 or not validated2:
            raise ValueError('O Nome deve conter apenas letras !')
        self.__nome = f'{nome} {sobrenome}'
        self.__email, validated = f_email(email)
        if not validated:
            raise ValueError('Email incorreto !')
        self.__senha, stat = f_senha(senha)
        if stat == 'upper':
            raise ValueError('A senha deve conter ao menos uma letra maiúscula !')
        elif stat == 'number':
            raise ValueError('A senha deve conter ao menos um numero !')
        elif stat == 'special':
            raise ValueError('A senha deve conter ao menos um caracter especial !')
        elif stat == 'limit':
            raise ValueError('A senha deve ter entre 8 a 30 caracteres !')
        else:
            pass
        telefone, validated = f_telefone(telefone)
        if validated:
            self.__telefone = format_telefone(telefone)
        else:
            raise ValueError('Telefone Inválido !')

        # -- Registra --
        if not exists:
            insert_user(self.__doc, self.__nome, self.__email, self.__senha, self.__telefone, self.__tipo_pessoa)
            cursor.commit()

        # -- Puxa Info --
        self.at_lista_propertys()

    def use_property(self, property: Property):
        self.__property = property

    @property
    def doc(self):
        return self.__doc

    def at_lista_propertys(self) -> None:
        self.__lista_propertys = puxa_propertys_id(user_doc=self.__doc)

    @property
    def get_propertys(self) -> list:
        self.at_lista_propertys()
        return self.__lista_propertys


    @property
    def tem_property(self) -> bool:
        self.at_lista_propertys()
        if len(self.__lista_propertys) != 0:
            return True
        else:
            return False

    @property
    def nome(self) -> str:
        return self.__nome

