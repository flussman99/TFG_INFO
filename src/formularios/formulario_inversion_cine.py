import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, Canvas, Entry, Text, Button, PhotoImage
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
from Disney import Dis_backtesting as Disney
from tkcalendar import DateEntry
import matplotlib.dates as mdates
import tkinter as tk
from datetime import datetime, timedelta


class FormularioInversionCine():

    def __init__(self, panel_principal, id_user):

        self.b = bt(1)
        self.id_user = id_user

        self.frame_width = 0
        self.frame_height = 0

        #Frame principal
        self.frame_principal = tk.Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Frame superior 
        self.frame_superior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL, width=399, height=276)
        self.frame_superior.pack(fill=tk.BOTH)

        #Titulo frame superior
        self.label_titulo_futbol = tk.Label(self.frame_superior, text="Inversión de Operaciones de Cine", font=("Berlin Sans FB", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_titulo_futbol.place(relx=0.05, rely=0.1)

        # Frame inferior (con scrollbar)
        self.frame_inferior = tk.Frame(self.frame_principal, bg="lightgray", width=399, height=276)
        self.frame_inferior.pack(fill=tk.BOTH)

        #VARIABLES
        #Inicializar Labels
        self.label_disney = None
        self.label_accion = None
        self.label_estudio = None
        self.label_metodo_comprar = None
        self.label_comparativa = None

        self.label_rentabilidad = None
        self.label_rentabilidad_futbol = None
        self.label_rentabilidad_comparativa = None
        self.label_rentabilidad_comparativa_texto = None

        #Inicializar ComboBoxs
        self.combo_estudios = None
        self.combo_metodos_comprar = None
        self.combo_comparativa = None

        #Inicializar imagenes
        self.imagen_disney = None
        self.label_imagen_disney = None
        self.imagen_estudio = None
        self.label_imagen_estudio = None

        #Inicializar variables
        self.label_fecha_inicio = None
        self.label_fecha_fin = None
        self.fecha_inicio_entry = None
        self.fecha_fin_entry = None

        #Variables SBS
        self.estudios = Disney.estudios_Disney
        self.imagenes_estudios = Disney.imagenes_estudios

        #Variables de la tabla
        self.frame_without_filter=None
        self.current_frame = None
        self.frame_with_filter=None
        self.frame_directo=None
        self.tree = None

        #Botones
        self.boton_empezar_inversion = None
        self.boton_parar_inversion = None


        #ComboBoxs
        self.crear_combo_boxs()

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)   

        #Llamada a la función on_parent_configure cuando se redimensiona la ventana
        panel_principal.bind("<Configure>", self.on_parent_configure)

    def crear_combo_boxs(self):

        #Crear frame para añadir todo los combo boxs
        self.frame_combo_boxs = tk.Frame(self.frame_superior, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_combo_boxs.place(relx=0.05, rely=0.3)

        #seguir
        self.operacion_futbol()

    def operacion_futbol(self):
        #label de Disney
        self.label_disney = tk.Label(self.frame_combo_boxs, text="Acción de Disney:", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_disney.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        #label accion de disney
        self.label_accion = tk.Label(self.frame_combo_boxs, text="NYSE:DIS", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_accion.grid(row=1, column=0, padx=10, pady=2, sticky="w")

        #label de "Elige el estudio:"
        self.label_estudio = tk.Label(self.frame_combo_boxs, text="Elige el estudio:", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_estudio.grid(row=0, column=1, padx=10, pady=2, sticky="w")

        #ComboBox de estudios
        self.combo_estudios = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_estudios.grid(row=1, column=1, columnspan=2, padx=10, pady=2, sticky="w")
        #ordenar los valores alfabeticamente
        self.estudios.sort()
        self.combo_estudios["values"] = self.estudios
        

        #Cargar imagen disney
        self.imagen_disney = util_img.leer_imagen("src/imagenes/Disney/disney.jpg", (10,10))
        self.label_imagen_disney = tk.Label(self.frame_superior, image=self.imagen_disney, bg=COLOR_CUERPO_PRINCIPAL)
        self.label_imagen_disney.place(relx=0.8, rely=0.1)

        #Ajustar vista
        self.on_parent_configure(None)

        #Actualizar vista al cambiar de liga
        self.combo_estudios.bind("<<ComboboxSelected>>", self.actualizar_estudio)

    def actualizar_estudio(self, event):
        #Coger el estudio seleccionado
        self.estudio = self.combo_estudios.get()

        #Poner a none todo
        self.label_imagen_estudio = None

        #Cargar imagen estudio
        self.imagen_estudio = util_img.leer_imagen(self.imagenes_estudios[self.estudio], (10,10))
        self.label_imagen_estudio = tk.Label(self.frame_superior, image=self.imagen_estudio, bg=COLOR_CUERPO_PRINCIPAL)
        self.label_imagen_estudio.place(relx=0.9, rely=0.1)

        #Ajustar vista
        self.on_parent_configure(event)

        #Actualizar vista
        self.actualizar_metodos()

    def actualizar_metodos(self):
        if self.label_metodo_comprar is None:
            #Label de "Elige cuando comprar"
            self.label_metodo_comprar = tk.Label(self.frame_combo_boxs, text="Elige cuando comprar", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_metodo_comprar.grid(row=2, column=0, padx=10, pady=2, sticky="w")

            #ComboBox de metodos comprar
            self.combo_metodos_comprar = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_metodos_comprar.grid(row=3, column=0, padx=10, pady=2, sticky="w")
            self.combo_metodos_comprar["values"] = ["Mayor a", "Menor a", "Igual a"]

            #Actualizar al seleccionar algo
            self.combo_metodos_comprar.bind("<<ComboboxSelected>>", self.actualizar_comparativa)
        
        #Actualizar vista
        self.on_parent_configure(None)

    def actualizar_comparativa(self, event):
        if self.label_comparativa is None:
            
            #Label de "Comparativa"
            self.label_comparativa = tk.Label(self.frame_combo_boxs, text="Comparativa", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_comparativa.grid(row=2, column=1, padx=10, pady=2, sticky="w")

            #ComboBox de comparativa
            self.combo_comparativa = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_comparativa.grid(row=3, column=1, padx=10, pady=2, sticky="w")
            self.combo_comparativa["values"] = ['SP500', 'IBEX35', 'Plazo Fijo']

        #al mirar todos los datos actualizar el boton
        self.combo_comparativa.bind("<<ComboboxSelected>>", self.actualizar_futbol_ticks)

        #Ajustar vista
        self.on_parent_configure(None)

    def actualizar_futbol_ticks(self, event):

        if (self.fecha_inicio_entry is None):
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
        self.boton_empezar_inversion = tk.Button(self.frame_combo_boxs, text="Empezar\nbacktesting", font=("Aptos", 12), bg="green", fg="white", command=self.empezar_inversion) # wraplength determina el ancho máximo antes de que el texto se divida en dos líneas
        self.boton_empezar_inversion.grid(row=4, column=3, rowspan=2, padx=10, pady=2, sticky="w")

        #Actualizar vista
        self.on_parent_configure(None)

    def crear_interfaz_inferior(self):
        # Frame para mostrar los datos
        self.frame_datos = tk.Frame(self.frame_inferior, bg=COLOR_CUERPO_PRINCIPAL, width=399)
        self.frame_datos.pack(fill=tk.BOTH, expand=True)

        # Label de "Rentabilidad"
        self.label_rentabilidad = tk.Label(self.frame_datos, text="Rentabilidad", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad.pack(side="left", padx=(10, 0), pady=5)

        # Rentabilidad
        self.rentabilidad_futbol = tk.StringVar()
        self.rentabilidad_futbol.set("0")
        self.label_rentabilidad_futbol = tk.Label(self.frame_datos, textvariable=self.rentabilidad_futbol, font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_futbol.pack(side="left", padx=(0, 10), pady=5)

        #Label rentabalidad comparativa
        self.label_rentabilidad_comparativa_texto = tk.Label(self.frame_datos, text="Rentabilidad Indicador " , font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_comparativa_texto.pack(side="left", padx=(10, 0), pady=5)

        # Rentabilidad comparativa 
        self.rentabilidad_comparativa = tk.StringVar()
        self.rentabilidad_comparativa.set("0")
        self.label_rentabilidad_comparativa = tk.Label(self.frame_datos, textvariable=self.rentabilidad_comparativa, font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_comparativa.pack(side="left", padx=(0, 10), pady=5)

        # Boton de "Parar Inversion"
        self.boton_parar_inversion = tk.Button(self.frame_datos, text="Parar\ninversión", font=("Aptos", 12), bg="green", fg="white", command=self.toggle_frames) 
        self.boton_parar_inversion.pack(side="right", padx=(0, 10), pady=5)


        #Crear un widget Treeview
        self.tree = ttk.Treeview(self.frame_inferior)
        self.tree.pack(side="left", fill="x", expand=True)

        #Actualizar vista
        self.on_parent_configure(None)

    def empezar_inversion(self):
        #Verifiar que se han seleccionado todos los campos
        if self.combo_estudios.get() == "" or self.combo_metodos_comprar.get() == "" or self.combo_comparativa.get() == "":
            messagebox.showerror("Error", "Debes seleccionar todos los campos.")
            return
        
        # Verificar que las fechas de inicio y fin no son la misma fecha
        if self.fecha_inicio_entry.get() == self.fecha_fin_entry.get():
            messagebox.showerror("Error", "La fecha de inicio y fin no pueden ser la misma.")
            return

        # Verificar si la interfaz de usuario ya ha sido creada
        if not hasattr(self, 'frame_datos'):
            # Si no ha sido creada, entonces crearla
            self.crear_interfaz_inferior()
        else:
            # Si ya ha sido creada, limpiar el Treeview
            if self.tree is not None:
                for item in self.tree.get_children():
                    self.tree.delete(item)

        # Llamar a la función para obtener nuevos datos
        #self.coger_ticks()



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
        self.label_titulo_futbol.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.2), "bold"))

        #Ajustar info ticks
        if self.label_fecha_inicio is not None:
            self.label_fecha_inicio.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.label_fecha_fin.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.fecha_inicio_entry.configure(width=int(self.frame_width * 0.02))
            self.fecha_fin_entry.configure(width=int(self.frame_width * 0.02))
            #Ajustar botones tanto el tamaño como el texto
            self.boton_empezar_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_empezar_inversion.configure(width=int(self.frame_width * 0.015))

        if self.boton_parar_inversion is not None:
            self.boton_parar_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_parar_inversion.configure(width=int(self.frame_width * 0.015))
        
        #Ajustar rentabilidad
        if self.label_rentabilidad is not None:
            self.label_rentabilidad.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
            self.label_rentabilidad_futbol.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
            self.label_rentabilidad_comparativa_texto.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
            self.label_rentabilidad_comparativa.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
            

        #Ajustar label elegir liga
        if self.label_disney is not None:
            #Ajustar liga
            self.label_disney.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.label_accion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

            if self.frame_width > 10 and self.frame_height > 10:
                self.imagen_disney = util_img.leer_imagen("src/imagenes/Disney/disney.jpg", (int(self.frame_width * 0.08), int(self.frame_width * 0.08)))
                self.label_imagen_disney.configure(image=self.imagen_disney)

            #Ajustar estudio
            if self.combo_estudios is not None:
                self.label_estudio.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                self.combo_estudios.configure(width=int(self.frame_width * 0.02))

                if self.combo_estudios.get() != "":
         
                    self.imagen_estudio = util_img.leer_imagen(self.imagenes_estudios[self.estudio], (int(self.frame_width * 0.08), int(self.frame_width * 0.08)))
                    self.label_imagen_estudio.configure(image=self.imagen_estudio)

                    #Ajustar metodo comprar
                    if self.combo_metodos_comprar is not None:
                        self.label_metodo_comprar.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.combo_metodos_comprar.configure(width=int(self.frame_width * 0.02))

                        #Ajustar comparativa
                        if self.combo_comparativa is not None:
                            self.label_comparativa.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.combo_comparativa.configure(width=int(self.frame_width * 0.02))
        
