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

    def __init__(self, panel_principal, user_id, deshabilitar_botones, habilitar_botones):

        self.user_id = user_id
        self.frame_width = 0
        self.frame_height = 0
        self.deshabilitar_botones = deshabilitar_botones
        self.habilitar_botones = habilitar_botones

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
        self.label_titulo = tk.Label(self.frame_principal, text="Operaciones Clásicas", font=("Berlin Sans FB", 16, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_titulo.pack(pady=10, padx=10, anchor="center", side="top", fill="x")

        # Frame grid para las opciones
        self.frame_info = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_info.pack(padx=10, anchor="center", side="top", fill="x")

        # Contenedor para los botones
        contenedor_botones = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL)
        contenedor_botones.pack(side="bottom", anchor="e", pady=(0,20), padx=10, fill="x")

        # Boton de "Backtesting"
        self.boton_empezar_backtesting = tk.Button(contenedor_botones, text="Backtesting", font=("Aptos", 12, "bold"), bg="#2d367b", fg="white", command=self.backtesting)
        self.boton_empezar_backtesting.pack(side="right", padx=5)

        # Boton de "Inversión"
        self.boton_empezar_inversion = tk.Button(contenedor_botones, text="Inversión", font=("Aptos", 12, "bold"), bg="#2d367b", fg="white", command=self.invertir)
        self.boton_empezar_inversion.pack(side="right", padx=5)
        
        #RSI
        # Subtítulo para la opción de rsi
        self.label_RSI = tk.Label(self.frame_info, text="RSI + MACD", font=("Berlin Sans FB", 14, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_RSI.grid(row=0, column=0, columnspan=2, sticky="w")

        #frame para la descripción
        self.frame_descripcion_rsi = tk.Frame(self.frame_info, bg=COLOR_CUERPO_PRINCIPAL, width=200, height=100)
        self.frame_descripcion_rsi.grid(row=1, column=0, columnspan=3, sticky="nsew") 
        
        # Descripción de la opción de RSI
        self.descripcion_rsi = tk.Label(self.frame_descripcion_rsi, justify="left", text="Esta estrategia se basa en la combinación de dos indicadores bastante conocidos que son el índice de fuerza relativa y la divergencia/convergencia de la media móvil. Cuando el RSI se encuentra por debajo de ciertos niveles nos indica que la acción está sobrevendida y si está por encima de estos niveles nos indica que está sobrecomprada. El índice de convergencia-divergencia de la media móvil tiene dos componentes que son la línea MACD y la señal. Cuando la línea está por encima de la señal nos puede indicar una posible zona de compra y al contrario posible zona de venta. Mezclando estos indicadores obtenemos una estrategia bastante robusta.", wraplength=200, font=("Aptos", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.descripcion_rsi.pack(pady=2, padx=5, anchor="w", side="top", fill="x")
        
        #MediaMovil
        #subitulo para la opcion 
        self.label_MediaMovil = tk.Label(self.frame_info, text="Media Movil", font=("Berlin Sans FB", 14, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_MediaMovil.grid(row=2, column=0, columnspan=2, sticky="w")

        #frame para la descripción
        self.frame_descripcion_MediaMovil = tk.Frame(self.frame_info, bg=COLOR_CUERPO_PRINCIPAL, width=200, height=100)
        self.frame_descripcion_MediaMovil.grid(row=3, column=0, columnspan=3, sticky="nsew")

        # Descripción de la opción MediaMovil
        self.descripcion_MediaMovil = tk.Label(self.frame_descripcion_MediaMovil, justify="left", text="El cruce de medias móviles es una estrategia que se usa muy a menudo y que suele dar muy buenos resultados. En nuestro caso hemos optado por el cálculo de una media a corto plazo basada en un periodo de 30 datos, y por otro lado una media más a largo plazo basada en 60 datos. Cuando la media al largo plazo cruza de abajo arriba a la media al corto plazo nos indica un posible cambio a tendencia creciente y nos marca una zona de compra. Cuando se produce lo contrario nos indica una posible zona de venta", wraplength=200, font=("Aptos", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.descripcion_MediaMovil.pack(pady=2, padx=5, anchor="w", side="top", fill="x")

        #Bandas
        # Subtitulo para la opción de Bandas
        self.label_Bandas = tk.Label(self.frame_info, text="Bandas de Bollinger", font=("Berlin Sans FB", 14, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_Bandas.grid(row=4, column=0, columnspan=2, sticky="w")

        #frame para la descripción
        self.frame_descripcion_Bandas = tk.Frame(self.frame_info, bg=COLOR_CUERPO_PRINCIPAL, width=200, height=100)
        self.frame_descripcion_Bandas.grid(row=5, column=0, columnspan=3, sticky="nsew")
        
        # Descripción de la opción de Bandas
        self.descripcion_Bandas = tk.Label(self.frame_descripcion_Bandas, justify="left", text="Este indicador está formado por tres componentes que se basan en medias móviles. Tenemos la banda baja, la banda media y la banda alta. Para nuestra estrategia vamos a usar la banda alta y la banda baja. Vamos a hacer una comparación de las bandas con el precio actual de la acción. Cuando el precio de la acción se encuentra por debajo de la banda baja, nos indica que se encuentra en una zona fuera de lo normal y puede ser un buen punto de compra. Y cuando nuestro precio se encuentra por encima de la banda alta nos indica una zona de venta.", wraplength=200, font=("Aptos", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.descripcion_Bandas.pack(pady=2, padx=5, anchor="w", side="top", fill="x")

        #Estocastico
        # Subtitulo para la opción de Estocastico
        self.label_Estocastico = tk.Label(self.frame_info, text="Estocastico + RSI", font=("Berlin Sans FB", 14, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_Estocastico.grid(row=6, column=0, columnspan=2, sticky="w")

        #frame para la descripción
        self.frame_descripcion_Estocastico = tk.Frame(self.frame_info, bg=COLOR_CUERPO_PRINCIPAL, width=200, height=100)
        self.frame_descripcion_Estocastico.grid(row=7, column=0, columnspan=3, sticky="nsew")
        
        # Descripción de la opción de Estocastico
        self.descripcion_Estocastico = tk.Label(self.frame_descripcion_Estocastico, justify="left", text="La última estrategia se basa en el uso del índice de fuerza relativa y un nuevo indicador que es el estocástico basado en dos componentes que son la línea K y la línea D. Cuando combinamos lo que explicamos del RSI con anterioridad y ahora le sumamos que cuando la línea K esté por encima de la línea D se producirá una oportunidad de compra y cuando pase lo contrario se generará una señal de venta.", wraplength=200, font=("Aptos", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.descripcion_Estocastico.pack(pady=2, padx=5, anchor="w", side="top", fill="x")

        #Ajustar vista
        self.on_parent_configure(None)


    def backtesting(self):
        # Función para abrir el formulario de backtesting
        self.limpiar_panel(self.frame_principal)
        FormularioBackTestingClasicas(self.frame_principal, self.user_id)

    def invertir(self):
        # Función para abrir el formulario de inversión
        self.limpiar_panel(self.frame_principal)
        FormularioInversionClasicas(self.frame_principal, self.user_id, self.deshabilitar_botones, self.habilitar_botones)

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
        self.label_RSI.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.15), "bold"))
        self.label_MediaMovil.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.15), "bold"))
        self.label_Bandas.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.15), "bold"))
        self.label_Estocastico.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.15), "bold"))

        #Ajustar el tamaño del frame de descripción y el wraplength y el tamaño de la fuente
        self.frame_descripcion_rsi.config(width=self.frame_width-25)
        self.descripcion_rsi.config(wraplength=self.frame_width-25)
        self.descripcion_rsi.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.09)))

        self.frame_descripcion_MediaMovil.config(width=self.frame_width-25)
        self.descripcion_MediaMovil.config(wraplength=self.frame_width-25)
        self.descripcion_MediaMovil.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.09)))

        self.frame_descripcion_Bandas.config(width=self.frame_width-25)
        self.descripcion_Bandas.config(wraplength=self.frame_width-25)
        self.descripcion_Bandas.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.09)))

        self.frame_descripcion_Estocastico.config(width=self.frame_width-25)
        self.descripcion_Estocastico.config(wraplength=self.frame_width-25)
        self.descripcion_Estocastico.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.09)))

        #Ajustar el tamaño de los botones y la fuente de los botones
        self.boton_empezar_backtesting.configure(width=int(self.frame_width * 0.025))
        self.boton_empezar_inversion.configure(width=int(self.frame_width * 0.025))
        self.boton_empezar_backtesting.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
        self.boton_empezar_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
        


    def limpiar_panel(self,panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()