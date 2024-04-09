import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Entry, Text, Button, PhotoImage
from config2 import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_imagenes as util_img
import pandas as pd
import psutil
import os
import sys 
from bot import Bot as bt
import MetaTrader5 as mt5 #Importamos libreria de metatrader le metemos el as para utilizarla con un nombre mas corto
import matplotlib.pyplot as plt
import mysql.connector
from configDB import DBConfig



class FormularioInicioSesion():
    
    def obtener_dimensiones(self):
        print("Obteniendo dimensiones")
        self.frame_width = self.frame_azul.winfo_width() * 0.6
        self.frame_height = self.frame_azul.winfo_height() * 0.8

        print(self.frame_width)
        print(self.frame_height)

    def __init__(self, panel_principal, abrir_panel_inicio, cambiar_estado_sesion, bool_inicio):
        
        self.bool_inicio = bool_inicio
        self.panel_inicio = abrir_panel_inicio
        self.cambiar_estado_sesion = cambiar_estado_sesion

        # Dimensiones del frame
        self.frame_width = 1
        self.frame_height = 1

        panel_principal.after(100, self.obtener_dimensiones)

        # Tamaño de la fuente basado en las dimensiones del frame
        self.font_size = int(min(self.frame_width, self.frame_height) * 0.2)        # Añadir los elementos al frame azul
        print (self.font_size)

        # Conexión a la base de datos
        self.conn = mysql.connector.connect(
                    host=DBConfig.HOST,
                    user=DBConfig.USER,
                    password=DBConfig.PASSWORD,
                    database=DBConfig.DATABASE,
                    port=DBConfig.PORT
                )
        
        # Crear un frame interno para el panel azul
        self.frame_azul = tk.Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL, bd=0, highlightthickness=0)
        self.frame_azul.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.8)

        #If para saber si ya se inicio sesion
        if self.bool_inicio == False:
            self.iniciar_Sesion()
        else:
            self.cerrar_Sesion()

        #PARA QUE SEA RESPONSIVE, EL PRIMERO CUANDO SE MODIFICA EL TAMAÑO DE LA VISTA, EL SEGUNDO CUANDO SE MAXIMIZA O RESTAURA LA VISTA
        panel_principal.bind("<Configure>", self.on_parent_configure)

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)

    def iniciar_Sesion(self):
        #BIENVENIDO
        #Label Bienvenido
        self.label_bienvenido = tk.Label(self.frame_azul, bg=COLOR_CUERPO_PRINCIPAL, text="BIENVENIDO", font=("Berlin Sans FB", 12, "bold"), fg="#2d367b")
        self.label_bienvenido.pack(pady=0)

        #INICIA SESION
        #Label Inicia Sesión
        label_inicia_sesion = tk.Label(self.frame_azul, bg=COLOR_CUERPO_PRINCIPAL, text="Inicia Sesión para continuar", font=("Helvetica", int(self.font_size*0.25)), fg="grey")
        label_inicia_sesion.pack(padx=0)

        #USUARIO
        #Label Usuario
        self.label_usuario = tk.Label(self.frame_azul, bg=COLOR_CUERPO_PRINCIPAL, text="USUARIO", font=("Calibri", int(self.font_size*0.25)), fg="#2d367b", anchor="w")
        self.label_usuario.pack(pady=5, padx=10, anchor="w")

        #Cargar imagenes
        self.imagen_usuario = util_img.leer_imagen("src/imagenes/extras/fondo_gris.png", (100, 10))
        self.icono_usuario = util_img.leer_imagen("src/imagenes/extras/usuario_inicio.png", (20, 20))

        #Crear un label con la imagen
        self.label_imagen_usuario = tk.Label(self.frame_azul, image=self.imagen_usuario, bg=COLOR_CUERPO_PRINCIPAL)
        self.label_imagen_usuario.pack(fill="x")

        # Crear un label con el icono a la izquierda y la imagen de fondo
        self.label_icono = tk.Label(self.label_imagen_usuario, image=self.icono_usuario, bg="#d9d9d9")
        self.label_icono.pack(side="left", padx=(10, 10))
        
        # Crear el Entry con margen izquierdo y fuente Calibri
        self.entry_usuario = tk.Entry(self.label_imagen_usuario, bg="#d9d9d9", font=("Calibri"))
        self.entry_usuario.insert(0, "admin")
        self.entry_usuario.pack(pady=5, padx=(0, 10), fill="x")  

        #CONTRASEÑA
        #Label Contraseña
        self.label_contra = tk.Label(self.frame_azul, bg=COLOR_CUERPO_PRINCIPAL, text="CONTRASEÑA", font=("Calibri", int(self.font_size*0.25)), fg="#2d367b", anchor="w")
        self.label_contra.pack(pady=(30,0), padx=10, anchor="w")

        #Cargar imagenes
        self.imagen_contra = util_img.leer_imagen("src/imagenes/extras/fondo_gris.png", (100, 10))
        self.icono_contra = util_img.leer_imagen("src/imagenes/extras/candado_inicio.png", (20, 20))

        #Crear un label con la imagen
        self.label_imagen_contra = tk.Label(self.frame_azul, image=self.imagen_contra, bg=COLOR_CUERPO_PRINCIPAL)
        self.label_imagen_contra.pack(fill="x")

        # Crear un label con el icono a la izquierda y la imagen de fondo
        self.label_icono2 = tk.Label(self.label_imagen_contra, image=self.icono_contra, bg="#d9d9d9")
        self.label_icono2.pack(side="left", padx=(10, 10))
        
        # Crear el Entry con margen izquierdo y fuente Calibri
        self.entry_contra = tk.Entry(self.label_imagen_contra, bg="#d9d9d9", font=("Calibri"), show="*")
        self.entry_contra.insert(0, "123456789")
        self.entry_contra.pack(pady=5, padx=(0, 10), fill="x")
        
        #BOTON INICIAR SESION
        self.boton_iniciar_sesion = tk.Button(self.frame_azul, text="    INICIAR SESIÓN   ", bg="#2d367b", fg="white", font=("Calibri", 20, "bold"), relief="flat", activebackground="#2d367b", activeforeground="white", command=self.verificar)
        self.boton_iniciar_sesion.pack(pady=(20,0))

    def cerrar_Sesion(self):
        #Cerrar sesión
        #Label Cerrar Sesión
        self.label_cerrar_sesion = tk.Label(self.frame_azul, bg=COLOR_CUERPO_PRINCIPAL, text="CERRAR SESIÓN", font=("Helvetica", int(self.font_size*0.25)), fg="grey")
        self.label_cerrar_sesion.pack(padx=0)

        #Boton Cerrar Sesión
        self.boton_cerrar_sesion = tk.Button(self.frame_azul, text="    CERRAR SESIÓN   ", bg="#2d367b", fg="white", font=("Calibri", 20, "bold"), relief="flat", activebackground="#2d367b", activeforeground="white", command=self.desverificar)
        self.boton_cerrar_sesion.pack(pady=(20,0))
        

    def on_parent_configure(self, event):
        # Se llama cuando cambia el tamaño de la ventana
        self.update_font_size()
        self.update_font()
        self.update_imagenes()

    def on_parent_configure2(self):
        # Se llama cuando cambia el tamaño de la ventana
        if (self.frame_width != self.frame_azul.winfo_width() or self.frame_height != self.frame_azul.winfo_height()):
            self.update_font_size()
            self.update_font()
            self.frame_azul.after(100, self.update_imagenes)
        self.frame_azul.after(1000, self.on_parent_configure2)

    def update_imagenes(self):
        # Actualiza el tamaño de las imágenes en función del tamaño de la ventana
        self.imagen_usuario = util_img.leer_imagen("src/imagenes/extras/fondo_gris.png", (int(self.frame_width*1), int(self.frame_height*0.1)))
        self.label_imagen_usuario.configure(image=self.imagen_usuario)

        self.icono_usuario = util_img.leer_imagen("src/imagenes/extras/usuario_inicio.png", (int(self.frame_width*0.05), int(self.frame_height*0.05)))
        self.label_icono.configure(image=self.icono_usuario)

        self.imagen_contra = util_img.leer_imagen("src/imagenes/extras/fondo_gris.png", (int(self.frame_width*1), int(self.frame_height*0.1)))
        self.label_imagen_contra.configure(image=self.imagen_contra)

        self.icono_contra = util_img.leer_imagen("src/imagenes/extras/candado_inicio.png", (int(self.frame_width*0.05), int(self.frame_height*0.05)))
        self.label_icono2.configure(image=self.icono_contra)

    def update_font_size(self):
        # Actualiza el tamaño de la fuente en función del tamaño de la ventana
        self.frame_width = self.frame_azul.winfo_width()
        self.frame_height = self.frame_azul.winfo_height()
        
        self.font_size = int(min(self.frame_width, self.frame_height) * 0.2)

    def update_font(self):
        self.label_bienvenido.configure(font=("Berlin Sans FB",  int(self.font_size*0.6), "bold"))

    #Hay que hacer que pueda logarse cualquier otro usuario
    def verificar(self):
        usu = self.entry_usuario.get()
        password = self.entry_contra.get()
        cursor = self.conn.cursor()
        sql = "SELECT nombre, userMetaTrader, passwordMetaTrader FROM Usuarios WHERE user = %s AND contraseña = %s"
        cursor.execute(sql, (usu,password))
        resultado = cursor.fetchone()
        server = "ICMarketsEU-Demo"
        if resultado:
            nombre_usuario = resultado[0]
            usermt5 = resultado[1]
            passwordmt5 = resultado[2]
            if not self.mt5_login(int(usermt5),passwordmt5,server):
                messagebox.showerror(message="Conexión con cuenta de metatrader fallida", title="Mensaje")
            else:
                #messagebox.showinfo(message="Sesión iniciada correctamente", title="Mensaje") 
                self.cambiar_estado_sesion()
                self.panel_inicio()
        else:
            messagebox.showerror(message="El usuario o la contraseña son incorrectos",title="Mensaje")
        
        cursor.close()
        # with open("login.txt", 'r') as f:
        #         lines = f.readlines()
        #         usr = lines[0].strip()
        #         key = lines[1].strip()
        #         server = lines[2].strip()
        # if(usu!=usr or password!=key):
        #     messagebox.showerror(message="El usuario o la contraseña son incorrectos",title="Mensaje")
        # else: 
            #messagebox.showinfo(message="Sesión iniciada correctamente", title="Mensaje")  
        
    def desverificar(self):
        #Hacer lo que sea para cerrar sesion vaya
        self.cerrar_mt5()

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