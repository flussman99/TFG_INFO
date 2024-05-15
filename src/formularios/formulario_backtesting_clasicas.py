import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Canvas, Entry, Text, Button, PhotoImage
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


class FormularioBackTestingClasicas():

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
        self.label_titulo_clasicas = tk.Label(self.frame_superior, text="Backtesting Operaciones Clásicas", font=("Berlin Sans FB", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_titulo_clasicas.place(relx=0.05, rely=0.1)

        # Frame inferior (con scrollbar)
        self.frame_inferior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL, width=399, height=276)
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
        self.label_fecha_inicio = None
        self.label_fecha_fin = None
        self.fecha_inicio_entry = None
        self.fecha_fin_entry = None
        self.fecha_ini = datetime(year=2023, month=2, day=1)

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

        #ordenar acciones alfabeticamente
        filtered_acciones.sort()
        
        self.combo_accion['values'] = filtered_acciones

        #Ajustar vista
        self.on_parent_configure(event)

        #Actualizar vista al cambiar de accion        
        self.combo_accion.bind("<<ComboboxSelected>>", self.actualizar_estrategia)

    def actualizar_estrategia(self, event):
        
        #Label de "Elige estrategia"
        self.label_estrategia = tk.Label(self.frame_combo_boxs, text="Elige estrategia", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_estrategia.grid(row=0, column=2, padx=10, pady=2, sticky="w")

        #ComboBox de estrategia
        self.combo_estrategia = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_estrategia.grid(row=1, column=2, padx=10, pady=2, sticky="w")
        self.combo_estrategia["values"] = ['RSI', 'Media Movil', 'Bandas', 'Estocastico']
        
        #Actualizar vista al cambiar de estrategia        
        self.combo_estrategia.bind("<<ComboboxSelected>>", self.actualizar_fechas)

        #Ajustar vista
        self.on_parent_configure(event)

    def actualizar_fechas(self, event):

        if (self.fecha_inicio_entry is None):
            #Label fecha inicio
            self.label_fecha_inicio = tk.Label(self.frame_combo_boxs, text="Fecha inicio", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_fecha_inicio.grid(row=2, column=0, padx=10, pady=2, sticky="w")

            #label fecha fin
            self.label_fecha_fin = tk.Label(self.frame_combo_boxs, text="Fecha fin", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_fecha_fin.grid(row=2, column=1, padx=10, pady=2, sticky="w")

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
            self.fecha_inicio_entry.grid(row=3, column=0, padx=10, pady=2, sticky="w")

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
            self.fecha_fin_entry.grid(row=3, column=1, padx=10, pady=2, sticky="w")
        
        if self.label_frecuencia is None:
            #Frecuencia
            self.label_frecuencia = tk.Label(self.frame_combo_boxs, text="Elige la frecuencia", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_frecuencia.grid(row=2, column=2, padx=10, pady=2, sticky="w")

            #ComboBox de frecuencia
            self.combo_frecuencia = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_frecuencia.grid(row=3, column=2, padx=10, pady=2, sticky="w")
            self.combo_frecuencia["values"] = ['1M', '3M', '5M', '10M', '15M', '30M', '1H', '2H', '4H','Daily', 'Weekly', 'Monthly']

        #al mirar todos los datos actualizar el boton
        self.combo_frecuencia.bind("<<ComboboxSelected>>", self.actualizar_boton)

        #Ajustar vista
        self.on_parent_configure(event)


    def actualizar_boton(self, event):
        if self.boton_empezar_backtesting is not None:
            self.boton_empezar_backtesting.destroy()
            self.boton_empezar_backtesting = None
        # Boton de "Empezar backtesting"
        self.boton_empezar_backtesting = tk.Button(self.frame_combo_boxs, text="Empezar\nbacktesting", font=("Aptos", 12), bg="green", fg="white", command=self.empezar_backtesting) # wraplength determina el ancho máximo antes de que el texto se divida en dos líneas
        self.boton_empezar_backtesting.grid(row=2, column=3, rowspan=2, padx=10, pady=2, sticky="w")

        self.on_parent_configure(event)



    def crear_interfaz_inferior(self):
        # Frame para mostrar los datos
        self.frame_datos = tk.Frame(self.frame_inferior, bg=COLOR_CUERPO_PRINCIPAL, width=399)
        self.frame_datos.pack(fill=tk.BOTH, expand=True)

        # Label de "Rentabilidad"
        self.label_rentabilidad = tk.Label(self.frame_datos, text="Rentabilidad", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad.pack(side="left", padx=(10, 0), pady=5)

        # Rentabilidad
        self.rentabilidad_clasica = tk.StringVar()
        self.rentabilidad_clasica.set("0")
        self.label_rentabilidad_clasica = tk.Label(self.frame_datos, textvariable=self.rentabilidad_clasica, font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_clasica.pack(side="left", padx=(0, 10), pady=5)

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
        self.tree.pack(side="left", fill="x")

    def empezar_backtesting(self):

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
        self.coger_ticks()
    
    def coger_ticks(self):
        
        inicio_txt = self.fecha_inicio_entry.get()
        fin_txt = self.fecha_fin_entry.get()
        accion_txt = self.combo_accion.get()
        self.estrategia_txt = self.combo_estrategia.get()
        frecuencia_txt = self.combo_frecuencia.get()
        print("----------------------------------------")
        print("Inicio: ", inicio_txt)
        print("Fin: ", fin_txt)
        print("Accion: ", accion_txt)
        print("Estrategia: ", self.estrategia_txt)
        print("Frecuencia: ", frecuencia_txt)
        print("----------------------------------------")

        #Obtener los datos en un df
        self.b.establecer_frecuencia_accion(frecuencia_txt, accion_txt) 

        #if parte backtestin
        self.frame_without_filter, rentabilidad = self.b.thread_tick_reader(inicio_txt, fin_txt, self.estrategia_txt)
        print(self.frame_without_filter)

        #Actualizar rentabilidad
        self.rentabilidad_clasica.set(str(rentabilidad))
        self.label_rentabilidad_clasica.configure(textvariable=self.rentabilidad_clasica)

        #Mostrar la tabla
        self.treeview()

    def treeview(self):
        #Crear el otro frame para no tener que hacer otra llamada
        self.frame_with_filter = self.frame_without_filter[self.frame_without_filter['Decision'].isin(['Compra', 'Venta'])]
        # Set the initial DataFrame to display
        self.current_frame = self.frame_without_filter

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

    def toggle_frames(self):
        if self.current_frame.equals(self.frame_without_filter):
            self.current_frame = self.frame_with_filter
        else:
            self.current_frame = self.frame_without_filter

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
            
            # Si llegamos a este punto, el usuario ha introducido un nombre de inversión correcto
            break

        if(nombre_inversión is None):
            return

        # Le damos valor al tipo de inversión que esta haciendo el usuario
        tipo = "Backtesting " + self.combo_estrategia.get()

        # Cogemos la acción en la que ha invertido el usuario
        accion = self.combo_accion.get()

        # Cogemos la fecha de inicio y la de fin de la inversión
        fecha_ini = self.fecha_inicio_entry.get()
        fecha_fin = self.fecha_fin_entry.get()

        # Cogemos cuando se toman las decisiones de comprar y vender
        if tipo == 'Backtesting RSI':
            compra = "RSI < 35 y MACDI > MACSI"
            venta = "RSI > 65 y MACDI < MACSI"
        elif tipo == 'Backtesting Media Movil':
            compra = "MM c/p < MM l/p y nº compras < 10"
            venta = "MM c/p > MM l/p"
        elif tipo == 'Backtesting Bandas':
            compra = "Banda Inferior > Precio Compra"
            venta = "Banda Superior < Precio Compra y nº compras < 10"
        elif tipo == 'Backtesting Estocastico':
            compra = "Línea K > Línea D y RSI < 35 y nº compras < 10"
            venta = "Línea K < Línea D y RSI > 60"

        # Cogemos la frecuencia de la inversión
        frecuencia = self.combo_frecuencia.get()

        # Cogemos la rentabilidad de la inversión
        rentabilidad = str(self.rentabilidad_clasica.get()) + "%"

        # Aquí no se aplica la rentabilidad de los índices
        rentabilidad_ibex = "No aplica"
        rentabilidad_sp500 = "No aplica"
        rentabilidad_plazos = "No aplica"
        
        # Guardamos la inversión en la base de datos
        cursor = self.conn.cursor()
        try:
            # Realizamos la consulta para insertar los datos en la tabla Inversiones
            consulta = "INSERT INTO Inversiones (id_usuario, nombre, tipo, accion, fecha_inicio, fecha_fin, compra, venta, frecuencia, rentabilidad, rentabilidad_ibex, rentabilidad_sp, rentabilidad_plazos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            datos = (self.id_user, nombre_inversión, tipo, accion, fecha_ini, fecha_fin, compra, venta, frecuencia ,rentabilidad, rentabilidad_ibex, rentabilidad_sp500, rentabilidad_plazos)
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
        print ("Estrategia: ", self.estrategia_txt)
        print("-------------------ESTRAREFA---------------------")
        FormularioBackTestingMasInformacion(self.frame_principal, self.frame_without_filter, self.estrategia_txt, self.rentabilidad_clasica.get())

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
        if self.boton_guardar_backtesting is not None:
            self.boton_guardar_backtesting.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_mostrar_operaciones.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_mas_informacion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_guardar_backtesting.configure(width=int(self.frame_width * 0.01))
            self.boton_mostrar_operaciones.configure(width=int(self.frame_width * 0.01))
            self.boton_mas_informacion.configure(width=int(self.frame_width * 0.01))
        
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

                    if self.label_fecha_inicio is not None:
                        self.label_fecha_inicio.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.label_fecha_fin.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.fecha_inicio_entry.configure(width=int(self.frame_width * 0.02))
                        self.fecha_fin_entry.configure(width=int(self.frame_width * 0.02))

                    #Ajustar frecuencia
                    if self.combo_frecuencia is not None:
                        self.label_frecuencia.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.combo_frecuencia.configure(width=int(self.frame_width * 0.02))
                        
                        if self.boton_empezar_backtesting is not None:
                            self.boton_empezar_backtesting.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
                            self.boton_empezar_backtesting.configure(width=int(self.frame_width * 0.02))



        
