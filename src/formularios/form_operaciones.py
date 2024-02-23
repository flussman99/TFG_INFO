import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Entry, Text, Button, PhotoImage
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
        entry_1 = Entry(
            canvas,
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            highlightthickness=0
        )
        entry_1.place(
            x=28.0,
            y=237.0,
            width=742.0,
            height=24.0
        )

        entry_image_2 = PhotoImage(
            file="src/imagenes/assets/entry_cartera_operaciones.png")
        entry_bg_2 = canvas.create_image(
            98.5,
            250.0,
            image=entry_image_2
        )
        entry_2 = Entry(
            canvas,
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            highlightthickness=0
        )
        entry_2.place(
            x=28.0,
            y=237.0,
            width=141.0,
            height=24.0
        )

        entry_image_3 = PhotoImage(
            file="src/imagenes/assets/entry_gran_latente_operaciones.png")
        entry_bg_3 = canvas.create_image(
            266.5,
            250.0,
            image=entry_image_3
        )
        entry_3 = Entry(
            canvas,
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            highlightthickness=0
        )
        entry_3.place(
            x=185.0,
            y=237.0,
            width=163.0,
            height=24.0
        )

        entry_image_4 = PhotoImage(
            file="src/imagenes/assets/entry_gran_dia_operaciones.png")
        entry_bg_4 = canvas.create_image(
            428.5,
            250.0,
            image=entry_image_4
        )
        entry_4 = Entry(
            canvas,
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            highlightthickness=0
        )
        entry_4.place(
            x=364.0,
            y=237.0,
            width=129.0,
            height=24.0
        )

        entry_image_5 = PhotoImage(
            file="src/imagenes/assets/entry_ordenes_operaciones.png")
        entry_bg_5 = canvas.create_image(
            566.5,
            250.0,
            image=entry_image_5
        )
        entry_5 = Entry(
            canvas,
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            highlightthickness=0
        )
        entry_5.place(
            x=509.0,
            y=237.0,
            width=115.0,
            height=24.0
        )

        entry_image_6 = PhotoImage(
            file="src/imagenes/assets/entry_gran_dia_operaciones.png")
        entry_bg_6 = canvas.create_image(
            705.0,
            250.0,
            image=entry_image_6
        )
        entry_6 = Entry(
            canvas,
            bd=0,
            bg="#30a4b4",
            fg="#FFFFFF",
            highlightthickness=0
        )
        entry_6.place(
            x=640.0,
            y=237.0,
            width=130.0,
            height=24.0
        )

        button_image_3 = PhotoImage(
            file="src/imagenes/assets/boton_comun_acciones_tiempo.png")
        button_3 = Button(
            canvas,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        button_3.place(
            x=20.0,
            y=86.0,
            width=151.0,
            height=32.0
        )

        button_image_4 = PhotoImage(
            file="src/imagenes/assets/boton_comun_lim_stop_key.png")
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
        button_5 = Button(
            canvas,
            image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        button_5.place(
            x=292.0,
            y=86.0,
            width=55.0,
            height=32.0
        )

        button_image_6 = PhotoImage(
            file="src/imagenes/assets/boton_comun_mkt.png")
        button_6 = Button(
            canvas,
            image=button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat"
        )
        button_6.place(
            x=380.0,
            y=86.0,
            width=115.0,
            height=32.0
        )

        button_image_7 = PhotoImage(
            file="src/imagenes/assets/boton_cantidad_operaciones.png")
        button_7 = Button(
            canvas,
            image=button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_7 clicked"),
            relief="flat"
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
            image=button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_8 clicked"),
            relief="flat"
        )
        button_8.place(
            x=380.0,
            y=156.0,
            width=115.0,
            height=32.0
        )

        button_image_9 = PhotoImage(
            file="src/imagenes/assets/boton_comun_lim_stop_key.png")
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
        button_10 = Button(
            canvas,
            image=button_image_10,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_10 clicked"),
            relief="flat"
        )
        button_10.place(
            x=292.0,
            y=156.0,
            width=55.0,
            height=32.0
        )

        button_image_11 = PhotoImage(
            file="src/imagenes/assets/boton_comun_numS_numO.png")
        button_11 = Button(
            canvas,
            image=button_image_11,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_11 clicked"),
            relief="flat"
        )
        button_11.place(
            x=569.0,
            y=156.0,
            width=67.0,
            height=32.0
        )

        button_image_12 = PhotoImage(
            file="src/imagenes/assets/boton_comun_numS_numO.png")
        button_12 = Button(
            canvas,
            image=button_image_12,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_12 clicked"),
            relief="flat"
        )
        button_12.place(
            x=711.0,
            y=156.0,
            width=67.0,
            height=32.0
        )

        button_image_13 = PhotoImage(
            file="src/imagenes/assets/boton_comun_S_O.png")
        button_13 = Button(
            canvas,
            image=button_image_13,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_13 clicked"),
            relief="flat"
        )
        button_13.place(
            x=528.0,
            y=156.0,
            width=28.0,
            height=32.0
        )

        button_image_14 = PhotoImage(
            file="src/imagenes/assets/boton_comun_S_O.png")
        button_14 = Button(
            canvas,
            image=button_image_14,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_14 clicked"),
            relief="flat"
        )
        button_14.place(
            x=669.0,
            y=156.0,
            width=28.0,
            height=32.0
        )

        button_image_15 = PhotoImage(
            file="src/imagenes/assets/boton_comun_acciones_tiempo.png")
        button_15 = Button(
            canvas,
            image=button_image_15,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_15 clicked"),
            relief="flat"
        )
        button_15.place(
            x=20.0,
            y=156.0,
            width=151.0,
            height=32.0
        )

        button_image_16 = PhotoImage(
            file="src/imagenes/assets/boton_comun_lim_stop_key.png")
        button_16 = Button(
            canvas,
            image=button_image_16,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_16 clicked"),
            relief="flat"
        )
        button_16.place(
            x=721.0,
            y=86.0,
            width=57.0,
            height=32.0
        )
        self.cuerpo_principal.mainloop()