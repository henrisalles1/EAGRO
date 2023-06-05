from tkinter import *

# -- Geral --
inicio = Tk()
inicio.title('Logo')
inicio.geometry('500x500')

# -- frame --
frame_top = Frame(inicio)
frame_bottom = Frame(inicio)

# -- txt --
txt_E_AGRO = Label(frame_top, text='LOGO', justify='center', font=('Arial', 25))
texto_orientacao = Label(frame_top, text='Bem vindo !', justify='center', font=('Arial', 12))
login = Button(frame_bottom, text='Login', command='', font=('Arial', 13), height=2, width=20)
register = Button(frame_bottom, text='Registre-se', command='', font=('Arial', 13), height=2, width=20)

# -- grid --
txt_E_AGRO.grid(column=0, row=0, pady=5)
texto_orientacao.grid(column=0, row=1)
login.grid(column=0, row=2)
register.grid(column=0, row=3, pady=20)

# -- flexgrid --
# - row -
inicio.grid_rowconfigure(0, weight=3)
inicio.grid_rowconfigure(1, weight=1)
inicio.grid_rowconfigure(2, weight=1)
inicio.grid_rowconfigure(3, weight=1)

# - column -
inicio.grid_columnconfigure(0, weight=1000)

frame_top.grid(row=0)
frame_bottom.grid(row=1)


inicio.mainloop()

