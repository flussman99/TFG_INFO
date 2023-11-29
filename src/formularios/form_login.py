
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import pandas as pd
import sys 
from bot import Bot as bt

class FormularioLoginDesign(tk.Toplevel):

   
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
        self.usuario = ttk.Entry(self.cuerpo_principal, textvariable="51468408",font=('Times', 14))
        self.usuario.insert(0, "51468408")  # Insertar el usuario predeterminado
        self.usuario.pack(fill=tk.X, padx=20,pady=10)

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
            b = bt(1, 3600, "SAN.MAD")#camibiar esta accion por una lista que podamos elegir
            #cada 3600 segundos cogemos un tick
            if not b.mt5_login(int(usr),key,server):
                quit()

            b.thread_tick_reader()
            b.wait()
            lista_segundos = b.get_ticks()
            xAxis = []
            yAxis = []
            i = 1
            print("Ticks received:",len(lista_segundos))

            print("Display obtained ticks 'as is'")
            count = 0
            for tick in lista_segundos:
                count+=1
                print(tick)
                if count >= 10:
                    break
            ticks_frame = pd.DataFrame(lista_segundos)
            print(ticks_frame.head(10))
          
            #FormularioMaestroDesign()
           