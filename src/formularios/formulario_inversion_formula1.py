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
from Formula1 import SF1_backtesting as SF1
from tkcalendar import DateEntry
import matplotlib.dates as mdates
import tkinter as tk
from datetime import datetime, timedelta
from formularios.formulario_mas_informacion import FormularioBackTestingMasInformacion
import ordenes as ORD   

class FormularioInversionFormula1():

    def __init__(self, panel_principal, id_user):

        self.id_user = id_user
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
        self.label_titulo_formula1 = tk.Label(self.frame_superior, text="Inversión Operaciones Fórmula 1", font=("Berlin Sans FB", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_titulo_formula1.place(relx=0.02, rely=0.1)

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
        self.label_comparativa = None
        self.label_lotaje = None
        self.label_rentabilidad = None
        self.label_rentabilidad_formula1 = None
        self.label_rentabilidad_comparativa = None
        self.label_rentabilidad_comparativa_dato = None
        
        #Inicializar variables
        self.label_lotaje = None
        self.label_stop_loss = None
        self.label_take_profit = None
        self.stop_loss_entry = None
        self.take_profit_entry = None
        self.lotaje_entry = None

        #Inicializar ComboBoxs
        self.combo_anos = None
        self.combo_pilotos = None
        self.combo_acciones = None
        self.combo_metodos_comprar = None
        self.combo_metodos_vender = None
        self.combo_comparativa = None


        #Inicializar imagenes
        self.imagen_piloto = None

        #Inicializar variables
        self.label_fecha_inicio = None
        self.label_fecha_fin = None
        self.fecha_inicio_entry = None
        self.fecha_fin_entry = None

        self.fecha_lim = datetime.today()
        self.fecha_ini = datetime.today()

        #Variables SBS
        self.acciones=SF1.acciones_escuderias
        self.standing=SF1.html_standings_files
        self.calendar=SF1.html_calendars_files
        self.pilotosTeams=SF1.html_pilotTeams_files
        self.imagenes_pilotos=SF1.imagenes_pilotos
        self.imagenes_escuderias=SF1.imagenes_escuderias
        self.paisAcciones = SF1.pais_Accion
        self.accionesAPI = SF1.acciones_api
        self.url = 'https://www.f1-fansite.com/f1-results/f1-standings-2024-championship'

        #Variables de la tabla
        self.frame_without_filter=None
        self.current_frame = None
        self.frame_with_filter=None
        self.frame_directo=None
        self.tree = None

        #Botones
        self.boton_empezar_inversion = None
        self.boton_mostrar_operaciones = None
        self.boton_guardar_inversion = None


        #ComboBoxs
        self.operacion_formula1()

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)   

        #Llamada a la función on_parent_configure cuando se redimensiona la ventana
        panel_principal.bind("<Configure>", self.on_parent_configure)

    def operacion_formula1(self):

        #Crear frame para añadir todo los combo boxs
        self.frame_combo_boxs = tk.Frame(self.frame_superior, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_combo_boxs.place(relx=0.02, rely=0.3)

        #Label de "Elige el año"
        self.label_ano = tk.Label(self.frame_combo_boxs, text="Elige el año", font=("Aptos", 15, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
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

        if self.label_piloto is None:
            #Label de "Elige el piloto"
            self.label_piloto = tk.Label(self.frame_combo_boxs, text="Elige el piloto", font=("Aptos", 15, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_piloto.grid(row=0, column=1, padx=10, pady=2, sticky="w")

            #ComboBox de pilotos
            self.combo_pilotos = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_pilotos.grid(row=1, column=1, padx=10, pady=2, sticky="w")

            #Añadir pilotos a la lista
            self.pilotos = SF1.obtener_listado_pilotos(self.combo_anos.get())
            #Ordenar los pilotos alfabeticamente
            self.pilotos.sort()
            self.combo_pilotos["values"] = list(self.pilotos)

        #Al seleccionar un piloto se actualiza la imagen
        self.combo_pilotos.bind("<<ComboboxSelected>>", self.actualizar_formula1_imagen_piloto)

        #Actualizar vista
        self.on_parent_configure(event)


    def actualizar_formula1_imagen_piloto(self, event):

        if self.label_accion is None:
            #Coger el año seleccionado
            self.ano = self.combo_anos.get()
            #Coger el piloto seleccionado
            self.piloto = self.combo_pilotos.get()

            #Poner imagen del piloto
            self.imagen_piloto = util_img.leer_imagen(self.imagenes_pilotos[self.piloto], (100,100))
            self.label_imagen_piloto = tk.Label(self.frame_superior, image=self.imagen_piloto, bg=COLOR_CUERPO_PRINCIPAL)
            self.label_imagen_piloto.place(relx=0.8, rely=0.1)

            #Label de accion
            self.accion = SF1.obtener_accion_escuderia(self.piloto, self.ano)
            self.label_accion = tk.Label(self.frame_combo_boxs, text="La acción selecionada es: " + self.accion, font=("Aptos", 15, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_accion.grid(row=2, column=0, columnspan=2, padx=10, pady=2, sticky="w")

        #continuar
        self.actualizar_formula1_metodos(None)



    def actualizar_formula1_metodos(self, event):
        if self.label_metodo_comprar is None:
            #Label de "Elige cuando comprar"
            self.label_metodo_comprar = tk.Label(self.frame_combo_boxs, text="Elige cuando comprar", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_metodo_comprar.grid(row=3, column=0, padx=10, pady=2, sticky="w")

            #ComboBox de metodos comprar
            self.combo_metodos_comprar = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_metodos_comprar.grid(row=4, column=0, padx=10, pady=2, sticky="w")
            self.combo_metodos_comprar["values"] = ["Top 1", "Top 3", "Top 5", "Top 10", "No puntúa"]

            #label de "Elige cuando vender"
            self.label_metodo_vender = tk.Label(self.frame_combo_boxs, text="Elige cuando vender", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
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
            self.actualizar_comparativa()

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
            self.actualizar_comparativa()

        #Actualizar vista
        self.on_parent_configure(event)

    def actualizar_comparativa(self):
        if self.label_comparativa is None:
            
            #Label de "Comparativa"
            self.label_comparativa = tk.Label(self.frame_combo_boxs, text="Comparativa", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_comparativa.grid(row=3, column=2, padx=10, pady=2, sticky="w")

            #ComboBox de comparativa
            self.combo_comparativa = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_comparativa.grid(row=4, column=2, padx=10, pady=2, sticky="w")
            self.combo_comparativa["values"] = ['SP500', 'IBEX35', 'Plazo Fijo']

        #al mirar todos los datos actualizar el boton
        self.combo_comparativa.bind("<<ComboboxSelected>>", self.actualizar_lotaje)

        #Ajustar vista
        self.on_parent_configure(None)

    def actualizar_lotaje(self, event):
        if self.label_lotaje is None:
            #Label lotaje
            self.label_lotaje = tk.Label(self.frame_combo_boxs, text="Lotaje", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_lotaje.grid(row=3, column=3, padx=10, pady=2, sticky="w")
            
            #Entry lotaje
            self.lotaje_entry = Entry(self.frame_combo_boxs, width=30)
            self.lotaje_entry.grid(row=4, column=3, padx=10, pady=2, sticky="w")

            #Label inversion
            self.label_inversion = tk.Label(self.frame_combo_boxs, text="Inversión: ", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_inversion.grid(row=3, column=4, padx=10, pady=2, sticky="w")

        self.lotaje_entry.bind("<KeyRelease>", self.actualizar_futbol_lotaje)

        #Actualizar vista
        self.on_parent_configure(event)

    def actualizar_futbol_lotaje(self, event):
        if self.lotaje_entry.get() == "" and self.boton_empezar_inversion is not None:
            self.boton_empezar_inversion.configure(state="disabled")

        try:
            aux = int(self.lotaje_entry.get())
            self.lotaje_entry.configure(text=aux)    

            # Aquí puedes usar 'aux', que contendrá el valor convertido a entero
        except ValueError:
            # Si no se puede convertir a entero, se maneja la excepción aquí
            # Por ejemplo, podrías mostrar un mensaje de error al usuario
            messagebox.showerror("Error", "El valor ingresado no es un número entero válido")

    
        #Cambiar texto inversion
        self.valor_precio = self.getValorPrecio()
        self.valor_inversion = int(self.lotaje_entry.get()) * self.valor_precio
        self.label_inversion.configure(text="Inversión: " + str(self.valor_inversion))

        #Actualizar vista
        self.on_parent_configure(event)

        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.lotaje_entry.get() != "":
            self.actualizar_formula1_ticks()

    def getValorPrecio(self):
        return 5
        #DAVID AQUI PILLAS EL PRECIO PERRA

    def set_dates(self):
        min_year, max_year = SF1.obtener_periodo_valido(self.piloto, self.combo_anos.get())
        self.fecha_lim = min(datetime(max_year, 12, 31), datetime.today())
        self.fecha_ini = datetime(min_year, 1, 1)

        self.fecha_fin_entry.config(maxdate=self.fecha_lim)
        self.fecha_fin_entry.config(mindate=self.fecha_ini)
        self.fecha_fin_entry.set_date(self.fecha_lim)

        self.fecha_inicio_entry.config(maxdate=self.fecha_lim)
        self.fecha_inicio_entry.config(mindate=self.fecha_ini)
        self.fecha_inicio_entry.set_date(self.fecha_ini)
    
    def actualizar_formula1_ticks(self):
        if (self.fecha_inicio_entry is None):
            #Label fecha inicio
            self.label_fecha_inicio = tk.Label(self.frame_combo_boxs, text="Fecha inicio", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_fecha_inicio.grid(row=5, column=0, padx=10, pady=2, sticky="w")

            #label fecha fin
            self.label_fecha_fin = tk.Label(self.frame_combo_boxs, text="Fecha fin", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_fecha_fin.grid(row=5, column=1, padx=10, pady=2, sticky="w")

            #Date fecha inicio
            fecha_ayer = datetime.now() - timedelta(days = 1)
            self.fecha_inicio_entry = DateEntry(
                self.frame_combo_boxs, 
                date_pattern='yyyy/mm/dd',
                background='darkblue', 
                foreground='white', 
                borderwidth=2,
                maxdate=self.fecha_lim,
                mindate=self.fecha_ini
            )
            self.fecha_inicio_entry.grid(row=6, column=0, padx=10, pady=2, sticky="w")

            #Date fecha fin
            self.fecha_fin_entry = DateEntry(
                self.frame_combo_boxs,
                date_pattern='yyyy/mm/dd',
                background='darkblue',
                foreground='white',
                borderwidth=2,
                maxdate=self.fecha_lim,
                mindate=self.fecha_ini
            )
            self.fecha_fin_entry.grid(row=6, column=1, padx=10, pady=2, sticky="w")

            self.set_dates()

        if (self.label_stop_loss is None):
            #Entry stop loss
            self.label_stop_loss = tk.Label(self.frame_combo_boxs, text="Stop Loss (Opcional)", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_stop_loss.grid(row=5, column=2, padx=(10,0), pady=2, sticky="w")

            self.stop_loss_entry = Entry(self.frame_combo_boxs, width=30)
            self.stop_loss_entry.grid(row=6, column=2, padx=(10,0), pady=2, sticky="w")
        
        if (self.label_take_profit is None):
            #Entry take profit
            self.label_take_profit = tk.Label(self.frame_combo_boxs, text="Take Profit (Opcional)", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_take_profit.grid(row=5, column=3, padx=(10,0), pady=2, sticky="w")

            self.take_profit_entry = Entry(self.frame_combo_boxs, width=30)
            self.take_profit_entry.grid(row=6, column=3, padx=(10,0), pady=2, sticky="w")

        # Boton de "Empezar inversion"
        self.boton_empezar_inversion = tk.Button(self.frame_combo_boxs, text="Empezar\ninversión", font=("Aptos", 12), bg="green", fg="white", command=self.empezar_inversion) # wraplength determina el ancho máximo antes de que el texto se divida en dos líneas
        self.boton_empezar_inversion.grid(row=5, column=4, rowspan=2, padx=10, pady=2, sticky="w")

        #Ajustar vista
        self.on_parent_configure(None)

    def empezar_inversion(self):

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
        self.tickdirecto()

        #Ajustar vista
        self.on_parent_configure(None)

    def crear_interfaz_inferior(self):
        # Frame para mostrar los datos
        self.frame_datos = tk.Frame(self.frame_inferior, bg=COLOR_CUERPO_PRINCIPAL, width=399)
        self.frame_datos.pack(fill=tk.BOTH, expand=True)

        # Label de "Rentabilidad"
        self.label_rentabilidad = tk.Label(self.frame_datos, text="Rentabilidad", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad.pack(side="left", padx=(10, 0), pady=5)

        # Rentabilidad
        self.rentabilidad_f1 = tk.StringVar()
        self.rentabilidad_f1.set("0")
        self.label_rentabilidad_f1 = tk.Label(self.frame_datos, textvariable=self.rentabilidad_f1, font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_f1.pack(side="left", padx=(0, 10), pady=5)

        #Label rentabalidad comparativa
        rent = self.combo_comparativa.get()
        self.label_rentabilidad_comparativa = tk.Label(self.frame_datos, text="Rentabilidad " + rent, font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_comparativa.pack(side="left", padx=(10, 0), pady=5)

        # Rentabilidad comparativa
        self.rentabilidad_comparativa = tk.StringVar()
        self.rentabilidad_comparativa.set("0")
        self.label_rentabilidad_comparativa_dato = tk.Label(self.frame_datos, textvariable=self.rentabilidad_comparativa, font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_comparativa_dato.pack(side="left", padx=(0, 10), pady=5)

        # Boton de "Parar Inversión"
        self.boton_parar_inversion = tk.Button(self.frame_datos, text="Parar\ninversión", font=("Aptos", 12), bg="green", fg="white", command=self.parar_inversion) 
        self.boton_parar_inversion.pack(side="right", padx=(0, 10), pady=5)

        # Crear un contenedor para los Treeviews
        self.tree_container = tk.Frame(self.frame_inferior)
        self.tree_container.pack(side="left", fill="both", expand=True)

        # Frame para el primer Treeview
        self.frame_tree = tk.Frame(self.tree_container)
        self.frame_tree.grid(row=0, column=0, sticky="nsew")

        # Frame para el segundo Treeview
        self.frame_tree_ticks = tk.Frame(self.tree_container)
        self.frame_tree_ticks.grid(row=0, column=1, sticky="nsew")

        # Primer Treeview
        self.tree = ttk.Treeview(self.frame_tree)
        self.tree.pack(side="left", fill="both", expand=True)

        # Segundo Treeview
        self.tree_ticks = ttk.Treeview(self.frame_tree_ticks)
        self.tree_ticks.pack(side="right", fill="both", expand=True)

        self.tree_container.grid_rowconfigure(0, weight=1)
        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_columnconfigure(1, weight=1)



    def obtenerPais(self, accion_txt):
        print(accion_txt)
        mercado = accion_txt.split('.')[1]
        pais = self.paisAcciones.get(mercado)
        print(mercado, pais)
        return pais
    
    def obtenerAccion(self, accion_txt):
        accionApi = self.accionesAPI.get(accion_txt)
        if(accionApi == '' or accionApi is None):
            accionApi = accion_txt
        print(accionApi)
        return accionApi

    def tickdirecto(self):
        
        frecuencia_txt = "Daily"
        inicio_txt = self.fecha_inicio_entry.get()
        fin_txt = self.fecha_fin_entry.get()
        estrategia_txt = 'Formula1'
        piloto_txt = self.piloto
        cuando_comprar = self.combo_metodos_comprar.get()
        cuando_vender = self.combo_metodos_vender.get()
        self.accion = self.obtenerAccion(self.accion)
        pais_txt = self.obtenerPais(self.accion)
        self.accion = self.accion.split('.')[0]
        lotaje_txt = self.lotaje_entry.get()
        stoploss_txt=self.stop_loss_entry.get()
        takeprofit_txt=self.take_profit_entry.get()

        if ',' in stoploss_txt:
            stoploss_txt = stoploss_txt.replace(",", ".")
            
        if ',' in takeprofit_txt:
            takeprofit_txt = takeprofit_txt.replace(",", ".")
            
        self.b.establecer_inversion_directo(frecuencia_txt, self.accion,lotaje_txt,stoploss_txt,takeprofit_txt)#le pasamos el acronimo de MT5 que es donde invierto
        self.fecha_inicio_indicadores=datetime.now().date() #para los sp500, ibex
        
        self.b.thread_F1(piloto_txt, self.url, cuando_comprar, cuando_vender)
        self.b.thread_orders_creativas(estrategia_txt)
        self.funciones_recursivas = True
        self.actualizar_carreras()
        self.actualizar_frame()


    def actualizar_carreras(self):
        if(self.funciones_recursivas):
            print("carreras")
            # if(SBS.FRAMEDIRECTO.empty):
            #     self.frame_principal.after(10000, self.actualiar_partidos)#10s
            self.frame_directo=SF1.FRAMEDIRECTO
            print("-------------------FRAME TICKS PARTIDO-------------------")
            print(self.frame_directo)
            self.treeview_carreras()
            self.frame_principal.after(7000, self.actualizar_carreras)
    
    def actualizar_frame(self):
        if(self.funciones_recursivas):
            print("ticks")
            # if(ORD.FRAMETICKS.empty):
            #     self.frame_principal.after(10000, self.actualiar_frame)
            self.frame_ticks=ORD.FRAMETICKS
            print("-------------------FRAME TICKS -------------------")
            print(self.frame_ticks)
            self.treeview_ticks()
            self.frame_principal.after(7000, self.actualizar_frame)


    def treeview_carreras(self):
        self.current_frame =self.frame_directo

        # Configurar las columnas del widget Treeview
        self.tree["columns"] = list(self.current_frame.columns)
        self.tree["show"] = "headings"  # Desactivar la columna adicional
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=50)

        # Limpiar el widget Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Añadir todos los datos del DataFrame al widget Treeview
        for index, row in self.current_frame.iterrows():
            self.tree.insert("", "end", values=tuple(row))

    def treeview_ticks(self):
        self.current_frame2 = self.frame_ticks

        # Configurar las columnas del widget Treeview
        self.tree_ticks["columns"] = list(self.current_frame2.columns)
        self.tree_ticks["show"] = "headings"  # Desactivar la columna adicional
        for col in self.tree_ticks["columns"]:
            self.tree_ticks.heading(col, text=col)
            self.tree_ticks.column(col, width=50)

        # Limpiar el widget Treeview
        for row in self.tree_ticks.get_children():
            self.tree_ticks.delete(row)

        # Añadir todos los datos del DataFrame al widget Treeview
        for index, row in self.current_frame2.iterrows():
            self.tree_ticks.insert("", "end", values=tuple(row))

    def parar_inversion(self):
        # Habilitar los ComboBoxs, los Entry y el Botón de "Empezar inversión"
        self.combo_anos.configure(state="normal")
        self.combo_pilotos.configure(state="normal")
        #self.combo_acciones.configure(state="normal")
        self.combo_metodos_comprar.configure(state="normal")
        self.combo_metodos_vender.configure(state="normal")
        self.stop_loss_entry.configure(state="normal")
        self.take_profit_entry.configure(state="normal")
        self.lotaje_entry.configure(state="normal")
        self.boton_empezar_inversion.configure(state="normal")

        #Calcular la rentabilidad de la comparativa
        self.calcular_rentabilidad_comparativa()


        self.funciones_recursivas=False#paro la ejecucion de las funciones recursivas
        self.b.kill_threads()
        frame_inversiones_finalizadas=self.b.parar_inversion()
        frame_carreras_final=self.b.parar_carreras()
        self.frame_ticks=frame_inversiones_finalizadas
        self.frame_directo=frame_carreras_final
        self.treeview_carreras()
        self.treeview_ticks()
        self.fecha_fin_indicadores=datetime.now().date()#para los sp500, ibex

        rentabilidades = self.frame_ticks[self.frame_ticks['Rentabilidad'] != '-']['Rentabilidad']
        suma_rentabilidades = rentabilidades.sum().round(2)
        self.rentabilidad_f1.set(str(suma_rentabilidades))
        self.label_rentabilidad_f1.configure(textvariable=self.rentabilidad_f1)


    def calcular_rentabilidad_comparativa(self): #PARA HACER JOSE Y DAVID, NO SE COMO COÑO VA ESTO, MIRARLO ANDA, HE PUESTO 5 PA QUE NO PETE
        rentabilidad_comparativa = 0
        if self.combo_comparativa.get() == "SP500":
            #rentabilidad_comparativa = tr.calcularSP(self.fecha_inicio_indicadores, self.fecha_fin_indicadores)
            rentabilidad_comparativa = 5
        elif self.combo_comparativa.get() == "IBEX35":
            #rentabilidad_comparativa = tr.calcularIBEX35(self.fecha_inicio_indicadores, self.fecha_fin_indicadores)
            rentabilidad_comparativa = 5
        elif self.combo_comparativa.get() == "Plazo Fijo":
            #rentabilidad_comparativa = tr.calcular_rentabilidad_plazo_fijo(self.fecha_inicio_indicadores, self.fecha_fin_indicadores)
            rentabilidad_comparativa = 5
        self.rentabilidad_comparativa.set(str(rentabilidad_comparativa))
        self.label_rentabilidad_comparativa_dato.configure(textvariable=self.rentabilidad_comparativa)


    # def guardar_inversion(self):
        
    #     # Conexión a la base de datos
    #     self.conn = mysql.connector.connect(
    #                 host=DBConfig.HOST,
    #                 user=DBConfig.USER,
    #                 password=DBConfig.PASSWORD,
    #                 database=DBConfig.DATABASE,
    #                 port=DBConfig.PORT
    #             )
        
    #     # Para ponerle nombre a la inversión, realizamos este bucle hasta que el usuario ingrese un nombrenombre_inversión = ""
    #     nombre_inversión = ""
    #     while True:
    #         # Dejamos que el usuario ingrese el nombre de la inversión que ha realizado
    #         nombre_inversión = simpledialog.askstring("Guardar inversión", "Ingrese el nombre de la inversión:", parent=self.frame_principal)

    #         if nombre_inversión is None:
    #             # Si se hace clic en Cancelar, salimos del bucle
    #             break

    #         if not nombre_inversión:
    #             # En el caso de que no se haya ingresado un nombre, mostramos mensaje de error y volvemos a pedirlo
    #             messagebox.showerror("Error", "Debes ingresar un nombre para tu inversión.")
    #             continue
            
    #         if self.nombre_inversion_existe(nombre_inversión):
    #             messagebox.showerror("Error", "Ya existe una inversión con ese nombre.")
    #             continue

    #         # Si llegamos a este punto, el usuario ha introducido un nombre de inversión correcto
    #         break

    #     if(nombre_inversión is None):
    #         return
        
    #     # Le damos valor al tipo de inversión que esta haciendo el usuario
    #     tipo = "Formula 1"

    #     # Cogemos la acción en la que ha invertido el usuario
    #     accion = self.accion

    #     # Cogemos la fecha de inicio y la de fin de la inversión
    #     fecha_ini = self.fecha_inicio_entry.get()
    #     fecha_fin = self.fecha_fin_entry.get()

    #     # Cogemos cuando toma las decisiones de comprar y vender el usuario
    #     compra = self.combo_metodos_comprar.get()
    #     venta = self.combo_metodos_vender.get()

    #     # Le damos valor a la frecuencia
    #     frecuencia = "Diaria"

    #     # Cogemos la rentabilidad de la inversión
    #     rentabilidad = self.rentabilidad_f1.get()

    #     # Guardamos la inversión en la base de datos
    #     cursor = self.conn.cursor()
    #     try:
    #         # Realizamos la consulta para insertar los datos en la tabla Inversiones
    #         consulta = "INSERT INTO Inversiones (id_usuario, nombre, tipo, accion, fecha_inicio, fecha_fin, compra, venta, frecuencia, rentabilidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #         datos = (self.id_user, nombre_inversión, tipo, accion, fecha_ini, fecha_fin, compra, venta, frecuencia, rentabilidad)
    #         cursor.execute(consulta, datos)
    #     except Exception as e:
    #         print(e)
        
    #     # Cerramos el cursor y la conexxión
    #     cursor.close()
    #     self.conn.commit()
    #     self.conn.close()

    # def nombre_inversion_existe(self, nombre_inversion):
    #     # Obtener el cursor para ejecutar consultas
    #     cursor = self.conn.cursor()

    #     # Consulta para obtener los datos de la tabla Inversiones segun el id_user correspondiente
    #     consulta = "SELECT COUNT(*) FROM Inversiones WHERE id_usuario = %s AND nombre = %s"
    #     datos = (self.id_user, nombre_inversion) 
    #     cursor.execute(consulta, datos)
    #     cantidad = cursor.fetchone()[0]

    #     # Cerrar el cursor
    #     cursor.close()

    #     return cantidad > 0


    # def mas_informacion(self):
    #     self.limpiar_panel(self.frame_principal)     
    #     FormularioBackTestingMasInformacion(self.frame_principal, self.frame_without_filter, "Formula1", self.rentabilidad_f1.get())

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
        self.frame_superior.configure(width=self.frame_width, height=self.frame_height*0.6)
        self.frame_inferior.configure(width=self.frame_width, height=self.frame_height*0.4)

        #Ajustar el tamaño del titulo
        self.label_titulo_formula1.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.2), "bold"))

        #Ajustar tiks
        if self.label_stop_loss is not None:
            self.label_stop_loss.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.label_take_profit.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.stop_loss_entry.configure(width=int(self.frame_width * 0.02))
            self.take_profit_entry.configure(width=int(self.frame_width * 0.02))

        #Ajustar el tamaño del boton iniciar inversion
        if self.boton_empezar_inversion is not None:
            self.boton_empezar_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_empezar_inversion.configure(width=int(self.frame_width * 0.015))

        #Ajustar el tamaño de los botones
        if self.boton_mostrar_operaciones is not None:
            self.boton_guardar_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_mostrar_operaciones.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_mas_informacion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_guardar_inversion.configure(width=int(self.frame_width * 0.015))
            self.boton_mostrar_operaciones.configure(width=int(self.frame_width * 0.015))
            self.boton_mas_informacion.configure(width=int(self.frame_width * 0.015))

        #ajustar el tamaño de las fechas
        if self.label_fecha_inicio is not None:
            self.label_fecha_inicio.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.label_fecha_fin.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.fecha_inicio_entry.configure(width=int(self.frame_width * 0.02))
            self.fecha_fin_entry.configure(width=int(self.frame_width * 0.02))

        #Ajustar el tamaño de los labels
        if self.label_ano is not None:
            self.label_ano.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.combo_anos.configure(width=int(self.frame_width * 0.02))

            if self.label_piloto is not None:
                self.label_piloto.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                self.combo_pilotos.configure(width=int(self.frame_width * 0.02))

                if self.label_accion is not None:
                    self.label_accion.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                    
                    if self.label_metodo_comprar is not None:
                        self.label_metodo_comprar.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.combo_metodos_comprar.configure(width=int(self.frame_width * 0.02))

                        if self.label_metodo_vender is not None:
                            self.label_metodo_vender.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.combo_metodos_vender.configure(width=int(self.frame_width * 0.02))

                            if self.label_comparativa is not None:
                                self.label_comparativa.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                self.combo_comparativa.configure(width=int(self.frame_width * 0.02))

                                if self.label_lotaje is not None:
                                    self.label_lotaje.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                    self.lotaje_entry.configure(width=int(self.frame_width * 0.02))
                                    self.label_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

                                    if self.label_rentabilidad is not None:
                                        self.label_rentabilidad.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                        self.label_rentabilidad_f1.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                        self.label_rentabilidad_comparativa.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                        self.label_rentabilidad_comparativa_dato.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))