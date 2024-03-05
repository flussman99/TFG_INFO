import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Entry, Text, Button, PhotoImage, Checkbutton, IntVar, Label
from PIL import Image, ImageDraw, ImageTk
from datetime import datetime
import pandas as pd
import sys
from bot import Bot as bt
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime
from config import COLOR_CUERPO_PRINCIPAL
"from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL , COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA"


class FormularioOperaciones(tk.Toplevel):
   
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
            elif combobox == self.combo_frecuencia:
                options = self.original_frecuencia 
            elif combobox == self.combo_velas:
                options = self.original_velas 

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

        def reload_options(event):
            # Get the combobox that triggered the event
            combobox = event.widget

            # Reset the values of the combobox
            if combobox == self.combo_acciones:
                combobox['values'] = self.original_acciones
            elif combobox == self.combo_mercados:
                combobox['values'] = self.original_mercados  
            elif combobox == self.combo_frecuencia:
                combobox['values'] = self.original_frecuencia 
            elif combobox == self.combo_velas:
                combobox['values'] = self.original_velas


        def borrar_texto(event):
            text_box = event.widget
            text_box.delete(0, tk.END)

        def reescribir_texto(event):
            text_box = event.widget

            if text_box.get() == '':
                if text_box == self.entry_compras:
                    self.entry_compras.insert(0, self.texto_compras)
                elif text_box == self.entry_ventas:
                    self.entry_ventas.insert(0, self.texto_ventas)
                elif text_box == self.entry_stop:
                    self.entry_stop.insert(0, self.texto_stop)
                elif text_box == self.entry_objetivo:
                    self.entry_objetivo.insert(0, self.texto_objetivo)


        def checkbox_clicked(check_var):
            if check_var.get() == 1:
                print("Checkbox activado")
            else:
                print("Checkbox desactivado")


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

        # Función para manejar la selección en el ComboBox
        def seleccionar_acciones(event):
            selected_item = self.acciones_var.get()
            print("Opción seleccionada:", selected_item)
            self.combo_acciones.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
            # hay que hacer que se muestre la info del mercado seleccionado

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
        

        velas = ['10', '20', '50', '100', '200', '500', '1000', '2000', '5000']
        self.velas_var = tk.StringVar(value=velas)
        self.combo_velas = ttk.Combobox(canvas, textvariable=self.velas_var, values=velas)
        self.combo_velas.place(x=34.0, y=103.0, width=258.0, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_velas.current(0)  # Establece la opción por defecto
        self.combo_velas.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        self.original_velas = velas

        # Función para manejar la selección en el ComboBox
        def seleccionar_velas(event):
            selected_item = self.velas_var.get()
            print("Opción seleccionada:", selected_item)
            self.combo_velas.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
            # hay que hacer que se muestre la info del mercado seleccionado

        self.combo_velas.bind("<<ComboboxSelected>>", seleccionar_velas)  # Asocia la función al evento de selección del ComboBox
        self.combo_velas.bind('<KeyRelease>', filter_options)

        button_image_4 = PhotoImage(
            file="src/imagenes/assets/boton_lim.png")
        button_4 = Button(
            canvas,
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        button_4.place(
            x=349.0,
            y=103.0,
            width=94.0,
            height=38.0
        )

        self.entry_compras = Entry(
            canvas,            
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            font=('Calistoga Regular', 12),
            highlightthickness=0,
            relief="flat"
        )

        self.entry_compras.place(
            x=500.0,
            y=103.0,
            width=94.0,
            height=38.0
        )
        self.texto_compras = "Nº compras"
        self.entry_compras.insert(0, self.texto_compras)
        self.entry_compras.bind("<FocusIn>", borrar_texto)
        self.entry_compras.bind("<FocusOut>", reescribir_texto)



        button_image_6 = PhotoImage(
            file="src/imagenes/assets/boton_comun_mkt.png")
        button_6 = Button(
            canvas,
            text="Precio compra",
            image=button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            compound=tk.CENTER,
            font=("Calistoga Regular", 12)
        )

        button_window = canvas.create_window(650, 103, anchor='nw', window=button_6, width=196, height=38)
        button_6.bind("<Button-1>", lambda event: seleccionar_velas())



        button_image_7 = PhotoImage(
            file="src/imagenes/assets/boton_cantidad_operaciones.png")
        button_7 = Button(
            canvas,
            text="Ticks en directo",
            image=button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=self.tickdirecto,
            compound=tk.CENTER,
            font="font_awesome"
        )
        button_7.place(
            x=904.0,
            y=103.0,
            width=305.0,
            height=38.0
        )



        button_image_8 = PhotoImage(
            file="src/imagenes/assets/boton_comun_mkt.png")
        button_8 = Button(
            canvas,
            text="Precio venta",
            image=button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_8 clicked"),
            compound=tk.CENTER,
            font=("Calistoga Regular", 12)
        )

        button_window = canvas.create_window(650, 187, anchor='nw', window=button_8, width=197, height=38)
        button_8.bind("<Button-1>", lambda event: seleccionar_velas())



        button_image_9 = PhotoImage(
            file="src/imagenes/assets/boton_stop.png")
        button_9 = Button(
            canvas,
            image=button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_9 clicked"),
            relief="flat"
        )
        button_9.place(
            x=349.0,
            y=187.0,
            width=94.0,
            height=38.0
        )

        entry_ventas_image = PhotoImage(
            file="src/imagenes/assets/boton_comun_lim_stop_key.png")
        self.entry_ventas = Entry(
            canvas,            
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            font=('Calistoga Regular', 12),
            highlightthickness=0,
            relief="flat"
        )
        self.entry_ventas.place(
            x=500.0,
            y=187.0,
            width=94.0,
            height=38.0
        )
        self.texto_ventas = "Nº ventas"
        self.entry_ventas.insert(0, self.texto_ventas)
        self.entry_ventas.bind("<FocusIn>", borrar_texto)
        self.entry_ventas.bind("<FocusOut>", reescribir_texto)




        self.entry_stop = Entry(
            canvas,            
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            font=('Calistoga Regular', 12),
            highlightthickness=0,
            relief="flat"
        )

        self.entry_stop.place(
            x=974.0,
            y=187.0,
            width=114.0,
            height=38.0
        )
        self.texto_stop = "Stop"
        self.entry_stop.insert(0, self.texto_stop)
        self.entry_stop.bind("<FocusIn>", borrar_texto)
        self.entry_stop.bind("<FocusOut>", reescribir_texto)


        self.entry_objetivo = Entry(
            canvas,            
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            font=('Calistoga Regular', 12),
            highlightthickness=0,
            relief="flat"
        )

        self.entry_objetivo.place(
            x=1217.0,
            y=187.0,
            width=114.0,
            height=38.0
        )
        self.texto_objetivo = "Objetivo"
        self.entry_objetivo.insert(0, self.texto_objetivo)
        self.entry_objetivo.bind("<FocusIn>", borrar_texto)
        self.entry_objetivo.bind("<FocusOut>", reescribir_texto)



        check_S_var = IntVar()
        checkbox_S = Checkbutton(
            canvas,
            text="S",  # Etiqueta del checkbox
            variable=check_S_var,  # Variable de control para el estado del checkbox
            onvalue=1,  # Valor cuando el checkbox está seleccionado
            offvalue=0,  # Valor cuando el checkbox está deseleccionado
            command=checkbox_clicked(check_S_var),  # Función para manejar los clics del checkbox
            bd=0,  # Grosor del borde del checkbox
            bg="white",  # Color de fondo del checkbox
            activebackground="white",  # Color de fondo cuando el checkbox está activo
            highlightthickness=0,  # Grosor del borde cuando el checkbox está resaltado
            relief="flat"  # Tipo de relieve del checkbox
        )
        checkbox_S.place(
            x=904.0,
            y=187.0,
            width=48.0,
            height=38.0
        )


        check_O_var = IntVar()
        checkbox_O = Checkbutton(
            canvas,
            text="O",  # Etiqueta del checkbox
            variable=check_O_var,  # Variable de control para el estado del checkbox
            onvalue=1,  # Valor cuando el checkbox está seleccionado
            offvalue=0,  # Valor cuando el checkbox está deseleccionado
            command=checkbox_clicked(check_O_var),  # Función para manejar los clics del checkbox
            bd=0,  # Grosor del borde del checkbox
            bg="white",  # Color de fondo del checkbox
            activebackground="white",  # Color de fondo cuando el checkbox está activo
            highlightthickness=0,  # Grosor del borde cuando el checkbox está resaltado
            relief="flat"  # Tipo de relieve del checkbox
        )
        checkbox_O.place(
            x=1145.0,
            y=187.0,
            width=48.0,
            height=38.0
        )



        frecuencia = ['1M', '2M', '5M', '10M', '15M', '20M', '30M', '1H', '2H', '3H', '4H', '6H', '8H', '12H', 'Daily', 'Weekly', 'Monthly']
        self.frecuencia_var = tk.StringVar(value=frecuencia)
        self.combo_frecuencia = ttk.Combobox(canvas, textvariable=self.frecuencia_var, values=frecuencia)
        self.combo_frecuencia.place(x=34.0, y=187.0, width=258.0, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_frecuencia.current(0)  # Establece la opción por defecto
        self.combo_frecuencia.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        self.original_frecuencia = frecuencia

        # Función para manejar la selección en el ComboBox
        def seleccionar_frecuencia(event):
            selected_item = self.mercados_var.get()
            print("Opción seleccionada:", selected_item)
            self.combo_frecuencia.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
            # hay que hacer que se muestre la info del mercado seleccionado

        self.combo_frecuencia.bind("<<ComboboxSelected>>", seleccionar_frecuencia)  # Asocia la función al evento de selección del ComboBox
        self.combo_frecuencia.bind('<KeyRelease>', filter_options)

        button_image_16 = PhotoImage(
            file="src/imagenes/assets/boton_comun_lim_stop_key.png")
        button_16 = Button(
            canvas,
            text="\uf0ad",
            image=button_image_16,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_16 clicked"),
            compound=tk.CENTER,
            font="font_awesome"
        )
        button_16.place(
            x=1234.0,
            y=103.0,
            width=98.0,
            height=38.0
        )
        self.cuerpo_principal.mainloop()
    
    def tickdirecto(self):
        frecuencia_txt = self.combo_frecuencia.get()
        accion_txt = self.combo_acciones.get()
        frec = self.calcular_frecuencia(frecuencia_txt)
        self.b.set_info(frec, accion_txt) 
        self.b.thread_RSI_MACD()
    
    def calcular_frecuencia(self, frecuencia_txt):
        # Obtener valores de la frecuencia en segundos
        if frecuencia_txt == "1M":
            frecuencia = 60
        elif frecuencia_txt == "2M":
            frecuencia = 120
        elif frecuencia_txt == "3M":
            frecuencia = 180
        elif frecuencia_txt == "4M":
            frecuencia = 240
        elif frecuencia_txt == "5M":
            frecuencia = 300
        elif frecuencia_txt == "6M":
            frecuencia = 360
        elif frecuencia_txt == "10M":
            frecuencia = 600
        elif frecuencia_txt == "12M":
            frecuencia = 720
        elif frecuencia_txt == "15M":
            frecuencia = 900
        elif frecuencia_txt == "20M":
            frecuencia = 1200
        elif frecuencia_txt == "30M":
            frecuencia = 1800
        elif frecuencia_txt == "1H":
            frecuencia = 3600
        elif frecuencia_txt == "2H":
            frecuencia = 7200
        elif frecuencia_txt == "3H":
            frecuencia = 10800
        elif frecuencia_txt == "4H":
            frecuencia = 14400
        elif frecuencia_txt == "6H":
            frecuencia = 21600
        elif frecuencia_txt == "8H":
            frecuencia = 28800
        elif frecuencia_txt == "12H":
            frecuencia = 43200
        elif frecuencia_txt == "Daily":
            frecuencia = 86400
        elif frecuencia_txt == "Weekly":
            frecuencia = 604800
        elif frecuencia_txt == "Monthly":
            frecuencia = 2592000
        else:
            frecuencia = 0
        return frecuencia
