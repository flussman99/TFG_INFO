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
from formularios.formulario_mas_informacion import FormularioBackTestingMasInformacion


class FormularioBackTestingCine():

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
        self.label_titulo_futbol = tk.Label(self.frame_superior, text="Backtesting Operaciones Cine", font=("Berlin Sans FB", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
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
        self.label_rentabilidad_cine = None
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
        self.url = 'src/Disney/html/Disney_Pelis_2010_2024.csv'

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
        self.boton_empezar_backtesting = tk.Button(self.frame_combo_boxs, text="Empezar\nbacktesting", font=("Aptos", 12), bg="green", fg="white", command=self.empezar_backtesting) # wraplength determina el ancho máximo antes de que el texto se divida en dos líneas
        self.boton_empezar_backtesting.grid(row=4, column=3, rowspan=2, padx=10, pady=2, sticky="w")

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
        self.rentabilidad_cine = tk.StringVar()
        self.rentabilidad_cine.set("0")
        self.label_rentabilidad_cine = tk.Label(self.frame_datos, textvariable=self.rentabilidad_cine, font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_cine.pack(side="left", padx=(0, 10), pady=5)

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
        self.tree.pack(side="left", fill="x", expand=True)

        #Actualizar vista
        self.on_parent_configure(None)

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

    def empezar_backtesting(self):
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
        self.coger_ticks()

        #Ajustar vista
        self.on_parent_configure(None)

    def coger_ticks(self):
        
        frecuencia_txt = "Daily"
        inicio_txt = self.fecha_inicio_entry.get()
        fin_txt = self.fecha_fin_entry.get()
        estrategia_txt = 'Disney'
        estudio_txt = self.estudio
        pais_txt = 'united states'
        cuando_comprar = self.combo_metodos_comprar.get()
        accion = self.label_accion.cget('text').split(".")
        accion_txt = accion[0]
        indicador= self.combo_comparativa.get()


        print("----------------------------------------")
        print(frecuencia_txt, accion_txt, inicio_txt, fin_txt, estrategia_txt)

        self.b.establecer_frecuencia_accion(frecuencia_txt, accion_txt) 
        self.frame_without_filter, rentabilidad, rentabilidad_indicador = self.b.thread_creativas(inicio_txt,fin_txt,pais_txt,self.url,estrategia_txt, cuando_comprar, cuando_comprar, estudio_txt, indicador)#pasas un vacio pq no necesitas ese valor sin ambargo en la del futbol si
        
        self.establecerRentabilidades(rentabilidad, rentabilidad_indicador)
        self.treeview()

    def establecerRentabilidades(self, rentabilidad, rentabilidad_indicador):
        #Rentabilidad Futbol
        self.rentabilidad_cine.set(str(rentabilidad))
        self.label_rentabilidad_cine.configure(textvariable=self.rentabilidad_cine)

        #Rentabilidad comparativa    
        self.rentabilidad_comparativa.set(str(rentabilidad_indicador))
        self.label_rentabilidad_comparativa.configure(textvariable=self.rentabilidad_comparativa)
        
   

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
        rentabilidad = self.rentabilidad_cine.get()
        # Cogemos la rentabilidad de la inversión#SEGOVIAN TIENES QUE HACER EL INSERT TB DE ESTO
        rentabilidadIndicador = self.rentabilidad_comparativa.get()

        # Guardamos la inversión en la base de datos
        cursor = self.conn.cursor()
        try:
            # Realizamos la consulta para insertar los datos en la tabla Inversiones
            consulta = "INSERT INTO Inversiones (id_usuario, nombre, tipo, accion, fecha_inicio, fecha_fin, compra, venta, frecuencia, rentabilidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            datos = (self.id_user, nombre_inversión, tipo, accion, fecha_ini, fecha_fin, compra, venta, frecuencia ,rentabilidad)
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
        FormularioBackTestingMasInformacion(self.frame_principal, self.frame_without_filter, "Futbol", self.rentabilidad_cine.get())

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
            self.label_rentabilidad_cine.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.12)))
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
                    #destruir imagen estudio
                    if self.label_imagen_estudio is not None:
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
        
