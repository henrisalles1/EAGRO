from customtkinter import *
from server.conSQL import puxa_senha_sql, puxa_doc_user
from client.Tools import incluir_linha, ler_linha
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# -- Colors
bkg = '#323232'
#bkg = '#FFFFFF'
c1 = '#2EAC6D'
c2 = '#6DB193'
c3 = '#295F4E'
red = '#E01A00'


class App:
    def __init__(self):
        email, senha, ja_logado = self.acha_login()
        self.window = CTk()
        self.window.config(background=bkg)
        self.window.title('X')
        if ja_logado:
            self.w_menu_principal(email, senha, False)
        else:
            self.w_inicio()

    # ---- Inicio ----
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
        self.limpa_tela_inicio('tb<')
        self.w_inicio()

    # ---- Login -----
    def w_login(self):
        self.limpa_tela_inicio('b')
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

    # ---- Register ----
    def w_register(self):
        self.limpa_tela_inicio('b')
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

    # ---- Menu Principal ----
    def w_menu_principal(self, email: str, senha: str, app_already_open: bool):
        self.user_doc = puxa_doc_user(email, senha)
        if app_already_open:
            self.limpa_tela_inicio('tb<')
        self.window.geometry('1200x700')
        # -- frame --
        frame_top_l = CTkFrame(self.window)
        frame_top_m = CTkFrame(self.window)
        frame_top_r = CTkFrame(self.window)
        frame_bottom = CTkFrame(self.window)

        self.lista_frames = [frame_top_l, frame_top_m, frame_top_r, frame_bottom]

        # ------- GRAFICO -------
        def grafico_estoque(nome, cor, grafico):
            if grafico:
                grafico.destroy()
            from server.graphs import graph_linha_temporal_estoque
            figura = plt.Figure(figsize=(16, 8), dpi=60, facecolor=bkg, tight_layout=True)
            ax = figura.add_subplot(111)
            ax.set_facecolor(bkg)
            canva = FigureCanvasTkAgg(figura, frame_top_l)
            canva = canva.get_tk_widget()
            max = graph_linha_temporal_estoque(typ='user', key=self.user_doc, ax=ax, nome=nome, cor=cor, bkg=bkg)
            max += max*0.2
            ax.set_ylim([0, max])
            canva.grid(row=0, column=0, sticky='news')
            return canva

        grafico = grafico_estoque('all', 'x', None)
        # -----------------------

        # ----- Frame_top_M -----

        def botao_alimento(nome: str, cor: str, command) -> CTkButton:
            return CTkButton(frame_top_m, text=nome,
                             command=command,
                             bg_color=bkg, fg_color=bkg, hover_color=c2, text_color=cor,
                             border_width=2, border_color=c1,
                             width=150, height=40)

        todos_prod = botao_alimento('Todos', '#FFFFFF', command=lambda: grafico_estoque('all', 'x', grafico))
        milho = botao_alimento('Milho', '#FFFF00', command=lambda: grafico_estoque('milho', '#FFFF00', grafico))
        cafe = botao_alimento('Café', '#643843', command=lambda: grafico_estoque('cafe', '#643843', grafico))
        tomate = botao_alimento('Tomate', '#CD1818', command=lambda: grafico_estoque('tomate', '#CD1818', grafico))
        soja = botao_alimento('Soja', '#F7F5EB', command=lambda: grafico_estoque('soja', '#F7F5EB', grafico))

        # --- grid ---
        frame_top_l.grid(row=0, column=0, sticky='news')
        frame_top_m.grid(row=0, column=1, sticky='news')
        frame_top_r.grid(row=0, column=2, sticky='news')
        frame_bottom.grid(row=1, column=0, columnspan=3, sticky='news')

        # - frame_top_l -

        # - frame_top_m -
        todos_prod.grid(row=0, column=0, sticky='news', pady=2)
        milho.grid(row=1, column=0, sticky='news', pady=2)
        cafe.grid(row=2, column=0, sticky='news', pady=2)
        tomate.grid(row=3, column=0, sticky='news', pady=2)
        soja.grid(row=4, column=0, sticky='news', pady=2)

        # - frame_top_r -

        # - frame_bottom

        self.window.mainloop()


    # ---- Tools ----
    def limpa_tela_inicio(self, typ: str):
        for x in typ:
            if x == 't':
                self.frame_top.destroy()
            elif x == 'b':
                self.frame_bottom.destroy()
            elif x == '<':
                self.button_voltar.destroy()

    def limpa_tela(self):
        for frame in self.lista_frames:
            frame.destroy()
        self.lista_frames = []



app2 = App()
app2.w_inicio()