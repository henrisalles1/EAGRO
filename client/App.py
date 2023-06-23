from customtkinter import *
from server.conSQL import puxa_senha_sql, puxa_user, select_property, cursor
from client.Tools import incluir_linha, ler_linha
from server.Register.User import User
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# -- Colors
bkg = '#323232'
#bkg = '#FFFFFF'
c1 = '#2EAC6D'
c2 = '#6DB193'
c3 = '#295F4E'
red = '#E01A00'


# ---- CTkinter defaults ----
def ctk_botao(frame, text, command, bg_color=bkg, fg_color=bkg, text_color=c1, border_width=2, border_color=c1,
              hover_color=c3, height=40, width=320, font='Arial', tamanho_font=15):
    botao = CTkButton(frame, text=text,
                      command=command,
                      bg_color=bg_color, fg_color=fg_color, text_color=text_color,
                      border_width=border_width, border_color=border_color, hover_color=hover_color,
                      width=width, height=height, font=(font, tamanho_font)
                      )
    return botao


def ctk_botao_label(frame, text, command, bg_color=bkg, fg_color=bkg, hover_color=bkg, text_color=c1,
                    border_spacing=0, width=20, height=20, font='Arial', tamanho_font=20):
    botao = CTkButton(frame, text=text,
                      command=command,
                      bg_color=bg_color, fg_color=fg_color, hover_color=hover_color, text_color=text_color,
                      border_spacing=border_spacing,
                      width=width, height=height, font=(font, tamanho_font))
    return botao


def ctk_label(frame, text, bg_color=bkg, fg_color=bkg, text_color=c1, font='Arial', tamanho_fonte=15):
    label = CTkLabel(frame, text=text, bg_color=bg_color, fg_color=fg_color, text_color=text_color,
                     font=(font, tamanho_fonte))
    return label


def ctk_entry(frame, text, show=None, text_color=c1, width=320, height=50):
    entry = CTkEntry(frame, placeholder_text=text, show=show, text_color=text_color, width=width, height=height)
    return entry


def spacer(frame):
    spc = CTkLabel(frame, text='')
    return spc


def ctk_radio_button(frame, text, command, var=None, value=None, bg_color=bkg, fg_color=c1, text_color=c2,
                     font='Arial', tamanho_fonte=15):
    botao = CTkRadioButton(frame, text=text, command=command, variable=var, value=value, bg_color=bg_color, fg_color=fg_color,
                           text_color=text_color, font=(font, tamanho_fonte))
    return botao


def ctk_frame(frame, fg_color=bkg, width=None, height=None, border_width=2, border_color=c1):
    fr = CTkFrame(frame)
    fr.configure(fg_color=fg_color, border_width=border_width,
                 border_color=border_color)
    if width:
        fr.configure(width=width)
    if height:
        fr.configure(height=height)
    return fr


