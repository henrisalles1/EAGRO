from Register.Doc import valida_doc
from Tools import f_nome, f_email, f_senha, f_telefone, format_telefone
from conSQL import insert_user, cursor


class User:
    def __init__(self, doc: str, nome: str, sobrenome: str, email: str, senha: str, telefone: str):
        self.__doc, self.__tipo_pessoa = valida_doc(doc)
        nome = f_nome(nome)
        sobrenome = f_nome(sobrenome)
        self.__nome = f'{nome} {sobrenome}'
        self.__email = f_email(email)
        self.__senha = f_senha(senha)
        self.__telefone = format_telefone(f_telefone(telefone))
        insert_user(self.__doc, self.__nome, self.__email, self.__senha, self.__telefone, self.__tipo_pessoa)
        cursor.commit()

    @property
    def get_doc(self):
        return self.__doc



