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
from config import COLOR_CUERPO_PRINCIPAL
"from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL , COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA"


class FormularioFormula1(tk.Toplevel):
   
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
        acciones, mercados = self.b.get_trading_data()



        def filter_options(event):

            combobox = event.widget
            options = combobox.cget('values')
            data = combobox.get().upper()

            if combobox == self.combo_acciones:
                options = self.original_acciones
            elif combobox == self.combo_mercados:
                options = self.original_mercados  
            elif combobox == self.combo_piloto:
                options = self.original_piloto 
            elif combobox == self.combo_años:
                options = self.original_años 

            if data:
                # Filter the options
                filtered_options = [option for option in options if option.startswith(data)]
            else:
                # If the data is empty, reset the options to the original list
                filtered_options = options

            combobox['values'] = filtered_options

            if hasattr(filter_options, 'job'):
                canvas.after_cancel(filter_options.job)

            # Schedule a new job
            filter_options.job = canvas.after(2000, combobox.event_generate, '<Down>')


        def filter_acciones(event):
            # Get selected market
            selected_market = self.combo_mercados.get().upper()

            if selected_market == 'DIVISES':
                selected_market = ''
                filtered_acciones = [accion for accion in acciones if '.' not in accion]
            else:
                filtered_acciones = [accion for accion in acciones if accion.endswith(selected_market)]

            # Update combo_acciones options
            self.combo_acciones['values'] = filtered_acciones
            self.combo_acciones.set(filtered_acciones[0])
        
        def filter_pilotos(event):
            # Get selected market
            selected_year = self.combo_años.get().upper()
            # Update combo_acciones options
            self.combo_piloto['values'] = SF1_backtesting.obtener_listado_pilotos(selected_year)
            self.combo_piloto.current(0)
            seleccionar_accion(event)


        # Función para manejar la selección en el ComboBox
        def seleccionar_accion(event):
            selected_pilot = self.combo_piloto.get()
            año = self.combo_años.get()

            self.combo_acciones.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
            
            accion = SF1_backtesting.obtener_accion_escuderia(selected_pilot, año)
            self.combo_acciones.set(accion)
            mercado = accion.split('.')[1]
            self.combo_mercados.set(mercado)


        def reload_options(event):
            # Get the combobox that triggered the event
            combobox = event.widget

            # Reset the values of the combobox
            if combobox == self.combo_acciones:
                combobox['values'] = self.original_acciones
            elif combobox == self.combo_mercados:
                combobox['values'] = self.original_mercados  
            elif combobox == self.combo_piloto:
                combobox['values'] = self.original_piloto 
            elif combobox == self.combo_años:
                combobox['values'] = self.original_años


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

        self.estrategia = ''

        def on_checkbox_click(checkbox):
            if checkbox == checkbox_1:
                checkbox_podio.deselect()
                checkbox_5.deselect()
                checkbox_puntos.deselect()
                self.estrategia = "Primero"
            elif checkbox == checkbox_podio:
                checkbox_1.deselect()
                checkbox_5.deselect()
                checkbox_puntos.deselect()
                self.estrategia = "Podio"
            elif checkbox == checkbox_5:
                checkbox_1.deselect()
                checkbox_podio.deselect()
                checkbox_puntos.deselect()
                self.estrategia = "Top 5"
            elif checkbox == checkbox_puntos:
                checkbox_1.deselect()
                checkbox_podio.deselect()
                checkbox_5.deselect()
                self.estrategia = "Puntos"



        self.mercados_var = tk.StringVar(value=mercados)
        self.combo_mercados = ttk.Combobox(canvas, textvariable=self.mercados_var, values=mercados)
        self.combo_mercados.place(x=34.0, y=19.0, width=640, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_mercados.current(0)  # Establece la opción por defecto
        self.combo_mercados.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        self.original_mercados = mercados


        # Función para manejar la selección en el ComboBox
        def seleccionar_mercado(event):
            selected_item = self.mercados_var.get()
            print("Opción seleccionada:", selected_item)
            self.combo_mercados.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
            # hay que hacer que se muestre la info del mercado seleccionado

        self.combo_mercados.bind("<<ComboboxSelected>>", seleccionar_mercado)  # Asocia la función al evento de selección del ComboBox
        self.combo_mercados.bind('<<ComboboxSelected>>', filter_acciones)
        self.combo_mercados.bind('<KeyRelease>', filter_options)


        self.acciones_var = tk.StringVar(value=acciones)
        self.combo_acciones = ttk.Combobox(canvas, textvariable=self.acciones_var, values=acciones)
        self.combo_acciones.place(x=684.0, y=19.0, width=640, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_acciones.current(0)  # Establece la opción por defecto
        self.combo_acciones.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        self.original_acciones = acciones


        self.combo_acciones.bind('<KeyRelease>', filter_options)
        #self.combo_acciones.bind('<KeyRelease>', seleccionar_acciones) SI HAY DOS FUNCIONES PETA
        self.combo_acciones.bind('<<ComboboxSelected>>', reload_options)



        button_image_2 = PhotoImage(
            file="src/imagenes/assets/boton_grafico_operaciones.png")
        button_2 = Button(
            canvas,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=34.0,
            y=334.0,
            width=1298.0,
            height=309.0
        )


        entry_image_1 = PhotoImage(
            file="src/imagenes/assets/entry_fondo_operaciones.png")
        entry_bg_1 = canvas.create_image(
            683.0,
            300.0,
            image=entry_image_1
        )

        canvas.create_text(42, 284, anchor="nw", text="Cartera: ", fill="white", font=("Calistoga Regular", 12))
        canvas.create_text(310, 284, anchor="nw", text="Gan. latente: ", fill="white", font=("Calistoga Regular", 12))
        canvas.create_text(617, 284, anchor="nw", text="Gan. día: ", fill="white", font=("Calistoga Regular", 12))
        canvas.create_text(865, 284, anchor="nw", text="Órdenes: ", fill="white", font=("Calistoga Regular", 12))
        canvas.create_text(1090, 284, anchor="nw", text="Posición: ", fill="white", font=("Calistoga Regular", 12))
        

        años = SF1_backtesting.obtener_listado_años()
        self.años_var = tk.StringVar(value=años)
        self.combo_años = ttk.Combobox(canvas, textvariable=self.años_var, values=años)
        self.combo_años.place(x=34.0, y=103.0, width=258.0, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_años.current(0)  # Establece la opción por defecto
        self.combo_años.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        self.original_años = años

        self.combo_años.bind("<<ComboboxSelected>>", filter_pilotos)
        # self.combo_años.bind("<<ComboboxSelected>>", seleccionar_accion)
        self.combo_años.bind('<KeyRelease>', filter_options)


        canvas.create_text(349, 187, anchor="nw", text="Op. de inversión:", fill="white", font=("Calistoga Regular", 12))



        fecha_ayer = datetime.now() - timedelta(days = 1)   

        self.entry_inicio_back = DateEntry(
            canvas, 
            date_pattern='yyyy/mm/dd',
            background="#30a4b4", 
            foreground="#FFFFFF",
            font=('Calistoga Regular', 12),
            borderwidth=2,
            maxdate=fecha_ayer
        )
        self.entry_inicio_back.place(
            x=349.0,
            y=103.0,
            width=94.0,
            height=38.0
        )


        self.entry_fin_back = DateEntry(
            canvas, 
            date_pattern='yyyy/mm/dd',
            background="#30a4b4", 
            foreground="#FFFFFF",
            font=('Calistoga Regular', 12),
            borderwidth=2,
            maxdate=fecha_ayer
        )
        self.entry_fin_back.place(
            x=500.0,
            y=103.0,
            width=94.0,
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

        button_window = canvas.create_window(650, 187, anchor='nw', window=button_start, width=197, height=38)
        # button_8.bind("<Button-1>", lambda event: seleccionar_años())



        entry_lotaje_image = PhotoImage(
            file="src/imagenes/assets/boton_comun_lim_stop_key.png")
        self.entry_lotaje = Entry(
            canvas,            
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            font=('Calistoga Regular', 12),
            highlightthickness=0,
            relief="flat"
        )
        self.entry_lotaje.place(
            x=500.0,
            y=187.0,
            width=94.0,
            height=38.0
        )
        self.texto_lotaje = "Cantidad"
        self.entry_lotaje.insert(0, self.texto_lotaje)
        self.entry_lotaje.bind("<FocusIn>", borrar_texto)
        self.entry_lotaje.bind("<FocusOut>", reescribir_texto)


        check_1_var = IntVar()
        checkbox_1 = Checkbutton(
            canvas,
            text="1º",  # Etiqueta del checkbox
            variable=check_1_var,  # Variable de control para el estado del checkbox
            onvalue=1,  # Valor cuando el checkbox está seleccionado
            offvalue=0,  # Valor cuando el checkbox está deseleccionado
            command=lambda: on_checkbox_click(checkbox_1),  # Función para manejar los clics del checkbox
            bd=0,  # Grosor del borde del checkbox
            bg="white",  # Color de fondo del checkbox
            activebackground="white",  # Color de fondo cuando el checkbox está activo
            highlightthickness=0,  # Grosor del borde cuando el checkbox está resaltado
            relief="flat"  # Tipo de relieve del checkbox
        )
        checkbox_1.place(
            x=904.0,
            y=187.0,
            width=70.0,
            height=38.0
        )

        check_podio_var = IntVar()
        checkbox_podio = Checkbutton(
            canvas,
            text="Podio",  # Etiqueta del checkbox
            variable=check_podio_var,  # Variable de control para el estado del checkbox
            onvalue=1,  # Valor cuando el checkbox está seleccionado
            offvalue=0,  # Valor cuando el checkbox está deseleccionado
            command=lambda: on_checkbox_click(checkbox_podio),  # Función para manejar los clics del checkbox
            bd=0,  # Grosor del borde del checkbox
            bg="white",  # Color de fondo del checkbox
            activebackground="white",  # Color de fondo cuando el checkbox está activo
            highlightthickness=0,  # Grosor del borde cuando el checkbox está resaltado
            relief="flat"  # Tipo de relieve del checkbox
        )
        checkbox_podio.place(
            x=990.0,
            y=187.0,
            width=70.0,
            height=38.0
        )

        check_5_var = IntVar()
        checkbox_5 = Checkbutton(
            canvas,
            text="Top 5",  # Etiqueta del checkbox
            variable=check_5_var,  # Variable de control para el estado del checkbox
            onvalue=1,  # Valor cuando el checkbox está seleccionado
            offvalue=0,  # Valor cuando el checkbox está deseleccionado
            command=lambda: on_checkbox_click(checkbox_5),  # Función para manejar los clics del checkbox
            bd=0,  # Grosor del borde del checkbox
            bg="white",  # Color de fondo del checkbox
            activebackground="white",  # Color de fondo cuando el checkbox está activo
            highlightthickness=0,  # Grosor del borde cuando el checkbox está resaltado
            relief="flat"  # Tipo de relieve del checkbox
        )
        checkbox_5.place(
            x=1076.0,
            y=187.0,
            width=70.0,
            height=38.0
        )

        check_puntos_var = IntVar()
        checkbox_puntos = Checkbutton(
            canvas,
            text="Puntúa",  # Etiqueta del checkbox
            variable=check_puntos_var,  # Variable de control para el estado del checkbox
            onvalue=1,  # Valor cuando el checkbox está seleccionado
            offvalue=0,  # Valor cuando el checkbox está deseleccionado
            command=lambda: on_checkbox_click(checkbox_puntos),  # Función para manejar los clics del checkbox
            bd=0,  # Grosor del borde del checkbox
            bg="white",  # Color de fondo del checkbox
            activebackground="white",  # Color de fondo cuando el checkbox está activo
            highlightthickness=0,  # Grosor del borde cuando el checkbox está resaltado
            relief="flat"  # Tipo de relieve del checkbox
        )
        checkbox_puntos.place(
            x=1162.0,
            y=187.0,
            width=70.0,
            height=38.0
        )


        piloto = SF1_backtesting.obtener_listado_pilotos(self.combo_años.get())
        self.piloto_var = tk.StringVar(value=piloto)
        self.combo_piloto = ttk.Combobox(canvas, textvariable=self.piloto_var, values=piloto)
        self.combo_piloto.place(x=34.0, y=187.0, width=258.0, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_piloto.current(0)  # Establece la opción por defecto
        self.combo_piloto.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        self.original_piloto = piloto

        self.combo_piloto.bind("<<ComboboxSelected>>", seleccionar_accion)
        self.combo_piloto.bind('<KeyRelease>', filter_options)

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
    
    def tickdirecto(self):
        piloto_txt = self.combo_piloto.get()
        accion_txt = self.combo_acciones.get()
        estrategia=self.combo_velas.get()

        self.b.establecer_piloto_accion(piloto_txt, accion_txt) 
       
        self.b.thread_orders(estrategia)
        
        if estrategia == 'RSI':
            self.b.thread_RSI_MACD()
        elif estrategia == 'Media Movil':
            self.b.thread_MediaMovil()
        elif estrategia == 'Bandas':
            self.b.thread_bandas()
        elif estrategia == 'Estocastico':
            self.b.thread_estocastico()

    def getPrice(self):
        piloto_txt = self.combo_piloto.get()
        accion_txt = self.combo_acciones.get()
        estrategia=self.combo_años.get()

        # self.b.establecer_piloto_accion(piloto_txt, accion_txt) 
       
        # self.b.thread_orders(estrategia)
        
        # if estrategia == 'RSI':
        #     self.b.thread_RSI_MACD()
        # elif estrategia == 'Media Movil':
        #     self.b.thread_MediaMovil()
        # elif estrategia == 'Bandas':
        #     self.b.thread_bandas()
        # elif estrategia == 'Estocastico':
        #     self.b.thread_estocastico()
    
    def lanzarEstrategia(self):
        piloto_txt = self.combo_piloto.get()
        accion_txt = self.combo_acciones.get()
        estrategia=self.combo_años.get()

    def pararTicksDirecto(self):
        piloto_txt = self.combo_piloto.get()
        accion_txt = self.combo_acciones.get()
        estrategia=self.combo_años.get()

    
    def coger_ticks(self):
        
        frecuencia_txt = "Daily"
        accion_txt = self.combo_acciones.get()
        inicio_txt = self.entry_inicio_back.get()
        fin_txt = self.entry_fin_back.get()
        estrategia_txt = 'Formula1.' + self.combo_piloto.get() + '.' + self.estrategia

        print("----------------------------------------")
        print(frecuencia_txt, accion_txt, inicio_txt, fin_txt, estrategia_txt)

        self.b.establecer_frecuencia_accion(frecuencia_txt, accion_txt) 

        #if parte backtestin
        self.b.thread_tick_reader(inicio_txt, fin_txt,estrategia_txt)

        # self.informacion()
    
    