import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Entry, Text, Button, PhotoImage
from config2 import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
from formularios.formulario_backtesting_clasicas import FormularioBackTestingClasicas
from formularios.formulario_inversion_clasicas import FormularioInversionClasicas
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


class FormularioClasicas():

    def __init__(self, panel_principal, user_id):

        self.user_id = user_id
        self.frame_width_superior = 0
        self.frame_height_superior = 0

        #Frame principal 
        self.frame_principal = tk.Frame(panel_principal, bg="lightgray")
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Frame superior 
        self.frame_superior = tk.Frame(self.frame_principal, bg="lightblue")
        self.frame_superior.pack(fill=tk.BOTH, expand=True)

        # Frame inferior (con scrollbar)
        self.frame_inferior = tk.Frame(self.frame_principal, bg="lightgray")
        self.frame_inferior.pack(fill=tk.BOTH, expand=True)

        self.superior()

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)   

        #Llamada a la función on_parent_configure cuando se redimensiona la ventana
        panel_principal.bind("<Configure>", self.on_parent_configure)

     

    def obtener_dimensiones(self):
        print("Obteniendo dimensiones")
        self.frame_width_superior = self.frame_superior.winfo_width() 
        self.frame_height_superior = self.frame_superior.winfo_height()
        print("Ancho: ", self.frame_width_superior)
        print("Alto: ", self.frame_height_superior)

    def superior(self):
        
        #Titulo para el frame superior
        self.label_titulo_superior = tk.Label(self.frame_superior, text="Operaciones Clásicas", font=("Berlin Sans FB", 30, "bold"), bg="lightblue", fg="white")
        self.label_titulo_superior.place(relx=0.5, rely=0.2, anchor="center")

        #cargar imagen de fondo
        self.icono_operaciones_clasicas = util_img.leer_imagen("src/imagenes/extras/backtesting.png", (10,10))
        self.icono_operaciones_creativas = util_img.leer_imagen("src/imagenes/extras/invertir.png", (10,10))

        #Boton para "Operaciones Clásicas" con imagen de fondo y sin bordes
        self.boton_inversion_clasicas = tk.Button(self.frame_superior, image=self.icono_operaciones_clasicas, bg="lightblue", command=self.backtesting_clasicas, borderwidth=0, highlightthickness=0)        
        self.boton_inversion_clasicas.place(relx=0.1, rely=0.5)

        #Boton para "Operaciones Creativas" con imagen de fondo y sin bordes
        self.boton_inversion_creativas = tk.Button(self.frame_superior, image=self.icono_operaciones_creativas, bg="lightblue", command=self.invertir_clasicas, borderwidth=0, highlightthickness=0)
        self.boton_inversion_creativas.place(relx=0.6, rely=0.5)


    def on_parent_configure(self, event):
        # Se llama cuando cambia el tamaño de la ventana
        self.obtener_dimensiones()
        self.update_superior()

    def on_parent_configure2(self):
        # Se llama cuando cambia el tamaño de la ventana
        if (self.frame_width_superior != self.frame_superior.winfo_width() or self.frame_height_superior != self.frame_superior.winfo_height()):
            self.obtener_dimensiones()
            self.update_superior()
        self.frame_superior.after(1000, self.on_parent_configure2)

    def update_superior(self):
        #Ajustar el tamaño del titulo
        self.label_titulo_superior.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width_superior, self.frame_height_superior) * 0.2)*0.6), "bold"))

        #Ajustar el tamaño del boton de operaciones clásicas
        self.icono_operaciones_clasicas = util_img.leer_imagen("src/imagenes/extras/backtesting.png", (int(self.frame_width_superior * 0.3), int(self.frame_height_superior * 0.4)))
        self.boton_inversion_clasicas.configure(image=self.icono_operaciones_clasicas)
        

        #Ajustar el tamaño del boton de operaciones creativas
        self.icono_operaciones_creativas = util_img.leer_imagen("src/imagenes/extras/invertir.png", (int(self.frame_width_superior * 0.3), int(self.frame_height_superior * 0.4)))
        self.boton_inversion_creativas.configure(image=self.icono_operaciones_creativas)

    
    def backtesting_clasicas(self):
        self.limpiar_panel(self.frame_principal)     
        FormularioBackTestingClasicas(self.frame_principal, self.user_id)

    def invertir_clasicas(self):
        self.limpiar_panel(self.frame_principal)     
        FormularioInversionClasicas(self.frame_principal)

    def limpiar_panel(self,panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()