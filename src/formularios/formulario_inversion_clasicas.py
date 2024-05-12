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
import ordenes as ORD   



class FormularioInversionClasicas():

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
        self.label_titulo_clasicas = tk.Label(self.frame_superior, text="Inversión de Operaciones Clásicas", font=("Berlin Sans FB", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_titulo_clasicas.place(relx=0.05, rely=0.1)

        # Frame inferior (con scrollbar)
        self.frame_inferior = tk.Frame(self.frame_principal, bg="lightgray", width=399, height=276)
        self.frame_inferior.pack(fill=tk.BOTH)

        #VARIABLES
        #Variables utiles
        self.acciones, self.mercados = self.b.get_trading_data()

        #Inicializar Labels
        self.label_mercado = None
        self.label_accion = None
        self.label_estrategia = None
        self.label_frecuencia = None

        #Inicializar ComboBoxs
        self.combo_mercado = None
        self.combo_accion = None
        self.combo_estrategia = None
        self.combo_frecuencia = None

        #Inicializar variables
        self.label_stop_loss = None
        self.label_take_profit = None
        self.label_lotaje = None
        self.label_inversion = None
        self.stop_loss_entry = None
        self.take_profit_entry = None
        self.lotaje_entry = None

        #Variables de la tabla
        self.frame_without_filter=None
        self.current_frame = None
        self.frame_with_filter=None
        self.frame_directo=None
        self.tree = None
        self.frame_ticks = None
        self.current_frame2 = None

        #Botones
        self.boton_empezar_inversion = None
        self.boton_parar_inversion = None

        #Rentabilidad
        self.label_rentabilidad_clasica = None
        self.rentabilidad_clasica = None
        self.label_rentabilidad_comparativa = None
        self.rentabilidad_comparativa = None

        #Funciones recursivas
        self.funciones_recursivas=True

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
        self.operacion_clasica()

    def operacion_clasica(self):
        #label de "Elige el mercado"
        self.label_mercado = tk.Label(self.frame_combo_boxs, text="Elige el Mercado", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_mercado.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        #ComboBox de ligas
        self.combo_mercado = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_mercado.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        self.combo_mercado["values"] = self.mercados
        
        #Ajustar vista
        self.on_parent_configure(None)

        #Actualizar vista al cambiar de mercado
        self.combo_mercado.bind("<<ComboboxSelected>>", self.actualizar_accion)

    def actualizar_accion(self, event):

        #Label de "Elige la Acción"
        self.label_accion = tk.Label(self.frame_combo_boxs, text="Elige la Acción", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_accion.grid(row=0, column=1, padx=10, pady=2, sticky="w")

        #ComboBox de acciones
        self.combo_accion = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_accion.grid(row=1, column=1, padx=10, pady=2, sticky="w")
        selected_market = self.combo_mercado.get()
        if selected_market == 'DIVISES':
            selected_market = ''
            filtered_acciones = [accion for accion in self.acciones if '.' not in accion]
        else:
            filtered_acciones = [accion for accion in self.acciones if accion.endswith(selected_market)]

        #Oredear acciones alfabeticamente
        filtered_acciones.sort()
        self.combo_accion['values'] = filtered_acciones

        #Ajustar vista
        self.on_parent_configure(event)

        #Actualizar vista al cambiar de accion        
        self.combo_accion.bind("<<ComboboxSelected>>", self.actualizar_estrategia)

    def actualizar_estrategia(self, event):
        
        if self.label_estrategia is None:
            #Label de "Elige estrategia"
            self.label_estrategia = tk.Label(self.frame_combo_boxs, text="Elige estrategia", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_estrategia.grid(row=0, column=2, padx=10, pady=2, sticky="w")

            #ComboBox de estrategia
            self.combo_estrategia = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_estrategia.grid(row=1, column=2, padx=10, pady=2, sticky="w")
            self.combo_estrategia["values"] = ['RSI', 'Media Movil', 'Bandas', 'Estocastico']
        
        #Actualizar vista al cambiar de estrategia        
        self.combo_estrategia.bind("<<ComboboxSelected>>", self.actualizar_frecuencia)

        #Ajustar vista
        self.on_parent_configure(event)

    def actualizar_frecuencia(self, event):
        
        if self.label_frecuencia is None:
            #Frecuencia
            self.label_frecuencia = tk.Label(self.frame_combo_boxs, text="Elige la frecuencia", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_frecuencia.grid(row=2, column=0, padx=10, pady=2, sticky="w")

            #ComboBox de frecuencia
            self.combo_frecuencia = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_frecuencia.grid(row=3, column=0, padx=10, pady=2, sticky="w")
            self.combo_frecuencia["values"] = ['1M', '3M', '5M', '10M', '15M', '30M', '1H', '2H', '4H','Daily', 'Weekly', 'Monthly']

        #al mirar todos los datos actualizar el boton
        self.combo_frecuencia.bind("<<ComboboxSelected>>", self.actualizar_lotaje)


        #Ajustar vista
        self.on_parent_configure(event)


    def actualizar_lotaje(self, event):
        
        if self.label_lotaje is None:
            #Label de "Lotaje"
            self.label_lotaje = tk.Label(self.frame_combo_boxs, text="Lotaje", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_lotaje.grid(row=2, column=1, padx=10, pady=2, sticky="w")

            #Entry de lotaje
            self.lotaje_entry = Entry(self.frame_combo_boxs, width=30)
            self.lotaje_entry.grid(row=3, column=1, padx=10, pady=2, sticky="w")

            #Label inversion
            self.label_inversion = tk.Label(self.frame_combo_boxs, text="Inversión", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_inversion.grid(row=2, column=2, padx=10, pady=2, sticky="w")
        
        self.lotaje_entry.bind("<KeyRelease>", self.actualizar_inversion)

        #Ajustar vista
        self.on_parent_configure(event)


    def actualizar_inversion(self, event):
        try:
            aux = int(self.lotaje_entry.get())

            # Aquí puedes usar 'aux', que contendrá el valor convertido a entero
        except ValueError:
            # Si no se puede convertir a entero, se maneja la excepción aquí
            # Por ejemplo, podrías mostrar un mensaje de error al usuario
            messagebox.showerror("Error", "El valor ingresado no es un número entero válido")
    
        #Cambiar texto inversion
        self.valor_precio = self.getValorPrecio()
        self.valor_inversion = int(self.lotaje_entry.get()) * self.valor_precio
        self.label_inversion.configure(text="Inversión: " + str(self.valor_inversion))

        #actualizar si se ha puesto algo en el lotaje
        if self.lotaje_entry.get() != "":
            self.actualizar_stop_take(event)

        #Actualizar vista
        self.on_parent_configure(event)

    def getValorPrecio(self):
        return 5
        #DAVID AQUI PILLAS EL PRECIO PERRA

    def actualizar_stop_take(self, event):
        if self.label_stop_loss is None:
            #Label de "Stop loss"
            self.label_stop_loss = tk.Label(self.frame_combo_boxs, text="Stop loss", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_stop_loss.grid(row=4, column=0, padx=10, pady=2, sticky="w")

            #Entry de stop loss
            self.stop_loss_entry = Entry(self.frame_combo_boxs, width=30)
            self.stop_loss_entry.grid(row=5, column=0, padx=10, pady=2, sticky="w")

            #Label de "Take profit"
            self.label_take_profit = tk.Label(self.frame_combo_boxs, text="Take profit", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_take_profit.grid(row=4, column=1, padx=10, pady=2, sticky="w")

            #Entry de take profit
            self.take_profit_entry = Entry(self.frame_combo_boxs, width=30)
            self.take_profit_entry.grid(row=5, column=1, padx=10, pady=2, sticky="w")

        
        self.stop_loss_entry.bind("<KeyRelease>", self.actualizar_stop_loss)
        self.take_profit_entry.bind("<KeyRelease>", self.actualizar_take_profit)

        self.on_parent_configure(event)

    def actualizar_stop_loss(self, event):
        try:
            aux_loss = float(self.stop_loss_entry.get())

            # Aquí puedes usar 'aux', que contendrá el valor convertido a entero
        except ValueError:
            # Si no se puede convertir a entero, se maneja la excepción aquí
            # Por ejemplo, podrías mostrar un mensaje de error al usuario
            messagebox.showerror("Error", "El valor ingresado no es un número entero válido")
    
        #actualizar si se ha puesto algo en el lotaje
        if self.stop_loss_entry.get() != "" and self.take_profit_entry.get() != "":
            self.actualizar_boton(event)

        #Actualizar vista
        self.on_parent_configure(event)

    def actualizar_take_profit(self, event):
        try:
            aux_profit = float(self.take_profit_entry.get())

            # Aquí puedes usar 'aux', que contendrá el valor convertido a entero
        except ValueError:
            # Si no se puede convertir a entero, se maneja la excepción aquí
            # Por ejemplo, podrías mostrar un mensaje de error al usuario
            messagebox.showerror("Error", "El valor ingresado no es un número entero válido")
    
        #actualizar si se ha puesto algo en el lotaje
        if self.take_profit_entry.get() != "" and self.stop_loss_entry.get() != "":
            self.actualizar_boton(event)

        #Actualizar vista
        self.on_parent_configure(event)

    def actualizar_boton(self, event):

        if self.boton_empezar_inversion is None:
            # Boton de "Empezar inversion"
            self.boton_empezar_inversion = tk.Button(self.frame_combo_boxs, text="Empezar\ninversión", font=("Aptos", 12), bg="green", fg="white", command=self.empezar_inversion) # wraplength determina el ancho máximo antes de que el texto se divida en dos líneas
            self.boton_empezar_inversion.grid(row=4, column=3, rowspan=2, padx=10, pady=2, sticky="w")

            if self.stop_loss_entry.get() == "" or self.take_profit_entry.get() == "":
                self.boton_empezar_inversion.configure(state="disabled")
        
        #Actualizar vista
        self.on_parent_configure(event)


    def crear_interfaz_inferior(self):
        # Frame para mostrar los datos
        self.frame_datos = tk.Frame(self.frame_inferior, bg=COLOR_CUERPO_PRINCIPAL, width=399)
        self.frame_datos.pack(fill=tk.BOTH, expand=True)

        # Label de "Rentabilidad"
        self.label_rentabilidad_clasica = tk.Label(self.frame_datos, text="Rentabilidad", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_clasica.pack(side="left", padx=(10, 0), pady=5)

        # Rentabilidad
        self.rentabilidad_clasica = tk.StringVar()
        self.rentabilidad_clasica.set("0")
        self.label_rentabilidad_clasica = tk.Label(self.frame_datos, textvariable=self.rentabilidad_clasica, font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_clasica.pack(side="left", padx=(0, 10), pady=5)



        # Boton de "Parar Inversión"
        self.boton_parar_inversion = tk.Button(self.frame_datos, text="Parar\ninversión", font=("Aptos", 12), bg="green", fg="white", command=self.parar_inversion) 
        self.boton_parar_inversion.pack(side="right", padx=(0, 10), pady=5)


        #Crear un widget Treeview
        self.tree_ticks = ttk.Treeview(self.frame_inferior)
        self.tree_ticks.pack(side="left", fill="x")
        

    def empezar_inversion(self):

        #Crear interfaz inferior
        self.crear_interfaz_inferior()

        self.tickdirecto()

        self.on_parent_configure(None)

    
    def treeview_ticks(self):
        self.current_frame2 = self.frame_ticks

        # Configurar las columnas del widget Treeview
        self.tree_ticks["columns"] = list(self.current_frame2.columns)
        self.tree_ticks["show"] = "headings"  # Desactivar la columna adicional
        for col in self.tree_ticks["columns"]:
            self.tree_ticks.heading(col, text=col)
            self.tree_ticks.column(col, width=100)

        # Limpiar el widget Treeview
        self.tree_ticks.delete(*self.tree_ticks.get_children())

        # Añadir todos los datos del DataFrame al widget Treeview
        for index, row in self.current_frame2.iterrows():
            self.tree_ticks.insert("", "end", values=tuple(row))


    def tickdirecto(self):
        frecuencia_txt = self.combo_frecuencia.get()
        accion_txt = self.combo_accion.get()
        estrategia = self.combo_estrategia.get()
        self.frec_milisegundos=self.calcular_frecuencia(frecuencia_txt)
        lotaje_txt = self.lotaje_entry.get()
        stoploss_txt= self.stop_loss_entry.get()
        takeprofit_txt=self.take_profit_entry.get()
        self.b.establecer_inversion_directo(frecuencia_txt, accion_txt,lotaje_txt,stoploss_txt,takeprofit_txt)

        if estrategia == 'RSI':
            self.b.thread_RSI_MACD()
        elif estrategia == 'Media Movil':
            self.b.thread_MediaMovil()
        elif estrategia == 'Bandas':
            self.b.thread_bandas()
        elif estrategia == 'Estocastico':
            self.b.thread_estocastico()

        self.b.thread_orders(estrategia)
        self.funciones_recursivas = True#se puedene ejecutar las funciones recursivas
        self.actualiar_frame()


    def calcular_frecuencia(self, frecuencia_txt):
        # Obtener valores de la frecuencia en segundos
        if frecuencia_txt == "1M":
            frecuencia = 20*1000
        elif frecuencia_txt == "3M":
            frecuencia = 180*1000
        elif frecuencia_txt == "5M":
            frecuencia = 300*1000
        elif frecuencia_txt == "10M":
            frecuencia = 600*1000
        elif frecuencia_txt == "15M":
            frecuencia = 900*1000
        elif frecuencia_txt == "30M":
            frecuencia = 1800*1000
        elif frecuencia_txt == "1H":
            frecuencia = 3600*1000
        elif frecuencia_txt == "2H":
            frecuencia = 7200*1000
        elif frecuencia_txt == "4H":
            frecuencia = 14400*1000
        elif frecuencia_txt == "Daily":
            frecuencia = 86400*1000
        elif frecuencia_txt == "Weekly":
            frecuencia = 604800*1000
        elif frecuencia_txt == "Monthly":
            frecuencia = 2592000*1000
        else:
            frecuencia = 0
        return frecuencia
   
    def actualiar_frame(self):
        if(self.funciones_recursivas):
            print("Operaciones")
            # if(ORD.FRAMETICKS.empty):
            #     self.frame_principal.after(10000, self.actualiar_frame)
            # else:    
            self.frame_ticks=ORD.FRAMETICKS
            self.treeview_ticks()
            self.frame_principal.after(self.frec_milisegundos, self.actualiar_frame)


    def parar_inversion(self):
        self.funciones_recursivas=False#paro la ejecucion de las funciones recursivas
        self.b.kill_threads()
        frame_inversiones_finalizadas=self.b.parar_inversion()
        self.frame_ticks=frame_inversiones_finalizadas
        self.treeview_ticks()

        rentabilidades = self.frame_ticks[self.frame_ticks['Rentabilidad'] != '-']['Rentabilidad']
        suma_rentabilidades = rentabilidades.sum().round(2)
        self.rentabilidad_clasica.set(str(suma_rentabilidades))
        self.label_rentabilidad_clasica.configure(textvariable=self.rentabilidad_clasica)



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
        self.label_titulo_clasicas.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.2), "bold"))

        #ajustar botones
        if self.boton_parar_inversion is not None:
            self.boton_parar_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_parar_inversion.configure(width=int(self.frame_width * 0.015))
        
        #Ajustar
        if self.label_mercado is not None:
            #Ajustar mercado
            self.label_mercado.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.combo_mercado.configure(width=int(self.frame_width * 0.02))
            
            #Ajustar accion
            if self.combo_accion is not None:
                self.label_accion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                self.combo_accion.configure(width=int(self.frame_width * 0.02))

                #Ajustar estrategia
                if self.combo_estrategia is not None:
                    self.label_estrategia.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                    self.combo_estrategia.configure(width=int(self.frame_width * 0.02))

                    #Ajustar frecuencia
                    if self.combo_frecuencia is not None:
                        self.label_frecuencia.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.combo_frecuencia.configure(width=int(self.frame_width * 0.02))
                        
                        #Ajustar lotaje
                        if self.lotaje_entry is not None:
                            self.label_lotaje.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.lotaje_entry.configure(width=int(self.frame_width * 0.02))
                            self.label_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            if self.lotaje_entry.get() != "":
                            #Habilitar el boton de empezar inversion
                                if self.boton_empezar_inversion is not None:
                                    self.boton_empezar_inversion.configure(state="normal")
                            if self.label_stop_loss is not None:
                                self.label_stop_loss.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                self.label_take_profit.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                self.stop_loss_entry.configure(width=int(self.frame_width * 0.02))
                                self.take_profit_entry.configure(width=int(self.frame_width * 0.02))

                        if self.boton_empezar_inversion is not None:
                            self.boton_empezar_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
                            self.boton_empezar_inversion.configure(width=int(self.frame_width * 0.015))



        
