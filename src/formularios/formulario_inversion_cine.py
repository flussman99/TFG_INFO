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
import ordenes as ORD   


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
        self.frame_inferior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL, width=399, height=276)
        self.frame_inferior.pack(fill=tk.BOTH)

        #VARIABLES
        #Inicializar Labels
        self.label_disney = None
        self.label_accion = None
        self.label_estudio = None
        self.label_metodo_comprar = None
        self.label_comparativa = None

        self.label_rentabilidad = None
        self.label_rentabilidad_cine = None
        self.label_rentabilidad_comparativa_dato = None
        self.label_rentabilidad_comparativa_texto = None

        self.ibex35 = None
        self.sp500 = None
        self.plazo_fijo = None

        self.label_rentabilidad_ibex35 = None
        self.label_rentabilidad_sp500 = None
        self.label_rentabilidad_plazo_fijo = None

        self.var_ibex35 = None
        self.var_sp500 = None
        self.var_plazo_fijo = None

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
        self.label_stop_loss = None
        self.label_take_profit = None
        self.label_lotaje = None

        self.stop_loss_entry = None
        self.take_profit_entry = None
        self.lotaje_entry = None

        #Variables SBS
        self.estudios = Disney.estudios_Disney
        self.imagenes_estudios = Disney.imagenes_estudios
        self.url = 'https://en.wikipedia.org/wiki/List_of_Walt_Disney_Studios_films_(2020-2029)'

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
        self.operacion_cine()

    def operacion_cine(self):
        #label de Disney
        self.label_disney = tk.Label(self.frame_combo_boxs, text="Acción de Disney:", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_disney.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        #label accion de disney
        self.label_accion = tk.Label(self.frame_combo_boxs, text="DIS.NYSE", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
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
            self.combo_metodos_comprar["values"] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

            #Actualizar al seleccionar algo
            self.combo_metodos_comprar.bind("<<ComboboxSelected>>", self.actualizar_comparativa)
        
        #Actualizar vista
        self.on_parent_configure(None)

    def actualizar_comparativa(self, event):
        if self.label_comparativa is None:
            
            #Label de "Comparativa"
            self.label_comparativa = tk.Label(self.frame_combo_boxs, text="Comparativa", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_comparativa.grid(row=2, column=1, padx=10, pady=2, sticky="w")

            #CheckBox de comparativas
            self.var_ibex35 = tk.BooleanVar()
            self.var_sp500 = tk.BooleanVar()
            self.var_plazo_fijo = tk.BooleanVar()
            self.ibex35 = tk.Checkbutton(self.frame_combo_boxs, text="IBEX35", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_ibex35)
            self.ibex35.grid(row=3, column=1, padx=10, pady=2, sticky="w")
            self.sp500 = tk.Checkbutton(self.frame_combo_boxs, text="SP500", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_sp500)
            self.sp500.grid(row=3, column=2, padx=10, pady=2, sticky="w")
            self.plazo_fijo = tk.Checkbutton(self.frame_combo_boxs, text="Plazo Fijo", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_plazo_fijo)
            self.plazo_fijo.grid(row=3, column=3, padx=10, pady=2, sticky="w")

        #al mirar todos los datos actualizar el boton
        self.actualizar_lotajes(None)

        #Ajustar vista
        self.on_parent_configure(None)

    def actualizar_lotajes(self, event):
        if (self.label_stop_loss is None):
            #Entry stop loss
            self.label_stop_loss = tk.Label(self.frame_combo_boxs, text="Stop Loss", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_stop_loss.grid(row=4, column=0, padx=10, pady=2, sticky="w")

            self.stop_loss_entry = Entry(self.frame_combo_boxs, width=30)
            self.stop_loss_entry.grid(row=5, column=0, padx=10, pady=2, sticky="w")
        
        if (self.label_take_profit is None):
            #Entry take profit
            self.label_take_profit = tk.Label(self.frame_combo_boxs, text="Take Profit", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_take_profit.grid(row=4, column=1, padx=10, pady=2, sticky="w")

            self.take_profit_entry = Entry(self.frame_combo_boxs, width=30)
            self.take_profit_entry.grid(row=5, column=1, padx=10, pady=2, sticky="w")

        if self.label_lotaje is None:
            #Label lotaje
            self.label_lotaje = tk.Label(self.frame_combo_boxs, text="Lotaje", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_lotaje.grid(row=4, column=2, padx=10, pady=2, sticky="w")
            
            #Entry lotaje
            self.lotaje_entry = Entry(self.frame_combo_boxs, width=30)
            self.lotaje_entry.grid(row=5, column=2, padx=10, pady=2, sticky="w")

            #Label inversion
            self.label_inversion = tk.Label(self.frame_combo_boxs, text="Inversión: ", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_inversion.grid(row=4, column=3, padx=10, pady=2, sticky="w")


        self.stop_loss_entry.bind("<KeyRelease>", self.actualizar_futbol_stop_loss)
        self.take_profit_entry.bind("<KeyRelease>", self.actualizar_futbol_take_profit)
        self.lotaje_entry.bind("<KeyRelease>", self.actualizar_futbol_lotaje)

        #Actualizar vista
        self.on_parent_configure(None)
    
    def actualizar_futbol_stop_loss(self, event):
        if self.stop_loss_entry.get() == "" and self.boton_empezar_inversion is not None:
            self.boton_empezar_inversion.configure(state="disabled")

        try:
            aux_loss = float(self.stop_loss_entry.get())

            # Aquí puedes usar 'aux', que contendrá el valor convertido a entero
        except ValueError:
            # Si no se puede convertir a entero, se maneja la excepción aquí
            # Por ejemplo, podrías mostrar un mensaje de error al usuario
            messagebox.showerror("Error", "El valor ingresado no es un número entero válido")

        #Actualizar vista
        self.on_parent_configure(event)

        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.lotaje_entry.get() != "" and self.stop_loss_entry.get() != "" and self.take_profit_entry.get() != "":
            self.actualizar_boton_inversion()

    def actualizar_futbol_take_profit(self, event):
        if self.take_profit_entry.get() == "" and self.boton_empezar_inversion is not None:
            self.boton_empezar_inversion.configure(state="disabled")

        try:
            aux_profit = float(self.take_profit_entry.get())

            # Aquí puedes usar 'aux', que contendrá el valor convertido a entero
        except ValueError:
            # Si no se puede convertir a entero, se maneja la excepción aquí
            # Por ejemplo, podrías mostrar un mensaje de error al usuario
            messagebox.showerror("Error", "El valor ingresado no es un número entero válido")

        #Actualizar vista
        self.on_parent_configure(event)

        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.lotaje_entry.get() != "" and self.stop_loss_entry.get() != "" and self.take_profit_entry.get() != "":
            self.actualizar_boton_inversion()

    def actualizar_futbol_lotaje(self, event):
        if self.lotaje_entry.get() == "" and self.boton_empezar_inversion is not None:
            self.boton_empezar_inversion.configure(state="disabled")

        try:
            aux = float(self.lotaje_entry.get())

            # Aquí puedes usar 'aux', que contendrá el valor convertido a entero
        except ValueError:
            # Si no se puede convertir a entero, se maneja la excepción aquí
            # Por ejemplo, podrías mostrar un mensaje de error al usuario
            messagebox.showerror("Error", "El valor ingresado no es un número entero válido")

    
        #Cambiar texto inversion
        self.valor_precio = self.getValorPrecio()
        self.valor_inversion = round(float(self.lotaje_entry.get()) * self.valor_precio, 2)
        self.label_inversion.configure(text="Inversión: " + str(self.valor_inversion))

        #Actualizar vista
        self.on_parent_configure(event)

        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.lotaje_entry.get() != "" and self.stop_loss_entry.get() != "" and self.take_profit_entry.get() != "":
            self.actualizar_boton_inversion()


    def getValorPrecio(self):
        print(self.label_accion.cget('text'))
        selected = mt5.symbol_select(self.label_accion.cget('text'), True)
        if selected:
            tick = mt5.symbol_info_tick(self.label_accion.cget('text'))
            print(tick)
            precio=tick[2]
            
        return precio

    def actualizar_boton_inversion(self):

        # Boton de "Empezar inversion"
        self.boton_empezar_inversion = tk.Button(self.frame_combo_boxs, text="Empezar\ninversión", font=("Aptos", 12), bg="green", fg="white", command=self.empezar_inversion) # wraplength determina el ancho máximo antes de que el texto se divida en dos líneas
        self.boton_empezar_inversion.grid(row=4, column=4, rowspan=2, padx=10, pady=2, sticky="w")

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
        self.rentabilidad_cine = tk.StringVar()
        self.rentabilidad_cine.set("0")
        self.label_rentabilidad_cine = tk.Label(self.frame_datos, textvariable=self.rentabilidad_cine, font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_cine.pack(side="left", padx=(0, 10), pady=5)

        # Boton de "Parar Inversion"
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
  

    def empezar_inversion(self):
        #Verifiar que se han seleccionado todos los campos
        if self.combo_estudios.get() == "" or self.combo_metodos_comprar.get() == "":
            messagebox.showerror("Error", "Debes seleccionar todos los campos.")
            return
        # Deshabilitar los ComboBoxs, los Entry y el Botón de "Empezar inversión"
        self.combo_estudios.configure(state="disabled")
        self.combo_metodos_comprar.configure(state="disabled")
        self.stop_loss_entry.configure(state="disabled")
        self.take_profit_entry.configure(state="disabled")
        self.lotaje_entry.configure(state="disabled")
        self.boton_empezar_inversion.configure(state="disabled")
        self.ibex35.configure(state="disabled")
        self.sp500.configure(state="disabled")
        self.plazo_fijo.configure(state="disabled")



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
        self.tickdirecto()

        #Ajustar vista
        self.on_parent_configure(None)



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

    def tickdirecto(self):
        
        frecuencia_txt = "Daily"
        estrategia_txt = 'Disney'
        estudio_txt = self.estudio
        cuando_comprar_str = self.combo_metodos_comprar.get()
        cuando_comprar_float = float(cuando_comprar_str) 
        pais_txt = 'united states'
        accion = self.label_accion.cget('text').split(".")
        accion_txt = accion[0]
        lotaje_txt = self.lotaje_entry.get()
        stoploss_txt=self.stop_loss_entry.get()
        takeprofit_txt=self.take_profit_entry.get()

        if ',' in stoploss_txt:
            stoploss_txt = stoploss_txt.replace(",", ".")
            
        if ',' in takeprofit_txt:
            takeprofit_txt = takeprofit_txt.replace(",", ".")
            
        self.b.establecer_inversion_directo(frecuencia_txt, accion_txt, lotaje_txt,stoploss_txt,takeprofit_txt)#le pasamos el acronimo de MT5 que es donde invierto
        self.fecha_inicio_indicadores=datetime.now().date() #para los sp500, ibex
        
        self.b.thread_Disney(estudio_txt, self.url, cuando_comprar_float, cuando_comprar_float)
        self.b.thread_orders_creativas(estrategia_txt)
        self.funciones_recursivas = True
        self.actualizar_peliculas()
        self.actualizar_frame()

    def actualizar_peliculas(self):
        if(self.funciones_recursivas):
            print("peliculas")
            # if(SBS.FRAMEDIRECTO.empty):
            #     self.frame_principal.after(10000, self.actualiar_partidos)#10s
            self.frame_directo=Disney.FRAMEDIRECTO
            print("-------------------FRAME TICKS PARTIDO-------------------")
            print(self.frame_directo)
            self.treeview_peliculas()
            self.frame_principal.after(7000, self.actualizar_peliculas)
    
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


    def update(self):

        #Ajustas el tamaño de los frames
        self.frame_superior.configure(width=self.frame_width, height=self.frame_height*0.5)
        self.frame_inferior.configure(width=self.frame_width, height=self.frame_height*0.5)

        #Ajustar el tamaño del titulo
        self.label_titulo_futbol.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.2), "bold"))

        #Ajustar info ticks
        if self.boton_empezar_inversion is not None:
            #Ajustar botones tanto el tamaño como el texto
            self.boton_empezar_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_empezar_inversion.configure(width=int(self.frame_width * 0.015))

        if self.boton_parar_inversion is not None:
            self.boton_parar_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_parar_inversion.configure(width=int(self.frame_width * 0.015))
        
        #Ajustar rentabilidad
        if self.label_rentabilidad is not None:
            self.label_rentabilidad.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
            self.label_rentabilidad_cine.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))

        #Ajustar info ticks
        if self.label_stop_loss is not None:
            self.label_stop_loss.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.label_take_profit.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.stop_loss_entry.configure(width=int(self.frame_width * 0.02))
            self.take_profit_entry.configure(width=int(self.frame_width * 0.02))
        
        if self.lotaje_entry is not None:
            self.label_lotaje.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.lotaje_entry.configure(width=int(self.frame_width * 0.02))
            self.label_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))    

        if self.label_rentabilidad_ibex35 is not None:
            self.label_rentabilidad_ibex35.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
        if self.label_rentabilidad_sp500 is not None:
            self.label_rentabilidad_sp500.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
        if self.label_rentabilidad_plazo_fijo is not None:
            self.label_rentabilidad_plazo_fijo.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
   

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
                        if self.label_comparativa is not None:
                            self.label_comparativa.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.ibex35.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.sp500.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.plazo_fijo.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
        
                        
                            if self.label_lotaje is not None:
                                self.label_lotaje.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                self.lotaje_entry.configure(width=int(self.frame_width * 0.02))
                                self.label_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

                                if self.label_rentabilidad is not None:
                                    self.label_rentabilidad.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                    self.label_rentabilidad_cine.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

    
    def treeview_peliculas(self):
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
        self.combo_estudios.configure(state="normal")
        self.combo_metodos_comprar.configure(state="normal")
        self.stop_loss_entry.configure(state="normal")
        self.take_profit_entry.configure(state="normal")
        self.lotaje_entry.configure(state="normal")
        self.boton_empezar_inversion.configure(state="normal")
        self.ibex35.configure(state="normal")
        self.sp500.configure(state="normal")
        self.plazo_fijo.configure(state="normal")

        #Calcular la rentabilidad de la comparativa
        self.calcular_rentabilidad_comparativa()


        self.funciones_recursivas=False#paro la ejecucion de las funciones recursivas
        self.b.kill_threads()
        frame_inversiones_finalizadas=self.b.parar_inversion()
        frame_carreras_final=self.b.parar_peliculas()
        self.frame_ticks=frame_inversiones_finalizadas
        self.frame_directo=frame_carreras_final
        self.treeview_peliculas()
        self.treeview_ticks()
        self.fecha_fin_indicadores=datetime.now().date()#para los sp500, ibex

        rentabilidades = self.frame_ticks[self.frame_ticks['Rentabilidad'] != '-']['Rentabilidad']
        suma_rentabilidades = rentabilidades.sum().round(2)
        self.rentabilidad_cine.set(str(suma_rentabilidades))
        self.label_rentabilidad_cine.configure(textvariable=self.rentabilidad_cine)

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
