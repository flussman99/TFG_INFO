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
from EquiposdeFutbol import SBS_backtesting as SBS
from tkcalendar import DateEntry
import matplotlib.dates as mdates
import tkinter as tk
from datetime import datetime, timedelta


class FormularioBackTestingCreativas():

    def __init__(self, panel_principal, user_id):

        self.user_id = user_id
        self.frame_width = 0
        self.frame_height = 0

        #Frame principal
        self.frame_principal = tk.Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Frame superior 
        self.frame_superior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_superior.pack(fill=tk.BOTH, expand=True)

        #Titulo frame superior
        self.label_titulo = tk.Label(self.frame_superior, text="Backtesting Operaciones Creativas", font=("Berlin Sans FB", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_titulo.place(relx=0.05, rely=0.1)

        # Frame inferior (con scrollbar)
        self.frame_inferior = tk.Frame(self.frame_principal, bg="lightgray")
        self.frame_inferior.pack(fill=tk.BOTH, expand=True)

        #ComboBoxs
        self.crear_combo_boxs()

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)   

        #Llamada a la función on_parent_configure cuando se redimensiona la ventana
        panel_principal.bind("<Configure>", self.on_parent_configure)

    def crear_combo_boxs(self):
        #Inicializar variables
        self.label_fecha_inicio = None
        self.label_fecha_fin = None
        self.fecha_inicio_entry = None
        self.fecha_fin_entry = None

        #Crear frame para añadir todo los combo boxs
        self.frame_combo_boxs = tk.Frame(self.frame_superior, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_combo_boxs.place(relx=0.05, rely=0.3)

        #Label de "Elige operación creativa"
        self.label_operacion_creativa = tk.Label(self.frame_combo_boxs, text="Elige operación creativa", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_operacion_creativa.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        #ComboBox de operaciones creativas
        self.combo_operaciones_creativas = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_operaciones_creativas.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        self.combo_operaciones_creativas["values"] = ["Fútbol", "Fórmula 1", "Películas", "Operacion 4", "Operacion 5"]

        #Opcion seleccionada
        self.opcion = self.combo_operaciones_creativas.get()

        #Evento de cambio de valor en el combobox
        self.combo_operaciones_creativas.bind("<<ComboboxSelected>>", self.actualizar_vista_opcion)

    def actualizar_vista_opcion(self, event):
        self.opcion = self.combo_operaciones_creativas.get()
        print("---------------------")
        if self.opcion == "Fútbol":
            print("Fútbol")
            self.operacion_futbol()
        elif self.opcion == "Fórmula 1":
            self.operacion_formula1()
        elif self.opcion == "Películas":
            self.operacion_peliculas()
        
        self.on_parent_configure(event)

    def operacion_futbol(self):
        #Inicializar variables
        self.ligas=SBS.ligas
        self.acciones=SBS.acciones
        self.pais=SBS.pais
        self.url=SBS.urls_equipos
        self.acronimos_acciones=SBS.acronimo_acciones
        self.imagenes_liga=SBS.imagenes_ligas
        self.imagenes_equipos=SBS.imagenes_equipos


        #Inicializar Labels
        self.label_liga = None
        self.label_equipo = None
        self.label_accion = None
        self.label_metodo_comprar = None
        self.label_metodo_vender = None

        #Inicializar ComboBoxs
        self.combo_ligas = None
        self.combo_equipos = None
        self.combo_accion = None
        self.combo_metodos_comprar = None
        self.combo_metodos_vender = None

        #Inicializar imagenes
        self.imagen_liga = None
        self.imagen_equipo = None
        self.imagen_accion = None

        #label de "Elige la liga"
        self.label_liga = tk.Label(self.frame_combo_boxs, text="Elige la liga", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_liga.grid(row=0, column=1, padx=10, pady=2, sticky="w")

        #ComboBox de ligas
        self.combo_ligas = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_ligas.grid(row=1, column=1, padx=10, pady=2, sticky="w")
        self.combo_ligas["values"] = list(self.ligas.keys())

        #Actualizar vista al cambiar de liga
        self.combo_ligas.bind("<<ComboboxSelected>>", self.actualizar_futbol_equipo)

    def actualizar_futbol_equipo(self, event):
        #Coger la liga seleccionada
        self.liga = self.combo_ligas.get()

        #Poner todo vacio si ya se ha seleccionado algo
        if self.combo_equipos is not None:
            if self.combo_equipos == "":
                self.label_imagen_equipo.destroy()
            self.label_equipo.destroy()
            self.combo_equipos.destroy()
            self.label_imagen_liga.destroy()
            self.label_equipo = None
            self.combo_equipos = None
            if self.combo_accion is not None:
                self.label_imagen_equipo.destroy()
                self.label_accion.destroy()
                self.combo_accion.destroy()
                self.label_accion = None
                self.combo_accion = None

        #Poner imagen de la liga
        self.imagen_liga = util_img.leer_imagen(self.imagenes_liga[self.liga], (10,10))
        self.label_imagen_liga = tk.Label(self.frame_superior, image=self.imagen_liga, bg=COLOR_CUERPO_PRINCIPAL)
        self.label_imagen_liga.place(relx=0.8, rely=0.1)

        #Label de "Elige el equipo"
        self.label_equipo = tk.Label(self.frame_combo_boxs, text="Elige el equipo", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_equipo.grid(row=0, column=2, padx=10, pady=2, sticky="w")

        #ComboBox de equipos
        self.combo_equipos = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_equipos.grid(row=1, column=2, padx=10, pady=2, sticky="w")
        self.combo_equipos["values"] = self.ligas[self.liga]

        #Actualizar vista al cambiar de equipo        
        self.combo_equipos.bind("<<ComboboxSelected>>", self.actualizar_futbol_accion)

        #Ajustar vista
        self.on_parent_configure(event)

    def actualizar_futbol_accion(self, event):
        #Coger el equipo seleccionado
        self.equipo = self.combo_equipos.get()
        #self.label_imagen_equipo.destroy()

        #Poner todo vacio si ya se ha seleccionado algo
        if self.combo_accion is not None:
            self.label_accion.destroy()
            self.combo_accion.destroy()
            self.label_accion = None
            self.combo_accion = None

        #Poner imagen del equipo
        self.imagen_equipo = util_img.leer_imagen(self.imagenes_equipos[self.equipo], (10,10))
        self.label_imagen_equipo = tk.Label(self.frame_superior, image=self.imagen_equipo, bg=COLOR_CUERPO_PRINCIPAL)
        self.label_imagen_equipo.place(relx=0.9, rely=0.1)
        
        #Label de "Elige acción"
        self.label_accion = tk.Label(self.frame_combo_boxs, text="Elige acción", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_accion.grid(row=0, column=3, padx=10, pady=2, sticky="w")

        #ComboBox de acciones
        self.combo_accion = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_accion.grid(row=1, column=3, padx=10, pady=2, sticky="w")
        self.combo_accion["values"] = self.acciones[self.equipo]
        
        #Actualizar vista al cambiar de accion        
        self.combo_accion.bind("<<ComboboxSelected>>", self.actualizar_futbol_metodos)

        #Ajustar vista
        self.on_parent_configure(event)

    def actualizar_futbol_metodos(self, event):
        #Coger la accion seleccionada
        self.accion = self.combo_accion.get()

        #Poner todo vacio si ya se ha seleccionado algo
        

        #Label de "Elige cuando comprar"
        self.label_metodo_comprar = tk.Label(self.frame_combo_boxs, text="Elige cuando comprar", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_metodo_comprar.grid(row=2, column=0, padx=10, pady=2, sticky="w")

        #ComboBox de metodos comprar
        self.combo_metodos_comprar = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_metodos_comprar.grid(row=3, column=0, padx=10, pady=2, sticky="w")
        self.combo_metodos_comprar["values"] = ["Ganado", "Perdido", "Empate", "Ganado o Empate", "Perdido o Empate", "Ganado o Perdido"]

        #label de "Elige cuando vender"
        self.label_metodo_vender = tk.Label(self.frame_combo_boxs, text="Elige cuando vender", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_metodo_vender.grid(row=2, column=1, padx=10, pady=2, sticky="w")

        #ComboBox de metodos vender
        self.combo_metodos_vender = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_metodos_vender.grid(row=3, column=1, padx=10, pady=2, sticky="w")
        self.combo_metodos_vender["values"] = ["Ganado", "Perdido", "Empate", "Ganado o Empate", "Perdido o Empate", "Ganado o Perdido"]

        #Cuando o comprar o vender tenga un valor seleccionado quitar esa opcion del otro
        self.combo_metodos_comprar.bind("<<ComboboxSelected>>", self.actualizar_futbol_metodos_vender)
        self.combo_metodos_vender.bind("<<ComboboxSelected>>", self.actualizar_futbol_metodos_comprar)

        #Ajustar vista
        self.on_parent_configure(event)

    def actualizar_futbol_metodos_comprar(self, event):
        #Coger el metodo de vender seleccionado
        self.metodo_vender = self.combo_metodos_vender.get()

        #Quitar el metodo de vender seleccionado del metodo de comprar
        self.combo_metodos_comprar["values"] = [x for x in ["Ganado", "Perdido", "Empate", "Ganado o Empate", "Perdido o Empate", "Ganado o Perdido"] if x != self.metodo_vender]

        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.combo_metodos_comprar.get() != "" and self.combo_metodos_vender.get() != "":
            self.actualizar_futbol_ticks()

        #Actualizar vista
        self.on_parent_configure(event)

    def actualizar_futbol_metodos_vender(self, event):
        #Coger el metodo de comprar seleccionado
        self.metodo_comprar = self.combo_metodos_comprar.get()

        #Quitar el metodo de comprar seleccionado del metodo de vender
        self.combo_metodos_vender["values"] = [x for x in ["Ganado", "Perdido", "Empate", "Ganado o Empate", "Perdido o Empate", "Ganado o Perdido"] if x != self.metodo_comprar]

        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.combo_metodos_comprar.get() != "" and self.combo_metodos_vender.get() != "":
            self.actualizar_futbol_ticks()

        #Actualizar vista
        self.on_parent_configure(event)

    def actualizar_futbol_ticks(self):
        #Coger el metodo de comprar y vender seleccionado
        self.metodo_comprar = self.combo_metodos_comprar.get()
        self.metodo_vender = self.combo_metodos_vender.get()

        #Label fecha inicio
        self.label_fecha_inicio = tk.Label(self.frame_combo_boxs, text="Fecha inicio", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_fecha_inicio.grid(row=4, column=0, padx=10, pady=2, sticky="w")

        #label fecha fin
        self.label_fecha_fin = tk.Label(self.frame_combo_boxs, text="Fecha fin", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_fecha_fin.grid(row=4, column=1, padx=10, pady=2, sticky="w")

        #Date fecha inicio
        fecha_ayer = datetime.now() - timedelta(days = 1)
        self.fecha_inicio_entry = DateEntry(
            self.frame_combo_boxs, 
            date_pattern='yyyy/mm/dd',
            background='darkblue', 
            foreground='white', 
            borderwidth=2,
            maxdate=fecha_ayer
        )
        self.fecha_inicio_entry.grid(row=5, column=0, padx=10, pady=2, sticky="w")

        #Date fecha fin
        self.fecha_fin_entry = DateEntry(
            self.frame_combo_boxs,
            date_pattern='yyyy/mm/dd',
            background='darkblue',
            foreground='white',
            borderwidth=2,
            maxdate=fecha_ayer
        )
        self.fecha_fin_entry.grid(row=5, column=1, padx=10, pady=2, sticky="w")

        # Boton de "Empezar backtesting"
        self.boton_empezar_backtesting = tk.Button(self.frame_combo_boxs, text="Empezar\nbacktesting", font=("Aptos", 12), bg="green", fg="white", command=self.empezar_backtesting) # wraplength determina el ancho máximo antes de que el texto se divida en dos líneas
        self.boton_empezar_backtesting.grid(row=4, column=2, rowspan=2, padx=10, pady=2, sticky="w")

        # Boton de "Empezar backtesting"
        self.boton_guardar_backtesting = tk.Button(self.frame_combo_boxs, text="Guardar\nbacktesting", font=("Aptos", 12), bg="green", fg="white", command=self.empezar_backtesting) # wraplength determina el ancho máximo antes de que el texto se divida en dos líneas
        self.boton_guardar_backtesting.grid(row=4, column=3, rowspan=2, padx=10, pady=2, sticky="w")

    def empezar_backtesting(self):
        pass

    def guardar_backtesting(self):
        pass

    def operacion_formula1(self):
        pass

    def operacion_peliculas(self):
        pass


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
        #Ajustar el tamaño del titulo
        self.label_titulo.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.2), "bold"))
        
        #Ajustar label elegir operacion creativa
        self.label_operacion_creativa.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

        #Ajustar with combobox
        self.combo_operaciones_creativas.configure(width=int(self.frame_width * 0.02))

        #Ajustar info ticks
        if self.label_fecha_inicio is not None:
            self.label_fecha_inicio.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.label_fecha_fin.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.fecha_inicio_entry.configure(width=int(self.frame_width * 0.02))
            self.fecha_fin_entry.configure(width=int(self.frame_width * 0.02))
            #Ajustar botones tanto el tamaño como el texto
            self.boton_empezar_backtesting.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_guardar_backtesting.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_empezar_backtesting.configure(width=int(self.frame_width * 0.015))
            self.boton_guardar_backtesting.configure(width=int(self.frame_width * 0.015))
        
        #Ajustar label elegir liga
        if self.opcion == "Fútbol":
            print ("Fútbollll")
            print ("----------------------------------------")
            #Ajustar liga
            self.label_liga.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.combo_ligas.configure(width=int(self.frame_width * 0.02))
            
            if self.combo_ligas is not None and self.combo_ligas.get() != "":
                print ("No hay liga seleccionada")
                print ("----------------------------------------")
                self.imagen_liga = util_img.leer_imagen(self.imagenes_liga[self.liga], (int(self.frame_width * 0.05), int(self.frame_width * 0.05)))
                self.label_imagen_liga.configure(image=self.imagen_liga)

            #Ajustar equipo
            if self.combo_equipos is not None:
                self.label_equipo.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                self.combo_equipos.configure(width=int(self.frame_width * 0.02))

                if self.combo_equipos.get() != "":
                    self.imagen_equipo = util_img.leer_imagen(self.imagenes_equipos[self.equipo], (int(self.frame_width * 0.05), int(self.frame_width * 0.05)))
                    self.label_imagen_equipo.configure(image=self.imagen_equipo)

                #Ajustar accion
                if self.combo_accion is not None:
                    self.label_accion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                    self.combo_accion.configure(width=int(self.frame_width * 0.02))

                    #Ajustar metodo comprar
                    if self.combo_metodos_comprar is not None:
                        self.label_metodo_comprar.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.combo_metodos_comprar.configure(width=int(self.frame_width * 0.02))

                    #Ajustar metodo vender
                    if self.combo_metodos_vender is not None:
                        self.label_metodo_vender.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.combo_metodos_vender.configure(width=int(self.frame_width * 0.02))

        elif self.opcion == "Fórmula 1":
            pass
        elif self.opcion == "Películas":
            pass

        
