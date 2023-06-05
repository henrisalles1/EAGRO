from Register.User import User
from conSQL import insert_property, cursor
from Register.Property import Property


nome = 'henrique'
sobrenome = 'salles'
doc = '079.495.743-99'
email = 'henrique.aguiar.salles@gmail.com'
senha = 'Luckynick079.49'
telefone = '+55(48)99140-1331'

# user = User(doc, nome, sobrenome, email, senha, telefone)


nome_property = 'Casa do Henrique'
user_doc = '07949574399'
cep = '88701050'
numero = '226'
complemento = 'Edificio Luciane'


prop = Property(nome_property, user_doc, cep, numero, complemento)
