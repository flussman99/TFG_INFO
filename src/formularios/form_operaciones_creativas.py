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


class FormularioOperacionesCreativas(tk.Toplevel):
   
    def __init__(self, panel_principal, form_Futbol ,form_f1, form_Disney):
        
        self.formulario_f1 = form_f1
        self.form_Futbol = form_Futbol  
        self.form_Disney = form_Disney  
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


        button_image_futbol = PhotoImage(
            file="src/imagenes/assets/boton_futbol.png")
        button_futbol = Button(
            canvas,
            image=button_image_futbol,
            borderwidth=0,
            highlightthickness=0,
            command=self.estrategiaFutbol,
            compound=tk.CENTER,
            font=("Calistoga Regular", 12)
        )

        button_window = canvas.create_window(36, 30, anchor='nw', window=button_futbol, width=412, height=222)



        button_image_formula1 = PhotoImage(
            file="src/imagenes/assets/boton_formula1.png")
        button_formula1 = Button(
            canvas,
            image=button_image_formula1,
            borderwidth=0,
            highlightthickness=0,
            command=self.estrategiaF1,
            compound=tk.CENTER,
            font=("Calistoga Regular", 12)
        )

        button_window = canvas.create_window(477, 220, anchor='nw', window=button_formula1, width=412, height=222)



        button_image_Cristian = PhotoImage(
            file="src/imagenes/assets/boton_Cristian.png")
        button_Cristian = Button(
            canvas,
            text="Estrategia Disney",
            image=button_image_Cristian,
            borderwidth=0,
            highlightthickness=0,
            command=self.estrategiaDisney,
            compound=tk.CENTER,
            font=("Calistoga Regular", 12)
        )

        button_window = canvas.create_window(36, 399, anchor='nw', window=button_Cristian, width=412, height=222)



        button_image_Alvaro = PhotoImage(
            file="src/imagenes/assets/boton_Alvaro.png")
        button_Alvaro = Button(
            canvas,
            text="Estrategia Alvaro",
            image=button_image_Alvaro,
            borderwidth=0,
            highlightthickness=0,
            command=self.estrategiaAlvaro,
            compound=tk.CENTER,
            font=("Calistoga Regular", 12)
        )

        button_window = canvas.create_window(918, 30, anchor='nw', window=button_Alvaro, width=412, height=222)



        button_image_Jose = PhotoImage(
            file="src/imagenes/assets/boton_Jose.png")
        button_Jose = Button(
            canvas,
            text="Estrategia Jose",
            image=button_image_Jose,
            borderwidth=0,
            highlightthickness=0,
            command=self.estrategiaJose,
            compound=tk.CENTER,
            font=("Calistoga Regular", 12)
        )

        button_window = canvas.create_window(918, 399, anchor='nw', window=button_Jose, width=412, height=222)

        self.cuerpo_principal.mainloop()
    

    def estrategiaFutbol(self):
        self.form_Futbol()

    def estrategiaF1(self):
        self.formulario_f1()

    def estrategiaAlvaro(self):
        print("Alvaro")
    
    def estrategiaJose(self):
        print("Jose")
    
    def estrategiaDisney(self):
        self.form_Disney()
