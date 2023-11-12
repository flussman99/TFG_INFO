import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD


class FormularioLoginDesign(tk.Toplevel):

    #De momento verificamos únicamente a nuestra cuenta de MetaTrader
    def verificar(self):
        usu = self.usuario.get()
        password = self.password.get()
        if(usu == "51468408" and password == "YHPuThmy"):
            messagebox.showinfo(message="Sesión iniciada correctamente", title="Mensaje")
            #FormularioMaestroDesign()
        else:
            messagebox.showerror(message="El usuario o la contraseña son incorrectos",title="Mensaje")

    def __init__(self, panel_principal):
        
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.cuerpo_principal = tk.Frame(panel_principal)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)


        title = tk.Label(self.cuerpo_principal, text="Inicio de sesion", font=('Times',30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        #Parte de Usuario
        etiqueta_usuario =tk.Label(self.cuerpo_principal, text="Usuario", font=('Times', 14),fg="#666a88",bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20,pady=5)
        self.usuario = ttk.Entry(self.cuerpo_principal, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=20,pady=10)

        #Parte de Contraseña
        etiqueta_password = tk.Label(self.cuerpo_principal, text="Contraseña", font=('Times', 14),fg="#666a88",bg='#fcfcfc', anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(self.cuerpo_principal, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        #Botón de Iniciar Sesión
        inicio = tk.Button(self.cuerpo_principal, text="Iniciar sesion",font=('Times', 15, BOLD), bg='#3a7ff6', bd=0,fg="#fff", command=self.verificar)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", (lambda event: self.verificar()))
