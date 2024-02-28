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

        self.cuerpo_principal = tk.Frame(panel_principal, width=798, height=553)
        self.cuerpo_principal.grid(row=1, column=0, sticky="nsew")

        panel_principal.grid_rowconfigure(1, weight=1)  
        panel_principal.grid_columnconfigure(0, weight=1)


        canvas = Canvas(
            self.cuerpo_principal,
            bg = "#FFFFFF",
            height = 553,
            width = 798,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        image_image_1 = PhotoImage(
            file="src/imagenes/assets/fondo.png")
        image_1 = canvas.create_image(
            399.0,
            276.0,
            image=image_image_1
        )

        # button_image_1 = PhotoImage(
        #     file="src/imagenes/assets/boton_mercado_operaciones.png")
        # boton_mercado = Button(
        #     canvas,
        #     image=button_image_1,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=self.seleccionarMercado(),
        #     relief="flat"
        # )
        # boton_mercado.place(
        #     x=20.0,
        #     y=16.0,
        #     width=758.0,
        #     height=32.0
        # )

        # style = ttk.Style()
        # style.configure(
        #     "Custom.TCombobox",
        #     background="#30A4B4",  # Color de fondo
        #     foreground="#FFFFFF",  # Color del texto
        #     font=("Calistoga Regular", 12),     # Fuente de letra
        #     fieldbackground=[('readonly', 'transparent')]
        # )  

        self.b = bt(1) #como mejorarlo?
        # Lista de opciones para el ComboBox
        acciones, mercados = self.b.get_trading_data()

        # Crear el ComboBox
        button_image_1 = PhotoImage(
        file="src/imagenes/assets/boton_mercado_operaciones.png")

        def borrar_texto(event):
            text_box = event.widget
            text_box.delete(0, tk.END)

        def checkbox_clicked(check_var):
            if check_var.get() == 1:
                print("Checkbox activado")
            else:
                print("Checkbox desactivado")


        self.mercados_var = tk.StringVar(value=mercados)
        self.combo_mercados = ttk.Combobox(canvas, textvariable=self.mercados_var, values=mercados)
        self.combo_mercados.place(x=20.0, y=16.0, width=758, height=32.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_mercados.current(0)  # Establece la opción por defecto
        self.combo_mercados.configure(background='#30A4B4', foreground='#FFFFFF', font=('Calistoga Regular', 12))


        # Función para manejar la selección en el ComboBox
        def seleccionar_mercado(event):
            selected_item = self.mercados_var.get()
            print("Opción seleccionada:", selected_item)
            self.combo_mercados.configure(background='#30A4B4', foreground='#FFFFFF', font=('Calistoga Regular', 12))
            # hay que hacer que se muestre la info del mercado seleccionado

        self.combo_mercados.bind("<<ComboboxSelected>>", seleccionar_mercado)  # Asocia la función al evento de selección del ComboBox


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
            x=20.0,
            y=279.0,
            width=758.0,
            height=258.0
        )



        entry_image_1 = PhotoImage(
            file="src/imagenes/assets/entry_fondo_operaciones.png")
        entry_bg_1 = canvas.create_image(
            399.0,
            250.0,
            image=entry_image_1
        )

        canvas.create_text(28, 237, anchor="nw", text="Cartera: ", fill="white", font=("Calistoga Regular", 12))
        canvas.create_text(185, 237, anchor="nw", text="Gan. latente: ", fill="white", font=("Calistoga Regular", 12))
        canvas.create_text(364, 237, anchor="nw", text="Gan. día: ", fill="white", font=("Calistoga Regular", 12))
        canvas.create_text(509, 237, anchor="nw", text="Órdenes: ", fill="white", font=("Calistoga Regular", 12))
        canvas.create_text(640, 237, anchor="nw", text="Posición: ", fill="white", font=("Calistoga Regular", 12))
        

        button_image_3 = PhotoImage(
        file="src/imagenes/assets/boton_comun_acciones_tiempo.png")

        velas = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
        self.velas_var = tk.StringVar(value=velas)
        self.combo_velas = ttk.Combobox(canvas, textvariable=self.velas_var, values=velas)
        self.combo_velas.place(x=20.0, y=86.0, width=151.0, height=32.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_velas.current(0)  # Establece la opción por defecto
        self.combo_velas.configure(background='#30A4B4', foreground='#FFFFFF', font=('Calistoga Regular', 12))


        # Función para manejar la selección en el ComboBox
        def seleccionar_velas(event):
            selected_item = self.velas_var.get()
            print("Opción seleccionada:", selected_item)
            self.combo_velas.configure(background='#30A4B4', foreground='#FFFFFF', font=('Calistoga Regular', 12))
            # hay que hacer que se muestre la info del mercado seleccionado

        self.combo_velas.bind("<<ComboboxSelected>>", seleccionar_velas)  # Asocia la función al evento de selección del ComboBox


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
            x=204.0,
            y=86.0,
            width=55.0,
            height=32.0
        )

        button_image_5 = PhotoImage(
            file="src/imagenes/assets/boton_comun_lim_stop_key.png")
        self.button_5 = Entry(
            canvas,            
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            font=('Calistoga Regular', 12),
            highlightthickness=0,
            relief="flat"
        )

        self.button_5.place(
            x=292.0,
            y=86.0,
            width=55.0,
            height=32.0
        )
        texto_compras = "Nº compras"
        self.button_5.insert(0, texto_compras)
        self.button_5.bind("<FocusIn>", borrar_texto)



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

        button_window = canvas.create_window(380, 86, anchor='nw', window=button_6, width=115, height=32)
        button_6.bind("<Button-1>", lambda event: seleccionar_velas())



        button_image_7 = PhotoImage(
            file="src/imagenes/assets/boton_cantidad_operaciones.png")
        button_7 = Button(
            canvas,
            text="\uf0ad",
            image=button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_7 clicked"),
            compound=tk.CENTER,
            font="font_awesome"
        )
        button_7.place(
            x=528.0,
            y=86.0,
            width=178.0,
            height=32.0
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

        button_window = canvas.create_window(380, 156, anchor='nw', window=button_8, width=115, height=32)
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
            x=204.0,
            y=156.0,
            width=55.0,
            height=32.0
        )

        button_image_10 = PhotoImage(
            file="src/imagenes/assets/boton_comun_lim_stop_key.png")
        button_10 = Entry(
            canvas,            
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            font=('Calistoga Regular', 12),
            highlightthickness=0,
            relief="flat"
        )
        button_10.place(
            x=292.0,
            y=156.0,
            width=55.0,
            height=32.0
        )
        texto_ventas = "Nº ventas"
        button_10.insert(0, texto_ventas)
        button_10.bind("<FocusIn>", borrar_texto)




        button_image_11 = PhotoImage(
            file="src/imagenes/assets/boton_comun_numS_numO.png")
        self.button_11 = Entry(
            canvas,            
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            font=('Calistoga Regular', 12),
            highlightthickness=0,
            relief="flat"
        )

        self.button_11.place(
            x=569.0,
            y=156.0,
            width=67.0,
            height=32.0
        )
        texto_stop = "Stop"
        self.button_11.insert(0, texto_stop)
        self.button_11.bind("<FocusIn>", borrar_texto)


        button_image_12 = PhotoImage(
            file="src/imagenes/assets/boton_comun_numS_numO.png")
        self.button_12 = Entry(
            canvas,            
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            font=('Calistoga Regular', 12),
            highlightthickness=0,
            relief="flat"
        )

        self.button_12.place(
            x=711.0,
            y=156.0,
            width=67.0,
            height=32.0
        )
        texto_objetivo = "Objetivo"
        self.button_12.insert(0, texto_objetivo)
        self.button_12.bind("<FocusIn>", borrar_texto)



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
            x=528.0,
            y=156.0,
            width=28.0,
            height=32.0
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
            x=669.0,
            y=156.0,
            width=28.0,
            height=32.0
        )


        button_image_15 = PhotoImage(
        file="src/imagenes/assets/boton_comun_acciones_tiempo.png")

        frecuencia = ['1M', '2M', '5M', '10M', '15M', '20M', '30M', '1H', '2H', '3H', '4H', '6H', '8H', '12H', 'Daily', 'Weekly', 'Monthly']
        self.frecuencia_var = tk.StringVar(value=frecuencia)
        self.combo_frecuencia = ttk.Combobox(canvas, textvariable=self.frecuencia_var, values=frecuencia)
        self.combo_frecuencia.place(x=20.0, y=156.0, width=151.0, height=32.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_frecuencia.current(0)  # Establece la opción por defecto
        self.combo_frecuencia.configure(background='#30A4B4', foreground='#FFFFFF', font=('Calistoga Regular', 12))


        # Función para manejar la selección en el ComboBox
        def seleccionar_frecuencia(event):
            selected_item = self.mercados_var.get()
            print("Opción seleccionada:", selected_item)
            self.combo_frecuencia.configure(background='#30A4B4', foreground='#FFFFFF', font=('Calistoga Regular', 12))
            # hay que hacer que se muestre la info del mercado seleccionado

        self.combo_frecuencia.bind("<<ComboboxSelected>>", seleccionar_frecuencia)  # Asocia la función al evento de selección del ComboBox


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
            x=721.0,
            y=86.0,
            width=57.0,
            height=32.0
        )
        self.cuerpo_principal.mainloop()