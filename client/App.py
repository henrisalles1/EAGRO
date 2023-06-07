from customtkinter import *
from server.conSQL import puxa_senha_sql
from client.Tools import incluir_linha, ler_linha


# -- Colors
bkg = '#323232'
c1 = '#2EAC6D'
c2 = '#6DB193'
c3 = '#295F4E'
red = '#E01A00'


class App:
    def __init__(self):
        email, senha, ja_logado = self.acha_login()
        self.window = CTk()
        self.window.title('E-Agro')
        if ja_logado:
            self.w_menu_principal(email, senha, False)
        else:
            self.w_inicio()

    def acha_login(self) -> (str, str, bool):
        try:
            email = ler_linha('data.txt', 0)
            senha = ler_linha('data.txt', 1)
            ja_logado = ler_linha('data.txt', 2)
            if ja_logado == 'True':
                return email, senha, ja_logado
            else:
                return None, None, False
        except:
            return None, None, False


    def w_inicio(self):
        self.window.geometry('600x650')
        # -- frame --
        self.frame_top = CTkFrame(self.window)
        self.frame_bottom = CTkFrame(self.window)

        # -- txt --
        txt_e_agro = CTkLabel(self.frame_top, text='E-AGRO',
                              font=('Arial', 50),
                              text_color=c1)
        texto_orientacao = CTkLabel(self.frame_top, text='Bem vindo !',
                                    font=('Arial', 14),
                                    text_color=c2)
        go_to_login = CTkButton(self.frame_bottom, text='Login', command=lambda: self.w_login(),
                                font=('Arial', 13),
                                border_color=c1, text_color=c1, fg_color=bkg, hover_color=c3,
                                border_width=2, width=310, height=38)
        register = CTkButton(self.frame_bottom, text='Registre-se', command=lambda: self.w_register(),
                             font=('Arial', 13),
                             border_color=c1, text_color=c1, fg_color=bkg, hover_color=c3,
                             border_width=2, width=310, height=38)

        # -- grid --
        txt_e_agro.grid(column=0, row=0)
        texto_orientacao.grid(column=0, row=1)
        go_to_login.grid(column=0, row=2, sticky='news')
        register.grid(column=0, row=3, pady=20, sticky='news')

        # -- flexgrid --
        # - row -
        self.window.grid_rowconfigure(0, weight=3)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)

        # - column -
        self.window.grid_columnconfigure(0, weight=1000)

        self.frame_top.grid(row=0)
        self.frame_bottom.grid(row=1)

        self.window.mainloop()

    def volta_inicio(self):
        self.limpa_tela('tb<')
        self.w_inicio()

    def w_login(self):
        self.limpa_tela('b')
        self.window.geometry('600x650')
        # -- frame --
        self.frame_bottom = CTkFrame(self.window)

        # -- txt --
        entry_email = CTkEntry(self.frame_bottom, placeholder_text='Insira seu email...',
                                    text_color=c1,
                                    width=320, height=50)
        entry_senha = CTkEntry(self.frame_bottom, placeholder_text='Insira sua senha...', show='*',
                                    text_color=c1,
                                    width=320, height=50)
        lembrar = CTkCheckBox(self.frame_bottom, text='Lembrar login',
                              fg_color=c3)

        login = CTkButton(self.frame_bottom, text='Login', command=lambda: self.tenta_login(entry_email, entry_senha, lembrar),
                          text_color=c1, bg_color=bkg, fg_color=bkg,
                          border_width=2, border_color=c1,
                          width=320, height=40
                          )
        self.button_voltar = CTkButton(self.window, text='<',
                                  command=lambda: self.volta_inicio(),
                                  bg_color=bkg, fg_color=bkg, hover_color=bkg, text_color=c2,
                                  border_spacing=0,
                                  width=20, height=20, font=('Arial', 20))

        # -- grid --
        entry_email.grid(column=0, row=0, sticky='news', pady=20)
        entry_senha.grid(column=0, row=1, sticky='news')
        lembrar.grid(column=0, row=2, pady=8)
        login.grid(column=0, row=3, sticky='news')
        self.button_voltar.place(x=50, y=50)

        self.frame_bottom.grid(column=0, row=1)

        self.window.mainloop()

    def tenta_login(self, email, senha, lembrar):
        email = email.get()
        senha = senha.get()
        try:
            if puxa_senha_sql(email) == senha:
                if lembrar.get():
                    self.lembrar_login(email.lower(), senha)
                self.w_menu_principal(email, senha, True)
        except:
            login_incorreto = CTkLabel(self.frame_top, text='Email ou Senha Incorretos !',
                                       text_color=red)
            login_incorreto.grid(column=0, row=2)
            self.window.mainloop()

    def lembrar_login(self, email, senha):
        incluir_linha('data.txt', 1, email)
        incluir_linha('data.txt', 2, senha)
        incluir_linha('data.txt', 3, 'True')


    def w_register(self):
        self.limpa_tela('b')
        self.window.geometry('600x650')

        # -- frames --
        self.frame_bottom = CTkFrame(self.window)

        # -- body --
        spacer = CTkLabel(self.frame_bottom, text='')

        entry_nome = CTkEntry(self.frame_bottom, placeholder_text='Nome',
                              text_color=c1,
                              width=150)
        entry_sobrenome = CTkEntry(self.frame_bottom, placeholder_text='Sobrenome',
                                   text_color=c1,
                                   width=150)
        entry_doc = CTkEntry(self.frame_bottom, placeholder_text='Documento CPF/CNPJ',
                             text_color=c1,
                             width=150)
        entry_telefone = CTkEntry(self.frame_bottom, placeholder_text='Telefone',
                                  text_color=c1,
                                  width=150)
        entry_email = CTkEntry(self.frame_bottom, placeholder_text='Email',
                               text_color=c1)
        entry_senha = CTkEntry(self.frame_bottom, placeholder_text='Senha',
                               text_color=c1, show='*')
        entry_confirma_senha = CTkEntry(self.frame_bottom, placeholder_text='Confirme sua Senha',
                                        text_color=c1, show='*')
        button_register = CTkButton(self.frame_bottom, text='Registre-se',
                                    command=lambda: self.tenta_register(entry_nome, entry_sobrenome, entry_doc, entry_telefone,
                                                                entry_email, entry_senha, entry_confirma_senha),
                                    bg_color=bkg, fg_color=bkg, text_color=c1,
                                    border_width=2, border_color=c1,
                                    width=320, height=40)

        self.button_voltar = CTkButton(self.window, text='<',
                                       command=lambda: self.volta_inicio(),
                                       bg_color=bkg, fg_color=bkg, hover_color=bkg, text_color=c2,
                                       border_spacing=0,
                                       width=20, height=20, font=('Arial', 20))

        # -- grid --
        spacer.grid(column=1, row=0, rowspan=2, padx=5)
        entry_nome.grid(column=0, row=0, sticky='news', pady=5)
        entry_sobrenome.grid(column=2, row=0, sticky='news', pady=5)
        entry_doc.grid(column=0, row=1, sticky='news', pady=5)
        entry_telefone.grid(column=2, row=1, sticky='news', pady=5)
        entry_email.grid(column=0, row=2, columnspan=3, sticky='news', pady=5)
        entry_senha.grid(column=0, row=3, columnspan=3, sticky='news', pady=5)
        entry_confirma_senha.grid(column=0, row=4, columnspan=3, sticky='news', pady=5)
        button_register.grid(column=0, row=5, columnspan=3, sticky='news', pady=5)
        self.button_voltar.place(x=50, y=50)

        self.frame_bottom.grid(column=0, row=1)

    def tenta_register(self, nome, sobrenome, doc, telefone, email, senha, confirma_senha):
        try:
            self.msg_erro.destroy()
        except:
            pass
        nome = nome.get()
        sobrenome = sobrenome.get()
        doc = doc.get()
        telefone = telefone.get()
        email = email.get()
        senha = senha.get()
        confirma_senha = confirma_senha.get()
        from server.Tools import f_nome
        nome, validated1 = f_nome(nome)
        sobrenome, validated2 = f_nome(sobrenome)
        if not validated1 or not validated2:
            self.msg_erro = CTkLabel(self.frame_top, text='O nome/sobrenome deve ser único e conter apenas letras !',
                                text_color=red)
            self.msg_erro.grid(column=0, row=2)
            raise ValueError('O nome/sobrenome deve ser único e conter apenas letras !')
        from server.Register.Doc import valida_doc
        doc, tipo_pessoa, validated = valida_doc(doc)
        if not validated:
            self.msg_erro = CTkLabel(self.frame_top, text='Documento com Erro ou Inválido',
                                text_color=red)
            self.msg_erro.grid(column=0, row=2)
            raise ValueError('Documento com Erro ou Inválido')

        # -- confere se já não esta cadastrado DOC
        from server.conSQL import doc_ja_cadastrado
        if doc_ja_cadastrado(doc):
            self.msg_erro = CTkLabel(self.frame_top, text='Documento já Cadastrado, tente o Login',
                                text_color=red)
            self.msg_erro.grid(column=0, row=2)
            raise ValueError('Documento já Cadastrado, tente o Login')

        from server.Tools import f_telefone
        telefone, validated = f_telefone(telefone)
        if not validated:
            self.msg_erro = CTkLabel(self.frame_top, text='Telefone Inválido, insira-o com seu DDD',
                                text_color=red)
            self.msg_erro.grid(column=0, row=2)
            raise ValueError('Telefone Inválido, insira-o com seu DDD')
        from server.Tools import f_email
        email, validated = f_email(email)
        if not validated:
            self.msg_erro = CTkLabel(self.frame_top, text='Email Inválido',
                                text_color=red)
            self.msg_erro.grid(column=0, row=2)
            raise ValueError('Email Inválido')

        # -- confere se já não esta cadastrado EMAIL
        from server.conSQL import email_ja_cadastrado
        if email_ja_cadastrado(email):
            self.msg_erro = CTkLabel(self.frame_top, text='Email já Cadastrado, tente o Login',
                                text_color=red)
            self.msg_erro.grid(column=0, row=2)
            raise ValueError('Email já Cadastrado, tente o Login')

        from server.Tools import f_senha
        senha, stat = f_senha(senha)
        if stat == 'upper':
            self.msg_erro = CTkLabel(self.frame_top, text='A senha deve conter ao menos uma letra maiúscula !',
                                text_color=red)
            self.msg_erro.grid(column=0, row=2)
            raise ValueError('A senha deve conter ao menos uma letra maiúscula !')
        elif stat == 'number':
            self.msg_erro = CTkLabel(self.frame_top, text='A senha deve conter ao menos um numero !',
                                text_color=red)
            self.msg_erro.grid(column=0, row=2)
            raise ValueError('A senha deve conter ao menos um numero !')
        elif stat == 'special':
            self.msg_erro = CTkLabel(self.frame_top, text='A senha deve conter ao menos um caracter especial !',
                                text_color=red)
            self.msg_erro.grid(column=0, row=2)
            raise ValueError('A senha deve conter ao menos um caracter especial !')
        elif stat == 'limit':
            self.msg_erro = CTkLabel(self.frame_top, text='A senha deve ter entre 8 a 30 caracteres !',
                                text_color=red)
            self.msg_erro.grid(column=0, row=2)
            raise ValueError('A senha deve ter entre 8 a 30 caracteres !')
        elif senha != confirma_senha:
            self.msg_erro = CTkLabel(self.frame_top, text='Os campos senha não possuem os mesmos valores !',
                                text_color=red)
            self.msg_erro.grid(column=0, row=2)
            raise ValueError('Os campos senha não possuem os mesmos valores !')
        from server.Register.User import User
        User(doc, nome, sobrenome, email, senha, telefone, False)
        self.msg_erro = CTkLabel(self.frame_top, text='Usuário Registrado, tente o Login !',
                            text_color=c1)
        self.msg_erro.grid(column=0, row=2)

    def w_menu_principal(self, email: str, senha: str, app_already_open: bool):
        if app_already_open:
            self.limpa_tela('tb<')
        self.window.geometry('1200x700')
        self.window.mainloop()
        # -- frame --
        self.frame_top_l = CTkFrame(self.window)
        self.frame_top_r = CTkFrame(self.window)
        self.frame_bottom_l = CTkFrame(self.window)
        self.frame_bottom_r = CTkFrame(self.window)

        # -- grid --

    def limpa_tela(self, typ: str):
        for x in typ:
            if x == 't':
                self.frame_top.destroy()
            elif x == 'b':
                self.frame_bottom.destroy()
            elif x == '<':
                self.button_voltar.destroy()


email = 'henrique.aguiar.salles@gmail.com'
senha = 'Luckynick079.49'
ja_logado = False

App()

