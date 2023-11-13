
import bot as bt
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox
from tkinter.font import BOLD


class FormularioLoginDesign(tk.Toplevel):

    #De momento verificamos únicamente a nuestra cuenta de MetaTrader
    def verificar(self):
        usu = self.usuario.get()
        password = self.password.get()
        with open("login.txt", 'r') as f:
                lines = f.readlines()
                usr = int(lines[0].strip())
                key = lines[1].strip()
                server = lines[2].strip()

        
        if(usu!=usr | password!=key):
            messagebox.showerror(message="El usuario o la contraseña son incorrectos",title="Mensaje")
        else:   
            # Creating a bot
            b = bt.Bot(1, 15*60, "SAN.MAD")
            # Login into mt5
            if not b.mt5_login(usr,password,server):
                quit()
            b.thread_tick_reader()
            #b.thread_slope_abs_rel()
            #b.thread_MACD()
            #b.thread_RSI()
            #b.thread_orders()
            b.wait()

            # Haciendo una gráfica de los datos
            lista_segundos = b.get_ticks()
            xAxis = []
            yAxis = []
            i = 1
            if len(lista_segundos) < 10000:
                for element in b.get_ticks():
                    xAxis.append(i)
                    yAxis.append(element)
                    i += 1

            plt.plot(xAxis, yAxis)
            plt.show()
            #plt.savefig()

            messagebox.showinfo(message="Sesión iniciada correctamente", title="Mensaje")
            #FormularioMaestroDesign()
           
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
