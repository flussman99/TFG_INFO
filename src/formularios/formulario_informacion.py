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


class FormularioInformacion():

    def __init__(self, panel_principal):
        self.frame_width = 0
        self.frame_height = 0

        #Frame principal 
        self.frame_principal = tk.Frame(panel_principal, bg="lightgray")
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Frame superior 
        self.frame_superior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_superior.pack(fill=tk.BOTH, expand=True)

        # Frame inferior 
        self.frame_inferior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_inferior.pack(fill=tk.BOTH, expand=True)

        self.superior()
        self.inferior()

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)   

        #Llamada a la función on_parent_configure cuando se redimensiona la ventana
        panel_principal.bind("<Configure>", self.on_parent_configure)

     

    
    def superior(self):

        #Titulo informacion
        self.titulo_info = tk.Label(self.frame_superior, text="Información del Proyecto:")
        self.titulo_info.configure(background=COLOR_CUERPO_PRINCIPAL, foreground="#2d367b", font=("Berlin Sans FB", 16, "bold"))
        self.titulo_info.pack(pady=(0, 5), padx=10, anchor="w")

        #Titulo descripcion
        self.titulo_descripcion = tk.Label(self.frame_superior, text="Descripción del Proyecto:")
        self.titulo_descripcion.configure(background=COLOR_CUERPO_PRINCIPAL, foreground="#2d367b", font=("Berlin Sans FB", 16, "bold"))
        self.titulo_descripcion.pack(pady=(0, 5), padx=10, anchor="w")

        #frame para la descripción
        self.frame_descripcion = tk.Frame(self.frame_superior, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_descripcion.pack(pady=(0, 5), padx=10, anchor="w")

        # Descripción 
        self.descripcion_info = tk.Label(self.frame_descripcion, justify="left", wraplength=600, font=("Aptos", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.descripcion_info.configure(text="Trabajo de Fin de Grado: Aplicación de Análisis de Precios de Acciones \nEste proyecto se centra en el desarrollo de una aplicación que tiene como objetivo realizar comparativas exhaustivas de análisis sobre los precios de las acciones en el mercado financiero. La aplicación emplea diversas características y sucesos reales para evaluar y entender las fluctuaciones en los precios de las acciones. \nCaracterísticas principales:\n     - Análisis detallado de datos históricos de precios de acciones.\n     - Identificación y consideración de características específicas de las acciones.\n     - Evaluación de eventos y sucesos reales que impactan en los mercados financieros.\nLa aplicación proporciona una interfaz intuitiva para que los usuarios exploren y comprendan mejor el comportamiento del mercado. Además, permite comparar diferentes análisis y escenarios, facilitando la toma de decisiones informadas en el ámbito financiero.\nEste proyecto busca no solo ofrecer una herramienta práctica para analistas financieros y profesionales del mercado, sino también servir como un aporte significativo al campo de estudio de la inversión y finanzas.\n¡Explora, analiza y comprende el mundo financiero con nuestra aplicación de Análisis de Precios de Acciones!")
        self.descripcion_info.pack(pady=(0, 5), padx=5, anchor="w")

    def inferior(self):
        #Tirulo participantes
        self.titulo_participantes = tk.Label(self.frame_inferior, text="Participantes:")
        self.titulo_participantes.configure(background=COLOR_CUERPO_PRINCIPAL, foreground="#2d367b", font=("Berlin Sans FB", 16, "bold"))
        self.titulo_participantes.pack(pady=(0, 5), padx=10, anchor="w")

        #frame para los participantes
        self.frame_participantes = tk.Frame(self.frame_inferior, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_participantes.pack(pady=(0, 5), padx=10, anchor="w")

        #Cargar imagenes de los participantes
        self.participante1 = util_img.leer_imagen("src/imagenes/participantes/alvaro.png", (10,10))
        self.participante2 = util_img.leer_imagen("src/imagenes/participantes/cristian.png", (10,10))
        self.participante3 = util_img.leer_imagen("src/imagenes/participantes/david.png", (10,10))
        self.participante4 = util_img.leer_imagen("src/imagenes/participantes/notkero.png", (10,10))
        self.participante5 = util_img.leer_imagen("src/imagenes/participantes/jose.png", (10,10))

        # Crear un Frame para cada imagen y empaquetarlos horizontalmente
        self.frame_participante1 = tk.Frame(self.frame_participantes, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_participante1.pack(side="left", padx=5)  # Empaquetar a la izquierda con un espacio de 5 píxeles
        self.label_participante1 = tk.Label(self.frame_participante1, image=self.participante1)
        self.label_participante1.pack()
        self.label_nombre_participante1 = tk.Label(self.frame_participante1, text="Álvaro Cordero", bg=COLOR_CUERPO_PRINCIPAL, font=("Berlin Sans FB", 10, "bold"))
        self.label_nombre_participante1.pack()

        self.frame_participante2 = tk.Frame(self.frame_participantes, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_participante2.pack(side="left", padx=5)  # Empaquetar a la izquierda con un espacio de 5 píxeles
        self.label_participante2 = tk.Label(self.frame_participante2, image=self.participante2)
        self.label_participante2.pack()
        self.label_nombre_participante2 = tk.Label(self.frame_participante2, text="Cristian Manzanas", bg=COLOR_CUERPO_PRINCIPAL, font=("Berlin Sans FB", 10, "bold"))
        self.label_nombre_participante2.pack()

        self.frame_participante3 = tk.Frame(self.frame_participantes, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_participante3.pack(side="left", padx=5)  # Empaquetar a la izquierda con un espacio de 5 píxeles
        self.label_participante3 = tk.Label(self.frame_participante3, image=self.participante3)
        self.label_participante3.pack()
        self.label_nombre_participante3 = tk.Label(self.frame_participante3, text="David Viejo", bg=COLOR_CUERPO_PRINCIPAL, font=("Berlin Sans FB", 10, "bold"))
        self.label_nombre_participante3.pack()

        self.frame_participante4 = tk.Frame(self.frame_participantes, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_participante4.pack(side="left", padx=5)  # Empaquetar a la izquierda con un espacio de 5 píxeles
        self.label_participante4 = tk.Label(self.frame_participante4, image=self.participante4)
        self.label_participante4.pack()
        self.label_nombre_participante4 = tk.Label(self.frame_participante4, text="Notkero Gomez", bg=COLOR_CUERPO_PRINCIPAL, font=("Berlin Sans FB", 10, "bold"))
        self.label_nombre_participante4.pack()

        self.frame_participante5 = tk.Frame(self.frame_participantes, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_participante5.pack(side="left", padx=5)  # Empaquetar a la izquierda con un espacio de 5 píxeles
        self.label_participante5 = tk.Label(self.frame_participante5, image=self.participante5)
        self.label_participante5.pack()
        self.label_nombre_participante5 = tk.Label(self.frame_participante5, text="Jose del Río", bg=COLOR_CUERPO_PRINCIPAL, font=("Berlin Sans FB", 10, "bold"))
        self.label_nombre_participante5.pack()

    def on_parent_configure(self, event):
        # Se llama cuando cambia el tamaño de la ventana
        self.obtener_dimensiones()
        self.update()

    def on_parent_configure2(self):
        # Se llama cuando cambia el tamaño de la ventana
        if (self.frame_width != self.frame_principal.winfo_width() or self.frame_height != self.frame_principal.winfo_height()):
            self.obtener_dimensiones()
            self.update()
        self.frame_principal.after(1000, self.on_parent_configure2)

    
    def obtener_dimensiones(self):
        print("Obteniendo dimensiones")
        self.frame_width = self.frame_principal.winfo_width() 
        self.frame_height = self.frame_principal.winfo_height()
        print("Ancho: ", self.frame_width)
        print("Alto: ", self.frame_height)


    def limpiar_panel(self,panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()

    def update(self):
        #Ajustar el tamaño del titulo
        self.titulo_info.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.25), "bold"))

        #Ajustar el tamaño de los subtitulos
        self.titulo_descripcion.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.15), "bold"))  

        #Ajustar el tamaño del frame de descripción y el wraplength
        self.frame_descripcion.config(width=self.frame_width-25)
        self.descripcion_info.config(wraplength=self.frame_width-25)
        self.descripcion_info.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))  


        #Ajustar el tamaño del titulo de los participantes
        self.titulo_participantes.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.15), "bold"))

        #Ajustar el tamaño de las imagenes de los participantes
        self.participante1 = util_img.leer_imagen("src/imagenes/participantes/alvaro.png", (int(self.frame_width * 0.15), int(self.frame_height * 0.25)))
        self.label_participante1.configure(image=self.participante1)
        self.label_nombre_participante1.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

        self.participante2 = util_img.leer_imagen("src/imagenes/participantes/cristian.png", (int(self.frame_width * 0.15), int(self.frame_height * 0.25)))
        self.label_participante2.configure(image=self.participante2)
        self.label_nombre_participante2.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

        self.participante3 = util_img.leer_imagen("src/imagenes/participantes/david.png", (int(self.frame_width * 0.15), int(self.frame_height * 0.25)))
        self.label_participante3.configure(image=self.participante3)
        self.label_nombre_participante3.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

        self.participante4 = util_img.leer_imagen("src/imagenes/participantes/notkero.png", (int(self.frame_width * 0.15), int(self.frame_height * 0.25)))
        self.label_participante4.configure(image=self.participante4)
        self.label_nombre_participante4.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

        self.participante5 = util_img.leer_imagen("src/imagenes/participantes/jose.png", (int(self.frame_width * 0.15), int(self.frame_height * 0.25)))
        self.label_participante5.configure(image=self.participante5)
        self.label_nombre_participante5.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))