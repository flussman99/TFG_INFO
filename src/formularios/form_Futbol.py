import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Entry, Text, Button, PhotoImage, Checkbutton, IntVar, Label
from PIL import Image, ImageDraw, ImageTk
from datetime import datetime, timedelta
import pandas as pd
import sys
import os
from bot import Bot as bt
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime
from Formula1 import SF1_backtesting
from EquiposdeFutbol import SBS_backtesting as SBS

from config import COLOR_CUERPO_PRINCIPAL
"from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL , COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA"


class FormularioFutbol(tk.Toplevel):
   
    def __init__(self, panel_principal):


        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.grid(row=0, column=0, sticky="nsew")

        panel_principal.grid_rowconfigure(0, weight=1)
        panel_principal.grid_columnconfigure(0, weight=1) 

        self.cuerpo_principal = tk.Frame(panel_principal, width=1366, height=667)
        self.cuerpo_principal.grid(row=1, column=0, sticky="nsew")

        panel_principal.grid_rowconfigure(1, weight=1)  
        panel_principal.grid_columnconfigure(0, weight=1)


        canvas = Canvas(
            self.cuerpo_principal,
            bg = "#FFFFFF",
            height = 663,
            width = 1366,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        image_image_1 = PhotoImage(
            file="src/imagenes/assets/fondo.png")
        image_1 = canvas.create_image(
            683.0,
            331.0,
            image=image_image_1
        )
 

        self.b = bt(1) #como mejorarlo?
        # Lista de opciones para el ComboBox
        # acciones, mercados = self.b.get_trading_data()
      

        self.estrategia='Futbol'
        self.pais_asoc = None  # or any default value you want
        self.url_asoc = None  # or any default value you want
        self.acronimo_api=None
        self.acronimo_mt5=None
        self.frame_without_filter=None
        self.current_frame = None
        self.frame_with_filter=None
        self.frame_directo=None
        
        ligas=SBS.ligas
        acciones=SBS.acciones
        pais=SBS.pais
        url=SBS.urls_equipos
        acronimos_acciones_api=SBS.acronimo_acciones_api
        acronimos_acciones_mt5=SBS.acronimo_acciones_mt5
        imagenes_liga=SBS.imagenes_ligas
        imagenes_equipos=SBS.imagenes_equipos

        self.ligas_var = tk.StringVar(value=list(ligas.keys()))
        self.combo_ligas = ttk.Combobox(canvas, textvariable=self.ligas_var, values=list(ligas.keys()))
        self.combo_ligas.place(x=34.0, y=19.0, width=300, height=38.0)
        self.combo_ligas.current(0)
        self.combo_ligas.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
        
        self.equipos_var = tk.StringVar()
        self.combo_equipos = ttk.Combobox(canvas, textvariable=self.equipos_var)
        self.combo_equipos.place(x=334.0, y=19.0, width=300, height=38.0)
        # self.combo_equipos.current(0)
        self.combo_equipos.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
        

        self.acciones_var = tk.StringVar()
        self.combo_acciones = ttk.Combobox(canvas, textvariable=self.acciones_var)
        self.combo_acciones.place(x=634.0, y=19.0, width=300, height=38.0)  # Ajusta la posición y el tamaño según sea necesario
        # self.combo_acciones.current(0)
        self.combo_acciones.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        def actualizar_equipos(event):
            liga_seleccionada = self.combo_ligas.get()
            equipos_liga = ligas[liga_seleccionada]
            # imagen = imagenes_liga[liga_seleccionada]
            # print(imagen)
            
            # # Delete the previous image label if it exists
            # if hasattr(self, 'image_label'):
            #     self.image_label.destroy()
            
            # # Create a new image label with the selected image
            # self.image_label = tk.Label(canvas, image=imagen)
            # self.image_label.place(x=934.0, y=19.0)  # Adjust the position and size as needed
            
            self.combo_equipos['values'] = equipos_liga
            self.combo_equipos.current(0) 
            actualizar_acciones(None)
        
        def actualizar_pais_url_acronimo(event):
            self.pais_asoc = obtener_pais()
            self.url_asoc = obtener_url()
            self.acronimo_api, self.acronimo_mt5 = obtener_acronimo()
    
            
        def actualizar_acciones(event):
            equipo_seleccionado = self.combo_equipos.get()
            imagen= imagenes_equipos[equipo_seleccionado]
            nombres_acciones_equipo = acciones.get(equipo_seleccionado, [])
            accion_previa = self.combo_acciones.get()
            self.combo_acciones['values'] = nombres_acciones_equipo
            if accion_previa in nombres_acciones_equipo:
                self.combo_acciones.set(accion_previa)
            else:
                self.combo_acciones.current(0)
            actualizar_pais_url_acronimo(None) #Pra que actue con la inicializacion del programa 
            self.combo_acciones.bind("<<ComboboxSelected>>", actualizar_pais_url_acronimo) #cuando un equipo tiene varias acciones se actualiza a la nueva seleccionada


        def obtener_acronimo():
            accion_seleccionada = self.combo_acciones.get()
            acronimo_seleccionado_api = acronimos_acciones_api.get(accion_seleccionada)
            acronimo_sleccionado_mt5 = acronimos_acciones_mt5.get(accion_seleccionada)
            # print(acronimo_seleccionado)
            return acronimo_seleccionado_api, acronimo_sleccionado_mt5

        def obtener_pais():
            acronimo_seleccionado_api,acronimo_mt5 = obtener_acronimo()
            pais_seleccionado = pais.get(acronimo_seleccionado_api)
            # print(pais_seleccionado)  # Imprime el país seleccionado
            return pais_seleccionado

        def obtener_url():
            equipo_seleccionado = self.combo_equipos.get()
            url_equipo = url.get(equipo_seleccionado)
            # print(url_equipo)  # Imprime la URL del equipo seleccionado
            return url_equipo


        self.combo_ligas.bind('<<ComboboxSelected>>', actualizar_equipos)
        self.combo_equipos.bind('<<ComboboxSelected>>', actualizar_acciones)

        def actualizar_vender(event):
            # Obtén el valor seleccionado en 'comprar'
            comprar_seleccionado = self.comprar_var.get()

            # Define los posibles valores para 'vender'
            valores = ['Ganado', 'Empatado', 'Perdido', "Ganado/Empatado", "Ganado/Perdido", "Empatado/Perdido"]

            # Elimina el valor seleccionado en 'comprar' de los posibles valores para 'vender'
            valores.remove(comprar_seleccionado)

            # Actualiza los valores disponibles en 'vender'
            self.combo_vender['values'] = valores

        def actualizar_comprar(event):
            # Obtén el valor seleccionado en 'vender'
            vender_seleccionado = self.vender_var.get()

            # Define los posibles valores para 'comprar'
            valores = ['Ganado', 'Empatado', 'Perdido', "Ganado/Empatado", "Ganado/Perdido", "Empatado/Perdido"]

            # Elimina el valor seleccionado en 'vender' de los posibles valores para 'comprar'
            valores.remove(vender_seleccionado)

            # Actualiza los valores disponibles en 'comprar'
            self.combo_comprar['values'] = valores

        self.titulos_comprar = ttk.Label(self.cuerpo_principal, text="Seleccione cuando comprar:")
        self.titulos_comprar.place(x=34.0, y=96, width=200, height=38.0)
        self.titulos_comprar.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
        
        # Crea el combobox 'comprar'
        self.comprar_var = tk.StringVar()
        self.combo_comprar = ttk.Combobox(canvas, textvariable=self.comprar_var, values=['Ganado', 'Empatado', 'Perdido', "Ganado/Empatado", "Ganado/Perdido", "Empatado/Perdido"])
        self.combo_comprar.place(x=34.0, y=131.0, width=200, height=38.0)
        self.combo_comprar.current(0)
        self.combo_comprar.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        # Vincula la función 'actualizar_vender' a la selección de un valor en 'comprar'
        self.combo_comprar.bind('<<ComboboxSelected>>', actualizar_vender)


        self.titulo_vender = ttk.Label(self.cuerpo_principal, text="Seleccione cuando Vender:")
        self.titulo_vender.place(x=34.0, y=189, width=200, height=38.0)
        self.titulo_vender.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        # Crea el combobox 'vender'
        self.vender_var = tk.StringVar()
        self.combo_vender = ttk.Combobox(canvas, textvariable=self.vender_var, values=['Ganado', 'Empatado', 'Perdido', "Ganado/Empatado", "Ganado/Perdido", "Empatado/Perdido"])
        self.combo_vender.place(x=34.0, y=224.0, width=200, height=38.0)
        self.combo_vender.current(0)
        self.combo_vender.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        # Vincula la función 'actualizar_comprar' a la selección de un valor en 'vender'
        self.combo_vender.bind('<<ComboboxSelected>>', actualizar_comprar)

        actualizar_vender(None)
        actualizar_comprar(None)
        actualizar_equipos(None)

        self.titulo_fecha_inicio = ttk.Label(self.cuerpo_principal, text="Seleccione la fecha Inicial:")
        self.titulo_fecha_inicio.place(x=270.0, y=96, width=200, height=38.0)
        self.titulo_fecha_inicio.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        fecha_ayer = datetime.now() - timedelta(days = 1)

        self.fecha_inicio_entry = DateEntry(
            canvas, 
            date_pattern='yyyy/mm/dd',
            background='darkblue', 
            foreground='white', 
            borderwidth=2,
            maxdate=fecha_ayer
        )
        self.fecha_inicio_entry.place(
            x=270.0,
            y=131.0,
            width=200.0,
            height=38.0
        )

        self.titulo_fecha_fin = ttk.Label(self.cuerpo_principal, text="Seleccione la fecha Final:")
        self.titulo_fecha_fin.place(x=270.0, y=189, width=200, height=38.0)
        self.titulo_fecha_fin.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
        
        self.fecha_fin_entry = DateEntry(
            canvas, 
            date_pattern='yyyy/mm/dd',
            background='darkblue', 
            foreground='white', 
            borderwidth=2,
            maxdate=fecha_ayer
        )
        self.fecha_fin_entry.place(
            x=270.0,
            y=224.0,
            width=200.0,
            height=38.0
        )


        button_image_backtesting = PhotoImage(
            file="src/imagenes/assets/boton_comun_mkt.png")
        button_backtesting = Button(
            canvas,
            text="Backtesting",
            fg="#FFFFFF",
            image=button_image_backtesting,
            borderwidth=0,
            highlightthickness=0,
            command=self.coger_ticks,
            compound=tk.CENTER,
            font=("Calistoga Regular", 12)
        )
        
        button_window = canvas.create_window(650, 103, anchor='nw', window=button_backtesting, width=196, height=38)

        button_image_directo = PhotoImage(
            file="src/imagenes/assets/boton_cantidad_operaciones.png")
        button_directo = Button(
            canvas,
            text="Ticks en directo",
            fg="#FFFFFF",
            image=button_image_directo,
            borderwidth=0,
            highlightthickness=0,
            command=self.tickdirecto,
            compound=tk.CENTER,
            font=("Calistoga regular", 12)
        )
        button_directo.place(
            x=904.0,
            y=103.0,
            width=305.0,
            height=38.0
        )


        self.rentabilidad_futbol = tk.StringVar()
        self.rentabilidad_futbol.set("0")

        self.rentabilidad_label = tk.Label(self.cuerpo_principal, textvariable=self.rentabilidad_futbol)

        self.rentabilidad_indicador_futbol = tk.StringVar()
        self.rentabilidad_indicador_futbol.set("0")

        self.rentabilidad_label_indicador = tk.Label(self.cuerpo_principal, textvariable=self.rentabilidad_indicador_futbol)
        # self.rentabilidad_label.place(x=35, y=300)
        def toggle_frames():
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
        
        # Crear el botón
        self.operaciones_button = ttk.Button(self.cuerpo_principal, text="Mostrar Operaciones", command=toggle_frames)
        # self.operaciones_button.place(x=270, y=300)  # Ajusta las coordenadas x e y según sea necesario

        # Crear el widget Treeview
        self.tree = ttk.Treeview(self.cuerpo_principal)
        # Añadir el widget Treeview al formulario
        # Añadir el widget Treeview al formulario en una ubicación específica
        # self.tree.place(x=35, y=350, width=1300)


        button_image_16 = PhotoImage(
            file="src/imagenes/assets/boton_comun_lim_stop_key.png")
        button_16 = Button(
            canvas,
            text="Parar ticks",
            fg="#FFFFFF",
            image=button_image_16,
            borderwidth=0,
            highlightthickness=0,
            command=self.pararTicksDirecto,
            compound=tk.CENTER,
            font=('Calistoga Regular', 12)
        )
        button_16.place(
            x=1234.0,
            y=103.0,
            width=98.0,
            height=38.0
        )
        self.cuerpo_principal.mainloop()

        button_window = canvas.create_window(650, 103, anchor='nw', window=button_16, width=196, height=38)
        

    def visualizar(self):
        # Hacer visible el botón, label y widget
        self.operaciones_button.place(x=270, y=300)
        self.rentabilidad_label.place(x=35, y=300)
        self.rentabilidad_label_indicador.place(x=100, y=300)
        self.tree.place(x=35, y=350, width=1300)

    def treeview(self,modo):
        if(modo=="Backtesting"):
            self.frame_with_filter = self.frame_without_filter[self.frame_without_filter['Decision'].isin(['1', '-1'])]

            # Set the initial DataFrame to display
            self.current_frame = self.frame_without_filter
        else:
            self.current_frame = self.frame_directo

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
        accion_txt = self.acronimo_api
        estrategia_txt = self.estrategia
        pais_txt = self.pais_asoc
        url_txt = self.url_asoc
        frecuencia_txt = "Daily"
        cuando_comprar = self.combo_comprar.get()
        cuando_vender = self.combo_vender.get()
       
        print(equipo_txt, accion_txt, pais_txt, url_txt)
        self.b.establecer_frecuencia_accion(frecuencia_txt, accion_txt) #le pasamos el acronimo de la API para el backtesting que es de donde importo los datos
        self.frame_without_filter, rentabilidad, rentabilidad_indicador = self.b.thread_creativas(inicio_txt, fin_txt, pais_txt, url_txt, estrategia_txt, cuando_comprar, cuando_vender, equipo_txt)
        self.rentabilidad_futbol.set(str(rentabilidad))

        self.rentabilidad_indicador_futbol.set(str(rentabilidad_indicador))

        self.visualizar()
        self.treeview("Backtesting")
        
       
    def pararTicksDirecto(self):
        self.b.kill_threads()
    
    def tickdirecto(self):
        cuando_comprar = self.combo_comprar.get()
        cuando_vender = self.combo_vender.get()
        accion_txt = self.acronimo_mt5
        url_txt = self.url_asoc
        estrategia_txt = self.estrategia
        equipo_txt = self.combo_equipos.get()
        frecuencia_txt = "Daily"
        print(equipo_txt, accion_txt, estrategia_txt,url_txt)
        self.b.establecer_frecuencia_accion(frecuencia_txt, accion_txt)#le pasamos el acronimo de MT5 que es donde invierto
        self.frame_directo=self.b.thread_Futbol(equipo_txt, url_txt, cuando_comprar,cuando_vender)
        self.b.thread_orders(estrategia_txt)

        self.visualizar()
        self.treeview("Directo")
    
