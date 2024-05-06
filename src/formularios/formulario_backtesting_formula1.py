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
from Formula1 import SF1_backtesting as SF1
from tkcalendar import DateEntry
import matplotlib.dates as mdates
import tkinter as tk
from datetime import datetime, timedelta
from formularios.formulario_backtesting_mas_informacion import FormularioBackTestingMasInformacion


class FormularioBackTestingFormula1():

    def __init__(self, panel_principal):

        self.b = bt(1)

        self.frame_width = 0
        self.frame_height = 0

        #Frame principal
        self.frame_principal = tk.Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Frame superior 
        self.frame_superior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL, width=399, height=276)
        self.frame_superior.pack(fill=tk.BOTH)

        #Titulo frame superior
        self.label_titulo_formula1 = tk.Label(self.frame_superior, text="Backtesting Operaciones Fórmula 1", font=("Berlin Sans FB", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_titulo_formula1.place(relx=0.05, rely=0.1)

        # Frame inferior (con scrollbar)
        self.frame_inferior = tk.Frame(self.frame_principal, bg="lightgray", width=399, height=276)
        self.frame_inferior.pack(fill=tk.BOTH)

        #VARIABLES
        #Inicializar Labels
        self.label_ano = None
        self.label_piloto = None
        self.label_accion = None
        self.label_metodo_comprar = None
        self.label_metodo_vender = None

        #Inicializar ComboBoxs
        self.combo_anos = None
        self.combo_pilotos = None
        self.combo_acciones = None
        self.combo_metodos_comprar = None
        self.combo_metodos_vender = None

        #Inicializar imagenes
        self.imagen_piloto = None

        #Inicializar variables
        self.label_fecha_inicio = None
        self.label_fecha_fin = None
        self.fecha_inicio_entry = None
        self.fecha_fin_entry = None

        #Variables SBS
        self.acciones=SF1.acciones_escuderias
        self.standing=SF1.html_standings_files
        self.calendar=SF1.html_calendars_files
        self.pilotosTeams=SF1.html_pilotTeams_files
        self.imagenes_pilotos=SF1.imagenes_pilotos
        self.imagenes_escuderias=SF1.imagenes_escuderias

        #Variables de la tabla
        self.frame_without_filter=None
        self.current_frame = None
        self.frame_with_filter=None
        self.frame_directo=None
        self.tree = None

        #Botones
        self.boton_empezar_backtesting = None
        self.boton_mostrar_operaciones = None
        self.boton_guardar_backtesting = None


        #ComboBoxs
        self.operacion_formula1()

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)   

        #Llamada a la función on_parent_configure cuando se redimensiona la ventana
        panel_principal.bind("<Configure>", self.on_parent_configure)

    def operacion_formula1(self):

        #Crear frame para añadir todo los combo boxs
        self.frame_combo_boxs = tk.Frame(self.frame_superior, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_combo_boxs.place(relx=0.05, rely=0.3)

        #Label de "Elige el año"
        self.label_ano = tk.Label(self.frame_combo_boxs, text="Elige el año", font=("Aptos", 15, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_ano.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        #ComboBox de años
        self.combo_anos = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_anos.grid(row=1, column=0, padx=10, pady=2, sticky="w")

        #Añadir años a la lista
        self.anos = SF1.obtener_listado_años()
        self.combo_anos["values"] = list(self.anos)

        #Al seleccionar un año se actualizan los pilotos
        self.combo_anos.bind("<<ComboboxSelected>>", self.actualizar_formula1_pilotos)
        
        #Actualizar vista al cambiar de accion        
        #self.combo_accion.bind("<<ComboboxSelected>>", self.actualizar_futbol_metodos)

        #Ajustar vista
        self.on_parent_configure(None)

    def actualizar_formula1_pilotos(self, event):
        #Poner todo vacio si ya se ha seleccionado algo

        #Label de "Elige el piloto"
        self.label_piloto = tk.Label(self.frame_combo_boxs, text="Elige el piloto", font=("Aptos", 15, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_piloto.grid(row=0, column=1, padx=10, pady=2, sticky="w")

        #ComboBox de pilotos
        self.combo_pilotos = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_pilotos.grid(row=1, column=1, padx=10, pady=2, sticky="w")

        #Añadir pilotos a la lista
        self.pilotos = SF1.obtener_listado_pilotos(self.combo_anos.get())
        self.combo_pilotos["values"] = list(self.pilotos)

        #Al seleccionar un piloto se actualiza la imagen
        self.combo_pilotos.bind("<<ComboboxSelected>>", self.actualizar_formula1_imagen_piloto)

        #Actualizar vista
        self.on_parent_configure(event)


    def actualizar_formula1_imagen_piloto(self, event):
        #Coger el año seleccionado
        self.ano = self.combo_anos.get()
        #Coger el piloto seleccionado
        self.piloto = self.combo_pilotos.get()

        #escuderia e imagen
        #self.escuderia=SF1.obtener_escuderia_piloto(self.piloto, self.ano)
        #self.imagen_escuderia = util_img.leer_imagen(self.acciones[self.escuderia], (100,100))
        #self.label_imagen_escuderia = tk.Label(self.frame_superior, image=self.imagen_escuderia, bg=COLOR_CUERPO_PRINCIPAL)
        #self.label_imagen_escuderia.place(relx=0.6, rely=0.1)

        #Poner imagen del piloto
        self.imagen_piloto = util_img.leer_imagen(self.imagenes_pilotos[self.piloto], (100,100))
        self.label_imagen_piloto = tk.Label(self.frame_superior, image=self.imagen_piloto, bg=COLOR_CUERPO_PRINCIPAL)
        self.label_imagen_piloto.place(relx=0.8, rely=0.1)

        #Label de accion
        self.label_accion = tk.Label(self.frame_combo_boxs, text="La acción selecionada es: " + SF1.obtener_accion_escuderia(self.piloto, self.ano), font=("Aptos", 15, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_accion.grid(row=2, column=0, columnspan=2, padx=10, pady=2, sticky="w")

        #continuar
        self.actualizar_formula1_metodos(None)



    def actualizar_formula1_metodos(self, event):
        #Poner todo vacio si ya se ha seleccionado algo
        
        #Label de "Elige cuando comprar"
        self.label_metodo_comprar = tk.Label(self.frame_combo_boxs, text="Elige cuando comprar", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_metodo_comprar.grid(row=3, column=0, padx=10, pady=2, sticky="w")

        #ComboBox de metodos comprar
        self.combo_metodos_comprar = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_metodos_comprar.grid(row=4, column=0, padx=10, pady=2, sticky="w")
        self.combo_metodos_comprar["values"] = ["Top 1", "Top 3", "Top 5", "Top 10", "No puntúa"]

        #label de "Elige cuando vender"
        self.label_metodo_vender = tk.Label(self.frame_combo_boxs, text="Elige cuando vender", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_metodo_vender.grid(row=3, column=1, padx=10, pady=2, sticky="w")

        #ComboBox de metodos vender
        self.combo_metodos_vender = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_metodos_vender.grid(row=4, column=1, padx=10, pady=2, sticky="w")
        self.combo_metodos_vender["values"] = ["Top 1", "Top 3", "Top 5", "Top 10", "No puntúa"]

        #Cuando o comprar o vender tenga un valor seleccionado quitar esa opcion del otro
        self.combo_metodos_comprar.bind("<<ComboboxSelected>>", self.actualizar_formula1_metodos_vender)
        self.combo_metodos_vender.bind("<<ComboboxSelected>>", self.actualizar_formula1_metodos_comprar)

        #Ajustar vista
        self.on_parent_configure(event)

    def actualizar_formula1_metodos_comprar(self, event):
        #Coger el metodo de vender seleccionado
        self.metodo_vender = self.combo_metodos_vender.get()
        
        #Quitar la opcion seleccionada en comprar del metodo vender
        if self.metodo_vender == "Top 1":
            self.combo_metodos_comprar["values"] = ["Top 3", "Top 5", "Top 10", "No puntúa"]
        elif self.metodo_vender == "Top 3":
            self.combo_metodos_comprar["values"] = ["Top 1", "Top 5", "Top 10", "No puntúa"]
        elif self.metodo_vender == "Top 5":
            self.combo_metodos_comprar["values"] = ["Top 1", "Top 3", "Top 10", "No puntúa"]
        elif self.metodo_vender == "Top 10":
            self.combo_metodos_comprar["values"] = ["Top 1", "Top 3", "Top 5", "No puntúa"]
        elif self.metodo_vender == "No puntúa":
            self.combo_metodos_comprar["values"] = ["Top 1", "Top 3", "Top 5", "Top 10"]
                
       
        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.combo_metodos_comprar.get() != "" and self.combo_metodos_vender.get() != "":
            self.actualizar_futbol_ticks()

        #Actualizar vista
        self.on_parent_configure(event)

    def actualizar_formula1_metodos_vender(self, event):
        #Coger el metodo de comprar seleccionado
        self.metodo_comprar = self.combo_metodos_comprar.get()

        #Quitar opciones dependiendo de lo que se eliga en comprar, opciones especiales en cada caso 
        if self.metodo_comprar == "Top 1":
            self.combo_metodos_vender["values"] = ["Top 3", "Top 5", "Top 10", "No puntúa"]
        elif self.metodo_comprar == "Top 3":
            self.combo_metodos_vender["values"] = ["Top 1", "Top 5", "Top 10", "No puntúa"]
        elif self.metodo_comprar == "Top 5":
            self.combo_metodos_vender["values"] = ["Top 1", "Top 3", "Top 10", "No puntúa"]
        elif self.metodo_comprar == "Top 10":
            self.combo_metodos_vender["values"] = ["Top 1", "Top 3", "Top 5", "No puntúa"]
        elif self.metodo_comprar == "No puntúa":
            self.combo_metodos_vender["values"] = ["Top 1", "Top 3", "Top 5", "Top 10"]
                
        
        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.combo_metodos_comprar.get() != "" and self.combo_metodos_vender.get() != "":
            self.actualizar_futbol_ticks()

        #Actualizar vista
        self.on_parent_configure(event)


    def guardar_backtesting(self):
        pass

    def mas_informacion(self):
        self.limpiar_panel(self.frame_principal)     
        FormularioBackTestingMasInformacion(self.frame_principal, self.frame_without_filter, "Futbol", self.rentabilidad_futbol.get())

    def limpiar_panel(self,panel):
        # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()


    def obtener_dimensiones(self):
        print("Obteniendo dimensiones")
        self.frame_width = self.frame_principal.winfo_width() 
        self.frame_height = self.frame_principal.winfo_height()
        print("Ancho: ", self.frame_width)
        print("Alto: ", self.frame_height)

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

        #Ajustas el tamaño de los frames
        self.frame_superior.configure(width=self.frame_width, height=self.frame_height*0.5)
        self.frame_inferior.configure(width=self.frame_width, height=self.frame_height*0.5)

        #Ajustar el tamaño del titulo
        self.label_titulo_formula1.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.2), "bold"))

       