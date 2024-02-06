
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import pandas as pd
import sys 
from bot import Bot as bt
import MetaTrader5 as mt5 #Importamos libreria de metatrader le metemos el as para utilizarla con un nombre mas corto


class FormularioLoginDesign(tk.Toplevel):

   
    def __init__(self, panel_principal, label_usuario, abrir_panel_inversiones, boton_inversiones):
        
        self.labelUsuario = label_usuario
        self.abrir_inv = abrir_panel_inversiones
        self.boton_inv = boton_inversiones
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
        self.usuario.insert(0, "51468408")  # Insertar el usuario predeterminado
        

        #Parte de Contraseña
        etiqueta_password = tk.Label(self.cuerpo_principal, text="Contraseña", font=('Times', 14),fg="#666a88",bg='#fcfcfc', anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(self.cuerpo_principal, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.insert(0, "YHPuThmy")
        self.password.config(show="*")

        #Botón de Iniciar Sesión
        inicio = tk.Button(self.cuerpo_principal, text="Iniciar sesion",font=('Times', 15, BOLD), bg='#3a7ff6', bd=0,fg="#fff", command=self.verificar)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", (lambda event: self.verificar()))
 #De momento verificamos únicamente a nuestra cuenta de MetaTrader
    def verificar(self):
        usu = self.usuario.get()
        password = self.password.get()
        with open("login.txt", 'r') as f:
                lines = f.readlines()
                usr = lines[0].strip()
                key = lines[1].strip()
                server = lines[2].strip()
        if(usu!=usr or password!=key):
            messagebox.showerror(message="El usuario o la contraseña son incorrectos",title="Mensaje")
        else: 
            #messagebox.showinfo(message="Sesión iniciada correctamente", title="Mensaje")  
            if not self.mt5_login(int(usr),key,server):
                quit()
            else:
                self.labelUsuario.config(text=f"Usuario: {usu}")
                self.boton_inv["state"] = tk.NORMAL
                self.abrir_inv()
            #FormularioMaestroDesign()

    def mt5_login(self,usr:int, passw:str, serv:str) -> bool:
        """Function to initialize the metatrader 5 aplication
        and login wiht our account details.

        Args:
            usr (int): User ID.
            password (str): Password

        Returns:
            bool: True if everything is OK, False if not
        """
        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            return False
        
        authorized=mt5.login(login=usr,password=passw,server=serv)
        if authorized:
            # display trading account data 'as is'
            #print(mt5.account_info())
            # display trading account data in the form of a list
            print("Show account_info()._asdict():")
            account_info_dict = mt5.account_info()._asdict()

            for prop in account_info_dict:
                print("  {}={}".format(prop, account_info_dict[prop]))

        else:
            print("failed to connect at account #{}, error code: {}".format(usr, mt5.last_error()))
            return False

        return True
           