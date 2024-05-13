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
from EquiposdeFutbol import SBS_backtesting as SBS
from tkcalendar import DateEntry
import matplotlib.dates as mdates
import tkinter as tk
from datetime import datetime, timedelta
from formularios.formulario_mas_informacion import FormularioBackTestingMasInformacion


class FormularioBackTestingFutbol():

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
        self.label_titulo_futbol = tk.Label(self.frame_superior, text="Backtesting Operaciones Fútbol", font=("Berlin Sans FB", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_titulo_futbol.place(relx=0.05, rely=0.1)

        # Frame inferior (con scrollbar)
        self.frame_inferior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL, width=399, height=276)
        self.frame_inferior.pack(fill=tk.BOTH)

        #VARIABLES
        #Inicializar Labels
        self.label_liga = None
        self.label_equipo = None
        self.label_accion = None
        self.label_metodo_comprar = None
        self.label_metodo_vender = None
        self.label_comparativa = None
        self.label_rentabilidad = None
        self.label_rentabilidad_futbol = None
        self.label_rentabilidad_comparativa = None
        self.label_rentabilidad_comparativa_texto = None

        #Inicializar ComboBoxs
        self.combo_ligas = None
        self.combo_equipos = None
        self.combo_accion = None
        self.combo_metodos_comprar = None
        self.combo_metodos_vender = None


        self.ibex35 = None
        self.sp500 = None
        self.plazo_fijo = None

        self.label_rentabilidad_ibex35 = None
        self.label_rentabilidad_sp500 = None
        self.label_rentabilidad_plazo_fijo = None

        self.var_ibex35 = None
        self.var_sp500 = None
        self.var_plazo_fijo = None

        #Inicializar imagenes
        self.imagen_liga = None
        self.imagen_equipo = None
        self.imagen_accion = None

        #Inicializar variables
        self.label_fecha_inicio = None
        self.label_fecha_fin = None
        self.fecha_inicio_entry = None
        self.fecha_fin_entry = None
        self.fecha_ini = datetime(year=2014, month=7, day=1)

        #Variables SBS
        self.ligas=SBS.ligas
        self.acciones=SBS.acciones
        self.pais=SBS.pais
        self.url=SBS.urls_equipos
        self.acronimos_acciones=SBS.acronimo_acciones_api
        self.imagenes_liga=SBS.imagenes_ligas
        self.imagenes_equipos=SBS.imagenes_equipos

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
        self.crear_combo_boxs()

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)   

        #Llamada a la función on_parent_configure cuando se redimensiona la ventana
        panel_principal.bind("<Configure>", self.on_parent_configure)

    def crear_combo_boxs(self):

        #Crear frame para añadir todo los combo boxs
        self.frame_combo_boxs = tk.Frame(self.frame_superior, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_combo_boxs.place(relx=0.05, rely=0.3)

        #definir prioridades de las columnas
        self.frame_combo_boxs.grid_columnconfigure(0, weight=1)
        self.frame_combo_boxs.grid_columnconfigure(1, weight=1)
        self.frame_combo_boxs.grid_columnconfigure(2, weight=1)
        self.frame_combo_boxs.grid_columnconfigure(3, weight=1)
        self.frame_combo_boxs.grid_columnconfigure(4, weight=1)


        #seguir
        self.operacion_futbol()

    def operacion_futbol(self):
        #label de "Elige la liga"
        self.label_liga = tk.Label(self.frame_combo_boxs, text="Elige la liga", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_liga.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        #ComboBox de ligas
        self.combo_ligas = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_ligas.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        self.combo_ligas["values"] = list(self.ligas.keys())
                
        #Ajustar vista
        self.on_parent_configure(None)

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

        if self.label_equipo is None:
            #Poner imagen de la liga
            self.imagen_liga = util_img.leer_imagen(self.imagenes_liga[self.liga], (10,10))
            self.label_imagen_liga = tk.Label(self.frame_superior, image=self.imagen_liga, bg=COLOR_CUERPO_PRINCIPAL)
            self.label_imagen_liga.place(relx=0.8, rely=0.1)

            #Label de "Elige el equipo"
            self.label_equipo = tk.Label(self.frame_combo_boxs, text="Elige el equipo", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_equipo.grid(row=0, column=1, padx=10, pady=2, sticky="w")

            #ComboBox de equipos
            self.combo_equipos = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_equipos.grid(row=1, column=1, padx=10, pady=2, sticky="w")
            self.combo_equipos["values"] = self.ligas[self.liga]

        #Ajustar vista
        self.on_parent_configure(event)

        #Actualizar vista al cambiar de equipo        
        self.combo_equipos.bind("<<ComboboxSelected>>", self.actualizar_futbol_accion)

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

        if self.label_accion is None:
            #Poner imagen del equipo
            self.imagen_equipo = util_img.leer_imagen(self.imagenes_equipos[self.equipo], (10,10))
            self.label_imagen_equipo = tk.Label(self.frame_superior, image=self.imagen_equipo, bg=COLOR_CUERPO_PRINCIPAL)
            self.label_imagen_equipo.place(relx=0.9, rely=0.1)
            
            #Label de "Elige acción"
            self.label_accion = tk.Label(self.frame_combo_boxs, text="Elige acción", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_accion.grid(row=0, column=2, padx=10, pady=2, sticky="w")

            #ComboBox de acciones
            self.combo_accion = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_accion.grid(row=1, column=2, padx=10, pady=2, sticky="w")
            self.combo_accion["values"] = self.acciones[self.equipo]
        
        #Actualizar vista al cambiar de accion        
        self.combo_accion.bind("<<ComboboxSelected>>", self.actualizar_futbol_metodos)

        #Ajustar vista
        self.on_parent_configure(event)

    def actualizar_futbol_metodos(self, event):
        #Coger la accion seleccionada
        self.accion = self.combo_accion.get()

        if self.label_metodo_comprar is None:
            #Label de "Elige cuando comprar"
            self.label_metodo_comprar = tk.Label(self.frame_combo_boxs, text="Elige cuando comprar", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_metodo_comprar.grid(row=2, column=0, padx=10, pady=2, sticky="w")

            #ComboBox de metodos comprar
            self.combo_metodos_comprar = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_metodos_comprar.grid(row=3, column=0, padx=10, pady=2, sticky="w")
            self.combo_metodos_comprar["values"] = ["Ganado", "Perdido", "Empatado", "Ganado/Empatado", "Empatado/Perdido", "Ganado/Perdido"]

            #label de "Elige cuando vender"
            self.label_metodo_vender = tk.Label(self.frame_combo_boxs, text="Elige cuando vender", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_metodo_vender.grid(row=2, column=1, padx=10, pady=2, sticky="w")

            #ComboBox de metodos vender
            self.combo_metodos_vender = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_metodos_vender.grid(row=3, column=1, padx=10, pady=2, sticky="w")
            self.combo_metodos_vender["values"] = ["Ganado", "Perdido", "Empatado", "Ganado/Empatado", "Empatado/Perdido", "Ganado/Perdido"]

        #Cuando o comprar o vender tenga un valor seleccionado quitar esa opcion del otro
        self.combo_metodos_comprar.bind("<<ComboboxSelected>>", self.actualizar_futbol_metodos_vender)
        self.combo_metodos_vender.bind("<<ComboboxSelected>>", self.actualizar_futbol_metodos_comprar)

        #Ajustar vista
        self.on_parent_configure(event)

    def actualizar_futbol_metodos_comprar(self, event):
        #Coger el metodo de vender seleccionado
        self.metodo_vender = self.combo_metodos_vender.get()
        
        #Quitar opciones dependiendo de lo que se eliga en vender, opciones especiales en cada caso
        if self.metodo_vender == "Ganado":
            self.combo_metodos_comprar["values"] = ["Perdido", "Empatado", "Empatado/Perdido"]
        elif self.metodo_vender == "Perdido":
            self.combo_metodos_comprar["values"] = ["Ganado", "Empatado", "Ganado/Empatado"]
        elif self.metodo_vender == "Empatado":
            self.combo_metodos_comprar["values"] = ["Ganado", "Perdido", "Ganado/Perdido"]
        elif self.metodo_vender == "Ganado/Empatado":
            self.combo_metodos_comprar["values"] = ["Perdido"]
        elif self.metodo_vender == "Empatado/Perdido":
            self.combo_metodos_comprar["values"] = ["Ganado"]
        elif self.metodo_vender == "Ganado/Perdido":
            self.combo_metodos_comprar["values"] = ["Empatado"]
       
        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.combo_metodos_comprar.get() != "" and self.combo_metodos_vender.get() != "":
            self.actualizar_comparativa()

        #Actualizar vista
        self.on_parent_configure(None)

    def actualizar_futbol_metodos_vender(self, event):
        #Coger el metodo de comprar seleccionado
        self.metodo_comprar = self.combo_metodos_comprar.get()

        #Quitar opciones dependiendo de lo que se eliga en comprar, opciones especiales en cada caso 
        if self.metodo_comprar == "Ganado":
            self.combo_metodos_vender["values"] = ["Perdido", "Empatado", "Empatado/Perdido"]
        elif self.metodo_comprar == "Perdido":
            self.combo_metodos_vender["values"] = ["Ganado", "Empatado", "Ganado/Empatado"]
        elif self.metodo_comprar == "Empatado":
            self.combo_metodos_vender["values"] = ["Ganado", "Perdido", "Ganado/Perdido"]
        elif self.metodo_comprar == "Ganado/Empatado":
            self.combo_metodos_vender["values"] = ["Perdido"]
        elif self.metodo_comprar == "Ganado/Perdido":
            self.combo_metodos_vender["values"] = ["Ganado"]
        elif self.metodo_comprar == "Ganado/Perdido":
            self.combo_metodos_vender["values"] = ["Empatado"]       
        
        
        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.combo_metodos_comprar.get() != "" and self.combo_metodos_vender.get() != "":
            self.actualizar_comparativa()

        #Actualizar vista
        self.on_parent_configure(None)

    def actualizar_comparativa(self):
        if self.label_comparativa is None:
            
            #Label de "Comparativa"
            self.label_comparativa = tk.Label(self.frame_combo_boxs, text="Comparativa", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_comparativa.grid(row=2, column=2, padx=10, pady=2, sticky="w")

            #ComboBox de comparativa
            #self.combo_comparativa = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            #self.combo_comparativa.grid(row=3, column=2, padx=10, pady=2, sticky="w")
            #self.combo_comparativa["values"] = ['SP500', 'IBEX35', 'Plazo Fijo']

            #CheckBox de comparativas
            self.var_ibex35 = tk.BooleanVar()
            self.var_sp500 = tk.BooleanVar()
            self.var_plazo_fijo = tk.BooleanVar()
            self.ibex35 = tk.Checkbutton(self.frame_combo_boxs, text="IBEX35", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_ibex35)
            self.ibex35.grid(row=3, column=2, padx=10, pady=2, sticky="w")
            self.sp500 = tk.Checkbutton(self.frame_combo_boxs, text="SP500", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_sp500)
            self.sp500.grid(row=4, column=2, padx=10, pady=2, sticky="w")
            self.plazo_fijo = tk.Checkbutton(self.frame_combo_boxs, text="Plazo Fijo", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_plazo_fijo)
            self.plazo_fijo.grid(row=5, column=2, padx=10, pady=2, sticky="w")



        #al mirar todos los datos actualizar el boton
        self.actualizar_futbol_ticks(None)

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
                maxdate=fecha_ayer,
                mindate=self.fecha_ini
            )
            self.fecha_inicio_entry.grid(row=5, column=0, padx=10, pady=2, sticky="w")

            #Date fecha fin
            self.fecha_fin_entry = DateEntry(
                self.frame_combo_boxs,
                date_pattern='yyyy/mm/dd',
                background='darkblue',
                foreground='white',
                borderwidth=2,
                maxdate=fecha_ayer,
                mindate=self.fecha_ini
            )
            self.fecha_fin_entry.grid(row=5, column=1, padx=10, pady=2, sticky="w")

        # Boton de "Empezar backtesting"
        self.boton_empezar_backtesting = tk.Button(self.frame_combo_boxs, text="Empezar\nbacktesting", font=("Aptos", 12), bg="green", fg="white", command=self.empezar_backtesting) # wraplength determina el ancho máximo antes de que el texto se divida en dos líneas
        self.boton_empezar_backtesting.grid(row=4, column=4, rowspan=2, padx=10, pady=2)

        #Actualizar vista
        self.on_parent_configure(None)

    def crear_interfaz_inferior(self):
        # Frame para mostrar los datos
        self.frame_datos = tk.Frame(self.frame_inferior, bg=COLOR_CUERPO_PRINCIPAL, width=399)
        self.frame_datos.pack(side="top", fill=tk.BOTH, expand=True)

        # Crear una sub-frame para las etiquetas
        self.frame_rentabilidades = tk.Frame(self.frame_inferior, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_rentabilidades.pack(side="top", anchor="w", padx=(10, 0), pady=5)

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

        # Boton de "Mostrar Operaciones"
        self.boton_mostrar_operaciones = tk.Button(self.frame_datos, text="Mostrar\noperaciones", font=("Aptos", 12), bg="green", fg="white", command=self.toggle_frames) 
        self.boton_mostrar_operaciones.pack(side="right", padx=(0, 10), pady=5)

        # Boton de "Guardar"
        self.boton_guardar_backtesting = tk.Button(self.frame_datos, text="Guardar\nbacktesting", font=("Aptos", 12), bg="green", fg="white", command=self.guardar_backtesting) 
        self.boton_guardar_backtesting.pack(side="right", padx=(0, 10), pady=5)

        #Boton "Más información"
        self.boton_mas_informacion = tk.Button(self.frame_datos, text="Más\ninformación", font=("Aptos", 12), bg="green", fg="white", command=self.mas_informacion)
        self.boton_mas_informacion.pack(side="right", padx=(0, 10), pady=5)

        #Crear un widget Treeview
        self.tree = ttk.Treeview(self.frame_inferior)
        self.tree.pack(side="bottom", fill="x", expand=True)

        #Actualizar vista
        self.on_parent_configure(None)

    def rentabilidades_comparativas(self): #DAVID aqui necesito la rentabilidad de los indicadores
        
        #Ibex35 si está seleccionado
        if self.var_ibex35.get():
            if self.label_rentabilidad_ibex35 is not None:
                self.label_rentabilidad_ibex35.destroy()
                self.label_rentabilidad_ibex35 = None
            #rentIbex35 = self.b.rentabilidad_indicador('Ibex35') 
            self.label_rentabilidad_ibex35 = tk.Label(self.frame_rentabilidades, text="Rentabilidad IBEX35: ", font=("Aptos", 10), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_rentabilidad_ibex35.pack(side="left", padx=(0, 10), pady=5)
        else:
            if self.label_rentabilidad_ibex35 is not None:
                self.label_rentabilidad_ibex35.destroy()
                self.label_rentabilidad_ibex35 = None
    
        #SP500 si está seleccionado
        if self.var_sp500.get():
            if self.label_rentabilidad_sp500 is not None:
                self.label_rentabilidad_sp500.destroy()
                self.label_rentabilidad_sp500 = None
            self.label_rentabilidad_sp500 = tk.Label(self.frame_rentabilidades, text="Rentabilidad SP500: ", font=("Aptos", 10), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_rentabilidad_sp500.pack(side="left", padx=(0, 10), pady=5)
        else:
            if self.label_rentabilidad_sp500 is not None:
                self.label_rentabilidad_sp500.destroy()
                self.label_rentabilidad_sp500 = None

        #Plazo fijo si está seleccionado
        if self.var_plazo_fijo.get():
            if self.label_rentabilidad_plazo_fijo is not None:
                self.label_rentabilidad_plazo_fijo.destroy()
                self.label_rentabilidad_plazo_fijo = None
            self.label_rentabilidad_plazo_fijo = tk.Label(self.frame_rentabilidades, text="Rentabilidad Plazo Fijo: ", font=("Aptos", 10), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_rentabilidad_plazo_fijo.pack(side="left", padx=(0, 10), pady=5)
        else:
            if self.label_rentabilidad_plazo_fijo is not None:
                self.label_rentabilidad_plazo_fijo.destroy()
                self.label_rentabilidad_plazo_fijo = None
            
        

            



    def empezar_backtesting(self):
        #Verifiar que se han seleccionado todos los campos
        if self.combo_ligas.get() == "" or self.combo_equipos.get() == "" or self.combo_accion.get() == "" or self.combo_metodos_comprar.get() == "" or self.combo_metodos_vender.get() == "":
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

        self.rentabilidades_comparativas()

        # Llamar a la función para obtener nuevos datos
        self.coger_ticks()

    def treeview(self):
        
        self.frame_with_filter = self.frame_without_filter[self.frame_without_filter['Decision'].isin(['Compra', 'Venta'])]

        # Set the initial DataFrame to display
        self.current_frame = self.frame_without_filter
        print("-----------------------------------")
        print(self.current_frame)
        # Configurar las columnas del widget Treeview
        self.tree["columns"] = list(self.current_frame.columns)
        self.tree["show"] = "headings"  # Desactivar la columna adicional
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Limpiar el widget Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Añadir todos los datos del DataFrame al widget Treeview
        for index, row in self.current_frame.iterrows():
            self.tree.insert("", "end", values=tuple(row))
    
    def coger_ticks(self):
        
        inicio_txt = self.fecha_inicio_entry.get()
        fin_txt = self.fecha_fin_entry.get()
        equipo_txt = self.combo_equipos.get()
        accion_txt = self.acronimos_acciones[self.combo_accion.get()]
        indicador= 'Ibex35'
        estrategia_txt = 'Futbol'
        pais_txt = self.pais[accion_txt]
        url_txt = self.url[equipo_txt]
        frecuencia_txt = "Daily"
        cuando_comprar = self.combo_metodos_comprar.get()
        cuando_vender = self.combo_metodos_vender.get()
       
        print(equipo_txt, accion_txt, pais_txt, url_txt)
        self.b.establecer_frecuencia_accion(frecuencia_txt, accion_txt) #le pasamos el acronimo de la API para el backtesting que es de donde importo los datos
        self.frame_without_filter, rentabilidad, rentabilidad_indicador = self.b.thread_creativas(inicio_txt, fin_txt, pais_txt, url_txt, estrategia_txt, cuando_comprar, cuando_vender, equipo_txt,indicador)
        
        self.establecerRentabilidades(rentabilidad, rentabilidad_indicador)
        self.treeview()
     
    def establecerRentabilidades(self, rentabilidad, rentabilidad_indicador):
        #Rentabilidad Futbol
        self.rentabilidad_futbol.set(str(rentabilidad))
        self.label_rentabilidad_futbol.configure(textvariable=self.rentabilidad_futbol)

        #Rentabilidad comparativa    
        self.rentabilidad_comparativa.set(str(rentabilidad_indicador))
        self.label_rentabilidad_comparativa.configure(textvariable=self.rentabilidad_comparativa)
        
        

    def toggle_frames(self):
        if self.current_frame.equals(self.frame_without_filter):
            self.current_frame = self.frame_with_filter
        else:
            self.current_frame = self.frame_without_filter
        print("-----------------------------------")
        print(self.current_frame)
        # Limpiar el widget Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Añadir todos los datos del DataFrame al widget Treeview
        for index, row in self.current_frame.iterrows():
            self.tree.insert("", "end", values=tuple(row))

    def guardar_backtesting(self):
        
        # Conexión a la base de datos
        self.conn = mysql.connector.connect(
                    host=DBConfig.HOST,
                    user=DBConfig.USER,
                    password=DBConfig.PASSWORD,
                    database=DBConfig.DATABASE,
                    port=DBConfig.PORT
                )
        
        # Para ponerle nombre a la inversión, realizamos este bucle hasta que el usuario ingrese un nombrenombre_inversión = ""
        nombre_inversión = ""
        while True:
            # Dejamos que el usuario ingrese el nombre de la inversión que ha realizado
            nombre_inversión = simpledialog.askstring("Guardar inversión", "Ingrese el nombre de la inversión:", parent=self.frame_principal)

            if nombre_inversión is None:
                # Si se hace clic en Cancelar, salimos del bucle
                break

            if not nombre_inversión:
                # En el caso de que no se haya ingresado un nombre, mostramos mensaje de error y volvemos a pedirlo
                messagebox.showerror("Error", "Debes ingresar un nombre para tu inversión.")
                continue
            
            if self.nombre_inversion_existe(nombre_inversión):
                messagebox.showerror("Error", "Ya existe una inversión con ese nombre.")
                continue
            
            # Si llegamos a este punto, el usuario ha ingresado un nombre de inversión válido
            break

        if(nombre_inversión is None):
            return
        
        # Le damos valor al tipo de inversión que esta haciendo el usuario
        tipo = "Futbol"

        # Cogemos la acción en la que ha invertido el usuario	
        accion = self.combo_accion.get()

        # Cogemos la fecha de inicio y la de fin de la inversión
        fecha_ini = self.fecha_inicio_entry.get()
        fecha_fin = self.fecha_fin_entry.get()

        #Cogemos cuando toma las decisiones de comprar y vender el usuario
        compra = self.combo_metodos_comprar.get()
        venta = self.combo_metodos_vender.get()

        #Le damos valor a la frecuencia
        frecuencia = "Diaria"

        # Cogemos la rentabilidad de la inversión
        rentabilidad = self.rentabilidad_futbol.get()

        # Cogemos el indicador con el que se compara la inversión
        indicador = self.combo_comparativa.get()

        # Cogemos la rentabilidad de la inversión
        rentabilidad_indicador = self.rentabilidad_comparativa.get()

        # Guardamos la inversión en la base de datos
        cursor = self.conn.cursor()
        try:
            # Realizamos la consulta para insertar los datos en la tabla Inversiones
            consulta = "INSERT INTO Inversiones (id_usuario, nombre, tipo, accion, fecha_inicio, fecha_fin, compra, venta, frecuencia, rentabilidad, indicador, rentabilidad_indicador) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            datos = (self.id_user, nombre_inversión, tipo, accion, fecha_ini, fecha_fin, compra, venta, frecuencia ,rentabilidad, indicador, rentabilidad_indicador)
            cursor.execute(consulta, datos)
        except Exception as e:
            print(e)
        
        # Cerramos el cursor y la conexxión
        cursor.close()
        self.conn.commit()
        self.conn.close()

    def nombre_inversion_existe(self, nombre_inversion):
        # Obtener el cursor para ejecutar consultas
        cursor = self.conn.cursor()

        # Consulta para obtener los datos de la tabla Inversiones segun el id_user correspondiente
        consulta = "SELECT COUNT(*) FROM Inversiones WHERE id_usuario = %s AND nombre = %s"
        datos = (self.id_user, nombre_inversion) 
        cursor.execute(consulta, datos)
        cantidad = cursor.fetchone()[0]

        # Cerrar el cursor
        cursor.close()

        return cantidad > 0


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
        self.label_titulo_futbol.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.2), "bold"))

        #Ajustar info ticks
        if self.label_fecha_inicio is not None:
            self.label_fecha_inicio.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.label_fecha_fin.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.fecha_inicio_entry.configure(width=int(self.frame_width * 0.02))
            self.fecha_fin_entry.configure(width=int(self.frame_width * 0.02))
            #Ajustar botones tanto el tamaño como el texto
            self.boton_empezar_backtesting.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_empezar_backtesting.configure(width=int(self.frame_width * 0.015))

        if self.boton_guardar_backtesting is not None:
            self.boton_guardar_backtesting.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_mostrar_operaciones.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_mas_informacion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_guardar_backtesting.configure(width=int(self.frame_width * 0.015))
            self.boton_mostrar_operaciones.configure(width=int(self.frame_width * 0.015))
            self.boton_mas_informacion.configure(width=int(self.frame_width * 0.015))
        
        #Ajustar rentabilidad
        if self.label_rentabilidad is not None:
            self.label_rentabilidad.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
            self.label_rentabilidad_futbol.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
            self.label_rentabilidad_comparativa_texto.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
            self.label_rentabilidad_comparativa.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
            
        if self.label_rentabilidad_ibex35 is not None:
            self.label_rentabilidad_ibex35.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
        if self.label_rentabilidad_sp500 is not None:
            self.label_rentabilidad_sp500.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
        if self.label_rentabilidad_plazo_fijo is not None:
            self.label_rentabilidad_plazo_fijo.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
        #Ajustar label elegir liga
        if self.label_liga is not None:
            #Ajustar liga
            self.label_liga.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.combo_ligas.configure(width=int(self.frame_width * 0.02))
            
            if self.combo_ligas is not None and self.combo_ligas.get() != "": 
                self.imagen_liga = util_img.leer_imagen(self.imagenes_liga[self.liga], (int(self.frame_width * 0.08), int(self.frame_width * 0.08)))
                self.label_imagen_liga.configure(image=self.imagen_liga)

            #Ajustar equipo
            if self.combo_equipos is not None:
                self.label_equipo.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                self.combo_equipos.configure(width=int(self.frame_width * 0.02))

                if self.combo_equipos.get() != "":
                    self.imagen_equipo = util_img.leer_imagen(self.imagenes_equipos[self.equipo], (int(self.frame_width * 0.08), int(self.frame_width * 0.08)))
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

                        #Ajustar comparativa
                        if self.label_comparativa is not None:
                            self.label_comparativa.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.ibex35.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.sp500.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.plazo_fijo.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
        
