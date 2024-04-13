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
from EquiposdeFutbol.SBS_backtesting import SBSBacktesting as SBS
from config import COLOR_CUERPO_PRINCIPAL
"from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL , COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA"

# SBS_backtesting=SBS_backtesting()

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
        self.sbs_backtesting=SBS()

        self.estrategia='Futbol'
        ligas=self.sbs_backtesting.ligas
        ligas = self.sbs_backtesting.ligas
        acciones=self.sbs_backtesting.acciones
        pais=self.sbs_backtesting.pais
        url=self.sbs_backtesting.urls_equipos

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
            self.combo_equipos['values'] = equipos_liga
            self.combo_equipos.current(0)
            
            
            actualizar_acciones(None)

        def actualizar_acciones(event):
            equipo_seleccionado = self.combo_equipos.get()
            acciones_equipo = acciones.get(equipo_seleccionado, [])
            self.combo_acciones['values'] = acciones_equipo
            if acciones_equipo:
                self.combo_acciones.current(0)
                self.pais_asoc=obtener_pais()
                self.url_asoc=obtener_url()
                
    
        def obtener_pais():
            accion_seleccionada = self.combo_acciones.get()
            pais_seleccionado = pais.get(accion_seleccionada)
            print(pais_seleccionado)  # Imprime el país seleccionado
            return pais_seleccionado

        def obtener_url():
            equipo_seleccionado = self.combo_equipos.get()
            url_equipo = url.get(equipo_seleccionado)
            print(url_equipo)  # Imprime la URL del equipo seleccionado
            return url_equipo


        self.combo_ligas.bind('<<ComboboxSelected>>', actualizar_equipos)
        self.combo_equipos.bind('<<ComboboxSelected>>', actualizar_acciones)

        
        
       
        

        def actualizar_vender(event):
            # Obtén el valor seleccionado en 'comprar'
            comprar_seleccionado = self.comprar_var.get()

            # Define los posibles valores para 'vender'
            valores = ['Ganado', 'Empatado', 'Perdido']

            # Elimina el valor seleccionado en 'comprar' de los posibles valores para 'vender'
            valores.remove(comprar_seleccionado)

            # Actualiza los valores disponibles en 'vender'
            self.combo_vender['values'] = valores

        def actualizar_comprar(event):
            # Obtén el valor seleccionado en 'vender'
            vender_seleccionado = self.vender_var.get()

            # Define los posibles valores para 'comprar'
            valores = ['Ganado', 'Empatado', 'Perdido']

            # Elimina el valor seleccionado en 'vender' de los posibles valores para 'comprar'
            valores.remove(vender_seleccionado)

            # Actualiza los valores disponibles en 'comprar'
            self.combo_comprar['values'] = valores

        self.titulos_comprar = ttk.Label(self.cuerpo_principal, text="Seleccione cuando comprar:")
        self.titulos_comprar.place(x=34.0, y=284, width=200, height=38.0)
        self.titulos_comprar.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        # Crea el combobox 'comprar'
        self.comprar_var = tk.StringVar()
        self.combo_comprar = ttk.Combobox(canvas, textvariable=self.comprar_var, values=['Ganado', 'Empatado', 'Perdido'])
        self.combo_comprar.place(x=34.0, y=322.0, width=200, height=38.0)
        self.combo_comprar.current(0)
        self.combo_comprar.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        # Vincula la función 'actualizar_vender' a la selección de un valor en 'comprar'
        self.combo_comprar.bind('<<ComboboxSelected>>', actualizar_vender)


        self.titulo_vender = ttk.Label(self.cuerpo_principal, text="Seleccione cuando Vender:")
        self.titulo_vender.place(x=240.0, y=284, width=200, height=38.0)
        self.titulo_vender.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        # Crea el combobox 'vender'
        self.vender_var = tk.StringVar()
        self.combo_vender = ttk.Combobox(canvas, textvariable=self.vender_var, values=['Ganado', 'Empatado', 'Perdido'])
        self.combo_vender.place(x=240.0, y=322.0, width=200, height=38.0)
        self.combo_vender.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        # Vincula la función 'actualizar_comprar' a la selección de un valor en 'vender'
        self.combo_vender.bind('<<ComboboxSelected>>', actualizar_comprar)


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
        # button_6.bind("<Button-1>", lambda event: seleccionar_años())



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



        button_image_start = PhotoImage(
            file="src/imagenes/assets/boton_comun_mkt.png")
        button_start = Button(
            canvas,
            text="Iniciar estrategia",
            fg="#FFFFFF",
            image=button_image_start,
            borderwidth=0,
            highlightthickness=0,
            command=self.lanzarEstrategia,
            compound=tk.CENTER,
            font=("Calistoga Regular", 12)
        )

        self.rentabilidad_label = Label(self.cuerpo_principal, text="")
        self.rentabilidad_label.place(x=100, y=100)  # Coloca la etiqueta en la posición que desees

        button_window = canvas.create_window(650, 187, anchor='nw', window=button_start, width=197, height=38)
        # button_8.bind("<Button-1>", lambda event: seleccionar_años())
    

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

        self.rentabilidad_label = Label(self.cuerpo_principal, text="")
        self.rentabilidad_label.place(x=100, y=100)  # Coloca la etiqueta en la posición que desees
        

        def borrar_texto(event):
            text_box = event.widget
            text_box.delete(0, tk.END)

        def reescribir_texto(event):
            text_box = event.widget

            if text_box.get() == '':
                if text_box == self.entry_fin_back:
                    self.entry_fin_back.insert(0, self.texto_fin_back)
                elif text_box == self.entry_lotaje:
                    self.entry_lotaje.insert(0, self.texto_lotaje)

    def mostrar_rentabilidad(self):
        rentabilidad_total = self.sbs_backtesting.obtener_rentabilidad_total()
        self.rentabilidad_label.config(text=str(rentabilidad_total))


        
    
    def tickdirecto(self):
        
        self.b.thread_orders(self.estrategia)
        

        

    def getPrice(self):
        piloto_txt = self.combo_piloto.get()
        accion_txt = self.combo_acciones.get()
        estrategia=self.combo_años.get()

    
    def lanzarEstrategia(self):
        piloto_txt = self.combo_piloto.get()
        accion_txt = self.combo_acciones.get()
        estrategia=self.combo_años.get()

    def pararTicksDirecto(self):
        piloto_txt = self.combo_piloto.get()
        accion_txt = self.combo_acciones.get()
        estrategia=self.combo_años.get()

    
    def coger_ticks(self):
        inicio_txt = self.fecha_inicio_entry.get()
        fin_txt = self.fecha_fin_entry.get()
        equipo_txt = self.combo_equipos.get()
        accion_txt = self.combo_acciones.get()
        estrategia_txt=self.estrategia
        pais_txt=self.pais_asoc
        url_txt=self.url_asoc
        frecuencia_txt = "Daily"
        cuando_comprar = self.combo_comprar.get()
        cuando_vender = self.combo_vender.get()
        print(equipo_txt, accion_txt, pais_txt, url_txt)

        self.b.establecer_frecuencia_accion(frecuencia_txt, accion_txt) 

        self.b.thread_Futbol(inicio_txt, fin_txt,pais_txt,url_txt,estrategia_txt, cuando_comprar, cuando_vender,equipo_txt)
        self.mostrar_rentabilidad()

    
    