import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Entry, Text, Button, PhotoImage
from config2 import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
from formularios.formulario_backtesting_futbol import FormularioBackTestingFutbol
from formularios.formulario_backtesting_formula1 import FormularioBackTestingFormula1
from formularios.formulario_inversion_futbol import FormularioInversionFutbol
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


class FormularioBackTestingOpciones():

    def __init__(self, panel_principal):

        self.frame_width = 0
        self.frame_height = 0

        #Frame principal 
        self.frame_principal = tk.Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)


        self.opciones()

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)   

        #Llamada a la función on_parent_configure cuando se redimensiona la ventana
        panel_principal.bind("<Configure>", self.on_parent_configure)

    
    def obtener_dimensiones(self):
        print("Obteniendo dimensiones")
        self.frame_width = self.frame_principal.winfo_width() 
        self.frame_height = self.frame_principal.winfo_height()
        print("Ancho: ", self.frame_width)
        print("Alto: ", self.frame_height)



    def opciones(self):
        # Título arriba a la izquierda
        self.label_titulo = tk.Label(self.frame_principal, text="Elige la operación creativa que desees", font=("Berlin Sans FB", 16, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_titulo.pack(pady=10, padx=10, anchor="center", side="top", fill="x")

        # Frame grid para las opciones
        self.frame_opciones = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_opciones.pack(pady=10, padx=10, anchor="center", side="top", fill="x")
        
        #FUTBOL
        # Subtítulo para la opción de fútbol
        self.label_futbol = tk.Label(self.frame_opciones, text="Fútbol", font=("Berlin Sans FB", 14, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_futbol.grid(row=2, column=0, columnspan=2, sticky="w")

        # Boton de "Empezar backtesting"
        self.boton_empezar_backtesting_futbol = tk.Button(self.frame_opciones, text="Empezar Backtesting", font=("Aptos", 12), bg="green", fg="white", command=self.futbol) 
        self.boton_empezar_backtesting_futbol.grid(row=2, column=2, sticky="e")

        #boton para "Empezar inversión"
        self.boton_empezar_inversion_futbol = tk.Button(self.frame_opciones, text="Empezar Inversión", font=("Aptos", 12), bg="green", fg="white", command=self.invertirfutbol)
        self.boton_empezar_inversion_futbol.grid(row=2, column=1, sticky="e")

        #frame para la descripción
        self.frame_descripcion_futbol = tk.Frame(self.frame_opciones, bg=COLOR_CUERPO_PRINCIPAL, width=200, height=100)
        self.frame_descripcion_futbol.grid(row=3, column=0, columnspan=3, sticky="nsew") 
        
        # Descripción de la opción de fútbol
        self.descripcion_futbol = tk.Label(self.frame_descripcion_futbol, justify="left", text="La estrategia consiste en invertir en acciones de empresas asociadas a equipos de fútbol, basándose en el rendimiento deportivo de dichos equipos. Este enfoque implica tomar decisiones de compra y venta de acciones en función de los resultados y desempeño del equipo en el campo. Se busca capitalizar el éxito deportivo como un indicador potencial de oportunidades de inversión en el mercado financiero relacionadas con la industria del deporte.", wraplength=200, font=("Aptos", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.descripcion_futbol.pack(pady=10, padx=5, anchor="w", side="top", fill="x")
        
        #FORMULA 1
        #subitulo para la opcion formula 1
        self.label_formula1 = tk.Label(self.frame_opciones, text="Fórmula 1", font=("Berlin Sans FB", 14, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_formula1.grid(row=4, column=0, columnspan=2, sticky="w")

        # Boton de "Empezar backtesting"
        self.boton_empezar_backtesting_formula1 = tk.Button(self.frame_opciones, text="Empezar Backtesting", font=("Aptos", 12), bg="green", fg="white", command=self.formula1)
        self.boton_empezar_backtesting_formula1.grid(row=4, column=2, sticky="e")

        #frame para la descripción
        self.frame_descripcion_formula1 = tk.Frame(self.frame_opciones, bg=COLOR_CUERPO_PRINCIPAL, width=200, height=100)
        self.frame_descripcion_formula1.grid(row=5, column=0, columnspan=3, sticky="nsew")

        # Descripción de la opción de fórmula 1
        self.descripcion_formula1 = tk.Label(self.frame_descripcion_formula1, justify="left", text="La estrategia consiste en invertir en acciones de empresas asociadas a equipos de fórmula 1, basándose en el rendimiento deportivo de dichos equipos. Este enfoque implica tomar decisiones de compra y venta de acciones en función de los resultados y desempeño del equipo en el circuito. Se busca capitalizar el éxito deportivo como un indicador potencial de oportunidades de inversión en el mercado financiero relacionadas con la industria del deporte.", wraplength=200, font=("Aptos", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.descripcion_formula1.pack(pady=10, padx=5, anchor="w", side="top", fill="x")

        #CINE
        # Subtitulo para la opción de cine
        self.label_cine = tk.Label(self.frame_opciones, text="Cine", font=("Berlin Sans FB", 14, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_cine.grid(row=6, column=0, columnspan=2, sticky="w")

        # Boton de "Empezar backtesting"
        self.boton_empezar_backtesting_cine = tk.Button(self.frame_opciones, text="Empezar Backtesting", font=("Aptos", 12), bg="green", fg="white", command=self.cine)
        self.boton_empezar_backtesting_cine.grid(row=6, column=2, sticky="e")

        #frame para la descripción
        self.frame_descripcion_cine = tk.Frame(self.frame_opciones, bg=COLOR_CUERPO_PRINCIPAL, width=200, height=100)
        self.frame_descripcion_cine.grid(row=7, column=0, columnspan=3, sticky="nsew")
        
        # Descripción de la opción de cine
        self.descripcion_cine = tk.Label(self.frame_descripcion_cine, justify="left", text="La estrategia consiste en invertir en acciones de empresas asociadas a la industria del cine, basándose en el rendimiento de las películas y la taquilla. Este enfoque implica tomar decisiones de compra y venta de acciones en función de los resultados y desempeño de las películas en la taquilla. Se busca capitalizar el éxito de las películas como un indicador potencial de oportunidades de inversión en el mercado financiero relacionadas con la industria del cine.", wraplength=200, font=("Aptos", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.descripcion_cine.pack(pady=10, padx=5, anchor="w", side="top", fill="x")


    def futbol(self):
        self.limpiar_panel(self.frame_principal)     
        FormularioBackTestingFutbol(self.frame_principal)

    def invertirfutbol(self):
        self.limpiar_panel(self.frame_principal)
        FormularioInversionFutbol(self.frame_principal)

    def formula1(self):
        self.limpiar_panel(self.frame_principal)     
        FormularioBackTestingFormula1(self.frame_principal)

    def cine(self):
        pass


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

    def update(self):
        #Ajustar el tamaño del titulo
        self.label_titulo.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.25), "bold"))

        #Ajustar el tamaño de los subtitulos
        self.label_futbol.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.15), "bold"))
        self.label_formula1.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.15), "bold"))
        self.label_cine.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.15), "bold"))

        #Ajustar el tamaño del frame de descripción y el wraplength
        self.frame_descripcion_futbol.config(width=self.frame_width-25)
        self.descripcion_futbol.config(wraplength=self.frame_width-25)
        self.frame_descripcion_formula1.config(width=self.frame_width-25)
        self.descripcion_formula1.config(wraplength=self.frame_width-25)
        self.frame_descripcion_cine.config(width=self.frame_width-25)
        self.descripcion_cine.config(wraplength=self.frame_width-25)


    def limpiar_panel(self,panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()