def ctk_textbox(frame, width=100, height=100, bg_color=bkg, fg_color=c1, border_color=c3, text_color=c2, scroll_color=c3,
                font='Arial', tamanho_fonte=12):
    textbox = CTkTextbox(frame, width=width, height=height,
                         bg_color=bg_color, fg_color=fg_color, border_color=border_color,
                         text_color=text_color, scrollbar_button_color=scroll_color,
                         font=(font, tamanho_fonte))
    return textbox


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
        self.frame_top = self.ctk_frame()
        self.frame_bottom = self.ctk_frame()

        # -- txt --
        txt_e_agro = ctk_label(self.frame_top, text='E-AGRO', tamanho_fonte=50)
        texto_orientacao = ctk_label(self.frame_top, text='Bem vindo !', text_color=c2, font=14)

        go_to_login = ctk_botao(self.frame_bottom, text='Login', command=lambda: self.w_login(), tamanho_font=13,
                                width=310, height=38)
        register = ctk_botao(self.frame_bottom, text='Registre-se', command=lambda: self.w_register(),
                             tamanho_font=13, width=310, height=38)

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
        self.frame_bottom = self.ctk_frame()

        # -- txt --
        entry_email = ctk_entry(self.frame_bottom, text='Insira seu email...')
        entry_senha = ctk_entry(self.frame_bottom, text='Insira sua senha...', show='*')
        lembrar = CTkCheckBox(self.frame_bottom, text='Lembrar login',
                              fg_color=c3)

        login = ctk_botao(self.frame_bottom, text='Login',
                          command=lambda: self.tenta_login(entry_email, entry_senha, lembrar))
        self.button_voltar = ctk_botao_label(self.window, text='<',
                                             command=lambda: self.volta_inicio())

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
        self.frame_bottom = self.ctk_frame(self.window)

        # -- body --
        spc = spacer(self.frame_bottom)

        w = 150
        h = 28
        entry_nome = ctk_entry(self.frame_bottom, text='Nome', width=w, height=h)
        entry_sobrenome = ctk_entry(self.frame_bottom, text='Sobrenome', width=w, height=h)
        entry_doc = ctk_entry(self.frame_bottom, text='Documento CPF/CNPJ', width=w, height=h)
        entry_telefone = ctk_entry(self.frame_bottom, text='Telefone', width=w, height=h)
        entry_email = ctk_entry(self.frame_bottom, text='Email', height=h)
        entry_senha = ctk_entry(self.frame_bottom, text='Senha', show='*', height=h)
        entry_confirma_senha = ctk_entry(self.frame_bottom, text='Confirme sua Senha', show='*', height=h)
        button_register = ctk_botao(self.frame_bottom, text='Registre-se',
                                    command=lambda: self.tenta_register(entry_nome, entry_sobrenome, entry_doc,
                                                                        entry_telefone, entry_email, entry_senha,
                                                                        entry_confirma_senha))

        self.button_voltar = ctk_botao_label(self.window, text='<',
                                             command=lambda: self.volta_inicio())

        # -- grid --
        spc.grid(column=1, row=0, rowspan=2, padx=5)
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
        self.__user = User(doc=doc, nome=nome, sobrenome=sobrenome, email=email, senha=senha, telefone=telefone, exists=False)
        self.msg_erro = CTkLabel(self.frame_top, text='Usuário Registrado, tente o Login !',
                                 text_color=c1)
        self.msg_erro.grid(column=0, row=2)

    # ---- Menu Principal ----

    def w_menu_principal(self, email=None, senha=None, veio_w_inicio=False):
        print('menu principal')
        # -- Puxa User --
        try:
            if self.__user:
                pass
        except:
            doc, nome, email, senha, telefone, tipo_pessoa = puxa_user(email, senha)
            nome = nome.split()[0]
            self.__user = User(doc=doc, nome=nome, email=email, senha=senha, telefone=telefone, exists=True)

        if veio_w_inicio:
            self.limpa_tela_inicio('tb<')
        self.window.geometry('1200x700')

        tem_property = self.__user.tem_property
        if not tem_property:
            self.w_menu_nao_tem_property()
        else:
            # -- frame --
            frame_top_l = CTkFrame(self.window)
            frame_top_m = CTkFrame(self.window)
            frame_top_r = CTkFrame(self.window)
            frame_bottom = CTkFrame(self.window)

            self.lista_frames = [frame_top_l, frame_top_m, frame_top_r, frame_bottom]
            for frame in self.lista_frames:
                frame.configure(fg_color=bkg)

            # ------- GRAFICO -------
            def grafico_estoque(nome, cor, grafico):
                if grafico:
                    grafico.destroy()
                from server.graphs import graph_linha_temporal_estoque
                figura = plt.Figure(figsize=(16, 8), dpi=60, facecolor=bkg, tight_layout=True)
                ax = figura.add_subplot(111)
                ax.set_facecolor(bkg)
                max = graph_linha_temporal_estoque(typ='user', key=self.__user.doc, ax=ax, nome=nome, cor=cor, bkg=bkg)
                if max == 0:
                    ax.text(0.4, 1, 'Sem Estoque', c=c1, fontsize=35)
                    max = 2
                else:
                    max += max*0.2
                ax.set_ylim([0, max])
                canva = FigureCanvasTkAgg(figura, frame_top_l)
                canva = canva.get_tk_widget()
                canva.grid(row=0, column=0, sticky='news')
                return canva

            grafico = grafico_estoque('all', 'x', None)
            if type(grafico) == CTkLabel:
                grafico.pack(expand=True, fill='both')
            else:
                grafico.grid()
            # -----------------------

            # ----- Frame_top_M -----

            def botao_alimento(nome: str, cor: str, command) -> CTkButton:
                return ctk_botao(frame_top_m, text=nome,
                                 command=command, text_color=cor,
                                 width=150, height=40)
            try:
                todos_prod = botao_alimento('Todos', '#FFFFFF',
                                            command=lambda: grafico_estoque('all', 'x', grafico))
                milho = botao_alimento('Milho', '#FFFF00',
                                       command=lambda: grafico_estoque('milho', '#FFFF00', grafico))
                cafe = botao_alimento('Café', '#643843',
                                      command=lambda: grafico_estoque('cafe', '#643843', grafico))
                tomate = botao_alimento('Tomate', '#CD1818',
                                        command=lambda: grafico_estoque('tomate', '#CD1818', grafico))
                soja = botao_alimento('Soja', '#F7F5EB',
                                      command=lambda: grafico_estoque('soja', '#F7F5EB', grafico))

                todos_prod.grid(row=0, column=0, sticky='news', pady=2)
                milho.grid(row=1, column=0, sticky='news', pady=2)
                cafe.grid(row=2, column=0, sticky='news', pady=2)
                tomate.grid(row=3, column=0, sticky='news', pady=2)
                soja.grid(row=4, column=0, sticky='news', pady=2)
            except:
                pass

            # --- grid ---
            frame_top_l.grid(row=0, column=0, sticky='news')
            frame_top_m.grid(row=0, column=1, sticky='news')
            frame_top_r.grid(row=0, column=2, sticky='news')
            frame_bottom.grid(row=1, column=0, columnspan=3, sticky='news')

            # ----- FRAME_BOTTOM -----
            estoque = ctk_botao(frame_bottom, 'Gerenciar estoque', command=lambda: self.w_ger_estoque())
            estoque.grid(row=0, column=0, sticky='news')

            self.window.mainloop()

    def w_menu_nao_tem_property(self):

        frame = self.ctk_frame()

        texto_central = ctk_label(frame, text='Você ainda não tem nenhuma propriedade cadastrada !', tamanho_fonte=20)
        texto_acao = ctk_label(frame, text='Cadastre-a agora mesmo')
        cadastrar_propriedade = ctk_botao(frame, text='Cadastrar Propriedade',
                                          command=lambda: self.w_cadastro_de_propriedade())
        spc = spacer(frame)
        # -- grid --
        frame.grid(row=0, column=0)
        texto_central.grid(row=0, column=0, sticky='news')
        texto_acao.grid(row=1, column=0, pady=2, sticky='news')
        spc.grid(row=2, column=0, pady=100)
        cadastrar_propriedade.grid(row=3, column=0, sticky='news')

        # -- flexgrid --
        self.window.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=2)
        frame.grid_columnconfigure(0, weight=1)

        self.window.grid_columnconfigure(0, weight=1)

        self.lista_frames = [frame]

        self.window.mainloop()

    def volta_menu_principal(self):
        self.limpa_tela()
        self.w_menu_principal()

    # ---- Janelas de manipulação de dados ----

    def w_ger_estoque(self):
        w_ger_estoque = CTk()
        w_ger_estoque.config(background=bkg)
        w_ger_estoque.title('Gerenciar Estoque')
        w_ger_estoque.geometry('800x600')

        frame = ctk_frame(w_ger_estoque)

        frame_l = ctk_frame(frame)
        frame_top_m = ctk_frame(frame)
        frame_top_r = ctk_frame(frame)
        frame_top_r.grid_rowconfigure('all', weight=1)
        frame_top_r.grid_columnconfigure('all', weight=1)
        frame_bottom = ctk_frame(frame)

        def command_radio_property(id: str):
            def command_add_prod(lista_prod, mini_frame_stock):
                def cria_button_predef_prod(lista_pre_def):
                    def add_prod(nome):
                        def finaliza_add_prod(nome, entry_stock):
                            value = entry_stock.get()
                            from server.conSQL import alter_propertys
                            alter_propertys(id=id, type_prod=nome, value_prod=value)
                            cursor.commit()
                            mini_frame = limpa_mini_frame(frame)
                            txt_confirmacao = ctk_label(mini_frame, f'Inseridos {value}t de {nome}')
                            txt_confirmacao.grid(row=0, column=0, sticky='news')

                        frame = limpa_mini_frame(mini_frame_stock)
                        txt = ctk_label(frame, f'Insira uma quantidade em Toneladas\n'
                                               f'   do seu estoque para {nome}')
                        txt.grid(row=0, column=0, pady=2, columnspan=2)
                        spc = spacer(frame)
                        spc.grid(row=1, column=0, pady=10, columnspan=2)
                        entry_stock = ctk_entry(frame, text='Estoque em Toneladas', width=120, height=30)
                        entry_stock.grid(row=2, column=0)

                        apply = ctk_botao(frame, 'Aplicar', command=lambda: finaliza_add_prod(nome, entry_stock),
                                          width=90, height=20)
                        apply.grid(row=2, column=1)

                    def botao_predef(predef):
                        botao = ctk_botao(frame_stock, text=predef,
                                          command=lambda: add_prod(predef), width=120, height=30)
                        return botao

                    lista_nome_prod = []
                    for prod in lista_prod:
                        x = prod.name
                        lista_nome_prod.append(x)

                    i = 2
                    c = 0
                    for predef in lista_pre_def:
                        if lista_nome_prod.__contains__(predef):
                            pass
                        else:
                            predef = predef.removeprefix('T_').lower()
                            predef = predef.title()
                            vars()[predef] = botao_predef(predef)
                            if c < 3:
                                vars()[predef].grid(row=i, column=c, padx=2, pady=2)
                                c += 1
                            else:
                                i += 1
                                vars()[predef].grid(row=i, column=0, padx=2, pady=2)
                                c = 1

                    add_novo_prod = ctk_botao(frame_stock, 'Novo Tipo',
                                              command='', width=120, height=30)
                    add_novo_prod.grid(row=i, column=c, padx=2, pady=2)

                frame_stock = limpa_mini_frame(mini_frame_stock)
                txt_a = ctk_label(frame_stock, 'Escolha um das pré-definições ou\n'
                                               '    crie uma nova categoria: ')
                txt_a.grid(row=0, column=0, columnspan=3, pady=3)
                spc = spacer(frame_stock)
                spc.grid(row=1, column=0, columnspan=3, pady=10)

                pre_def = ['T_MILHO', 'T_CAFE', 'T_TOMATE', 'T_SOJA']
                cria_button_predef_prod(pre_def)

            def command_radio_products(prod):
                txt = ctk_label(frame_top_r, text=f'{prod.name}')
                txt.grid(row=0, column=0, columnspan=2)
                spc = spacer(frame_top_r)
                spc.grid(row=1, column=0, columnspan=2)
                entry_add = ctk_entry(frame_top_r, text='Adicionar ao estoque')
                entry_add.grid(row=2, column=0)
                button_add = ctk_botao(frame_top_r, text='Adicionar', command='')
                button_add.grid(row=2, column=1)
                entry_remove = ctk_entry(frame_top_r, text='Remover ao estoque')
                entry_remove.grid(row=3, column=0)
                button_remove = ctk_botao(frame_top_r, text='Remover', command='')
                button_remove.grid(row=3, column=1)
                entry_new_stock = ctk_entry(frame_top_r, text='Novo Estoque')
                entry_new_stock.grid(row=4, column=0)
                button_new_stock = ctk_botao(frame_top_r, text='Alterar Estoque', command='')
                button_new_stock.grid(row=4, column=1)

            def botao_radio_products(prod):
                b = ctk_radio_button(frame_top_m, text=str(prod),
                                     command=lambda: command_radio_products(prod))
                return b

            lista_prod = busca_prod(id)
            if len(lista_prod) > 0:
                i = 0
                for prod in lista_prod:
                    prodx = (str(prod.name)).removeprefix('T_')
                    vars()[prodx] = botao_radio_products(prod)
                    vars()[prodx].grid(row=i, column=0, pady=2)
                    i += 1
                adicionar_prod = ctk_botao(frame_top_m, text='Adicionar Produto',
                                           command=lambda: command_add_prod(lista_prod, frame_top_r),
                                           width=180, height=40)
                adicionar_prod.grid(row=i, column=0, pady=2)
            else:
                adicionar_prod = ctk_botao(frame_top_m, text='Adicionar Produto',
                                           command=lambda: command_add_prod(lista_prod, frame_top_r),
                                           width=180, height=40)
                adicionar_prod.grid(row=0, column=0, pady=2)

        def limpa_mini_frame(xy):
            xy.destroy()
            Fr = ctk_frame(frame)
            Fr.grid(row=0, column=2, sticky='news')
            Fr.grid_rowconfigure('all', weight=1)
            Fr.grid_columnconfigure('all', weight=1)
            return Fr

        def busca_prod(id: str):
            df = select_property(id)
            lista_prod = []
            for i in range(len(df.axes[1])):
                if i > 5:
                    if df[df.axes[1][i]][0] != 0:
                        lista_prod.append(df[df.axes[1][i]])
            return lista_prod

        lista_propertys = self.__user.get_propertys
        i = 0
        for prop in lista_propertys:
            id = prop[0]
            nome = prop[1]
            vars()[nome] = ctk_radio_button(frame_l, text=str(nome),
                                            command=lambda: command_radio_property(id))
            vars()[nome].grid(row=i, column=0)
            i += 1


        # ---- Frames ----
        w_ger_estoque.grid_rowconfigure(0, weight=1)
        w_ger_estoque.grid_columnconfigure(0, weight=1)

        frame.grid(row=0, column=0, sticky='news', padx=20, pady=20)

        frame_l.grid(row=0, column=0, padx=5, sticky='news')
        frame_top_m.grid(row=0, column=1, sticky='news')

        frame_top_r.grid(row=0, column=2, padx=5, sticky='news')

        frame_bottom.grid(row=1, column=0, columnspan=3, sticky='news', padx=5)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)


        w_ger_estoque.mainloop()

    def w_cadastro_de_propriedade(self):
        self.limpa_tela()

        frame = self.ctk_frame()
        frame_top = self.ctk_frame(frame)
        center = spacer(frame)
        frame_bottom = self.ctk_frame(frame)
        
        botao_voltar = ctk_botao_label(self.window, text='<', command=lambda: self.volta_menu_principal())

        self.lista_frames = [frame, botao_voltar]

        txt = ctk_label(frame_top, text='Cadastro de Propriedade', tamanho_fonte=30)
        user = ctk_label(frame_top, text=f'user: {self.__user.nome}', tamanho_fonte=14,
                         text_color='#4F4F4F')

        spc = spacer(frame_bottom)

        h = 35
        nome_entry = ctk_entry(frame_bottom, text='Nome da Propriedade',
                               width=150, height=h)
        cep_entry = ctk_entry(frame_bottom, text='CEP',
                              width=150, height=h)
        numero_entry = ctk_entry(frame_bottom, text='Nº',
                                 width=150, height=h)
        complemento_entry = ctk_entry(frame_bottom, text='Complemento',
                                      width=350, height=h)

        cadastrar = ctk_botao(frame=frame_bottom, text='Cadastrar nova Properiedade',
                              command=lambda: self.tenta_cadastro_property(nome_entry, cep_entry, numero_entry,
                                                                           complemento_entry, frame_top))

        # -- grid --
        txt.grid(row=0, column=0)
        user.grid(row=1, column=0)

        botao_voltar.place(x=50, y=50)

        nome_entry.grid(row=0, column=0, columnspan=3, sticky='news', pady=12)
        cep_entry.grid(row=1, column=0, sticky='news')
        spc.grid(row=1, column=1)
        numero_entry.grid(row=1, column=2, sticky='news')
        complemento_entry.grid(row=2, column=0, columnspan=3, sticky='news', pady=12)
        cadastrar.grid(row=3, column=0, columnspan=3, sticky='news')

        frame.grid(row=0, column=0)
        frame_top.grid(row=0, column=0)
        center.grid(row=1, column=0, pady=80)
        frame_bottom.grid(row=2, column=0)

    def tenta_cadastro_property(self, nome, cep, numero, complemento, frame_erro):
        try:
            self.msg_erro.destroy()
        except:
            pass
        nome = nome.get()
        cep = cep.get()
        numero = numero.get()
        complemento = complemento.get()
        from server.conSQL import puxa_propertys
        df = puxa_propertys(self.__user.doc)
        lista_nomes = list(df['NOME'])
        print(lista_nomes)
        print(nome)
        if nome in lista_nomes:
            self.msg_erro = CTkLabel(frame_erro, text='Você já tem uma propriedade com esse nome',
                                     text_color=red)
            self.msg_erro.grid(row=2, column=0)
            raise ValueError('Nome de propriedade em uso')
        if len(nome) > 60:
            self.msg_erro = CTkLabel(frame_erro, text='O nome deve ter até 60 caracteres',
                                     text_color=red)
            self.msg_erro.grid(row=2, column=0)
            raise ValueError('Limite de caracteres')
        lista_ceps = list(df['CEP'])
        if cep in lista_ceps:
            self.msg_erro = CTkLabel(frame_erro, text='Você já tem uma propriedade neste CEP',
                                     text_color=red)
            self.msg_erro.grid(row=2, column=0)
            raise ValueError('CEP duplicado')
        if not cep.isnumeric():
            self.msg_erro = CTkLabel(frame_erro, text='CEP inválido',
                                     text_color=red)
            self.msg_erro.grid(row=2, column=0)
            raise ValueError('Campo deve conter apenas digitos')
        if len(numero) != 3:
            self.msg_erro = CTkLabel(frame_erro, text='O campo Numero deve ter 3 digitos',
                                     text_color=red)
            self.msg_erro.grid(row=2, column=0)
            raise ValueError('Limite de caracteres')
        if not numero.isnumeric():
            self.msg_erro = CTkLabel(frame_erro, text='O campo Numero deve conter apenas digitos',
                                     text_color=red)
            self.msg_erro.grid(row=2, column=0)
            raise ValueError('Campo deve conter apenas digitos')
        if len(complemento) > 30:
            self.msg_erro = CTkLabel(frame_erro, text='O campo Complemento deve conter até 30 caracteres',
                                     text_color=red)
            self.msg_erro.grid(row=2, column=0)
            raise ValueError('Limite de caracteres')
        from server.Register.Property import Property
        Property(nome, self.__user.doc, cep, numero, complemento, False)
        self.msg_erro = CTkLabel(frame_erro, text=f'Propriedade {nome} cadastrada !',
                                 text_color=c2)
        self.msg_erro.grid(row=2, column=0)

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

    def ctk_frame(self, frame=None, fg_color=bkg):
        if not frame:
            frame = self.window
        fr = CTkFrame(frame)
        fr.configure(fg_color=fg_color)
        return fr





app2 = App()
