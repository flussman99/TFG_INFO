
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox, Canvas, Entry, Text, Button, PhotoImage
from tkinter.font import BOLD
import pandas as pd
import psutil
import os
import sys 
from bot import Bot as bt
import MetaTrader5 as mt5 #Importamos libreria de metatrader le metemos el as para utilizarla con un nombre mas corto


class FormularioLoginDesign(tk.Toplevel):

   
    def __init__(self, panel_principal, label_usuario, boton_inversiones, boton_operaciones, abrir_panel_inicio):


        self.panel_inicio = abrir_panel_inicio
        self.labelUsuario = label_usuario
        self.boton_inv = boton_inversiones
        self.boton_op = boton_operaciones
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.cuerpo_principal = tk.Frame(panel_principal, width=1366, height=667)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

        self.cuerpo_principal.configure(bg = "#FFFFFF")


        canvas = Canvas(
            self.cuerpo_principal,
            bg = "#FFFFFF",
            height = 667,
            width = 1366,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        image_image_1 = PhotoImage(
            file="src/imagenes/assets/fondo.png")
        image_1 = canvas.create_image(
            683.0,
            333.0,
            image=image_image_1
        )

        image_image_2 = PhotoImage(
            file="src/imagenes/assets/logo_pequeño.png")
        image_2 = canvas.create_image(
            683.0,
            172.0,
            image=image_image_2
        )

        canvas.create_text(
            301.0,
            284.0,
            anchor="nw",
            text="Usuario:",
            fill="#FFFFFF",
            font=("Calistoga Regular", 20 * -1)
        )

        canvas.create_text(
            301.0,
            410.0,
            anchor="nw",
            text="Contraseña:",
            fill="#FFFFFF",
            font=("Calistoga Regular", 20 * -1)
        )

        entry_image_1 = PhotoImage(
            file="src/imagenes/assets/entry_comun_usr_psswd.png")
        entry_bg_1 = canvas.create_image(
            683.0,
            359.0,
            image=entry_image_1
        )

        self.usuario = Entry(
            canvas,
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            highlightthickness=0,
            font=("Calistoga Regular", 20 * -1)
        )
        canvas.create_window(296, 331, window=self.usuario)
        self.usuario.insert(0, "51468408")

        self.usuario.place(
            x=296.0,
            y=331.0,
            width=774.0,
            height=52.0
        )

        entry_image_2 = PhotoImage(
            file="src/imagenes/assets/entry_comun_usr_psswd.png")
        entry_bg_2 = canvas.create_image(
            683.0,
            487.0,
            image=entry_image_2
        )

        self.password = Entry(
            canvas,
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            highlightthickness=0,
            font=("Calistoga Regular", 20 * -1)
        )
        canvas.create_window(296, 460, window=self.password)
        self.password.insert(0, "YHPuThmy")
        self.password.config(show="*")

        self.password.place(
            x=296.0,
            y=460.0,
            width=774.0,
            height=52.0
        )

        button_image_1 = PhotoImage(
            file="src/imagenes/assets/boton_login.png")
        self.inicio = Button(
            canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.verificar,
            relief="flat"
        )
        canvas.create_window(609, 577, window=self.inicio)
        self.inicio.bind("<Return>", (lambda event: self.verificar()))

        self.inicio.place(
            x=609.0,
            y=577.0,
            width=147.0,
            height=38.0
        )

        self.cuerpo_principal.mainloop()
        #Hay que hacer que pueda logarse cualquier otro usuario


    def verificar(self):
        usu = self.usuario.get()
        password = self.password.get()
        server = "ICMarketsEU-Demo"
        # with open("login.txt", 'r') as f:
        #         lines = f.readlines()
        #         usr = lines[0].strip()
        #         key = lines[1].strip()
        #         server = lines[2].strip()
        # if(usu!=usr or password!=key):
        #     messagebox.showerror(message="El usuario o la contraseña son incorrectos",title="Mensaje")
        # else: 
            #messagebox.showinfo(message="Sesión iniciada correctamente", title="Mensaje")  
        if not self.mt5_login(int(usu),password,server):
            messagebox.showerror(message="El usuario o la contraseña son incorrectos",title="Mensaje")
            # quit()
        else:
            messagebox.showinfo(message="Sesión iniciada correctamente", title="Mensaje") 
            self.labelUsuario.config(text=f"Usuario: {usu}")
            self.boton_op["state"] = tk.NORMAL
            self.boton_inv["state"] = tk.NORMAL
            self.lift()
            self.panel_inicio()

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
            self.cerrar_mt5()
            return False

        return True 
    
    def cerrar_mt5(self):
        for proc in psutil.process_iter():
            if "terminal64.exe" in proc.name():  # El nombre del proceso puede variar
                os.kill(proc.pid, 9)  # Envía la señal SIGKILL para forzar el cierre
                break