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
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class FormularioBackTestingMasInformacion():

    def __init__(self, panel_principal, dataFrame, estrategia, rentabilidad):

        self.frame_width = 0
        self.frame_height = 0

        self.dataFrame = dataFrame
        self.estrategia = estrategia
        self.rentabilidad = rentabilidad

        #Frame principal 
        self.frame_principal = tk.Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)


        self.informacion()

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)   

        #Llamada a la función on_parent_configure cuando se redimensiona la ventana
        panel_principal.bind("<Configure>", self.on_parent_configure)


    def informacion(self):
        # Título arriba a la izquierda
        self.label_titulo_informacion = tk.Label(self.frame_principal, text="Información del backtesting", font=("Berlin Sans FB", 16, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_titulo_informacion.pack(pady=10, padx=10, anchor="w", side="top", fill="x")

        # Frame grid para las opciones
        self.frame_opciones = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_opciones.pack(pady=10, padx=10, anchor="center", side="top", fill="x")
        
        #Subtitulo "Información de la estrategia"
        self.label_info = tk.Label(self.frame_opciones, text="Información de la estrategia de " + self.estrategia, font=("Berlin Sans FB", 12, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_info.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        #frame para la descripción
        self.frame_info_inicial = tk.Frame(self.frame_opciones, bg=COLOR_CUERPO_PRINCIPAL, width=200, height=100)
        self.frame_info_inicial.grid(row=1, column=0, columnspan=3, sticky="nsew") 
        
        # Descripción de la operacion creativa
        self.descripcion_creativa = tk.Label(self.frame_info_inicial, justify="left", wraplength=200, font=("Aptos", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.descripcion_creativa.pack(pady=10, padx=5, anchor="w", side="top", fill="x")

        # Descripción de la operacion creativa
        self.descripcion_clasica = tk.Label(self.frame_info_inicial, justify="left", wraplength=200, font=("Aptos", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.descripcion_clasica.pack(pady=10, padx=5, anchor="w", side="top", fill="x")
        
        print("estrategia: ", self.estrategia)
        if (self.estrategia == "Futbol"):
            self.descripcion_creativa.configure(text="La operación creativa de fútbol consiste en inveritr en los equipos de fútbol, con el fin de obtener una rentabilidad a partir de las predicciones de los resultados de los partidos.")
        elif (self.estrategia == "Formula1"):
            self.descripcion_creativa.configure(text="La operación creativa de Formula 1 consiste en inveritr en los equipos de Formula 1, con el fin de obtener una rentabilidad a partir de las predicciones de los resultados de las carreras.")
        elif (self.estrategia == "Cine"):
            self.descripcion_creativa.configure(text="La operación creativa de cine consiste en inveritr en las películas, con el fin de obtener una rentabilidad a partir de las predicciones de los resultados en taquilla.")
        if (self.estrategia == "RSI"):
            self.descripcion_creativa.configure(text="La estrategia de RSI consiste en detectar zonas de sobreventa y sobrecompra mediante el calculo del mismo y detectaremos zonas de compra cuando se encuentre por debajo de los 35 puntos y zonas de venta por encima de los 65. Ademas le añadimos el calculo del indice MACD que en funcion de las dos componentes que tiene obtenemos señales mas fuertes")
        elif (self.estrategia == "Media Movil"):
            self.descripcion_creativa.configure(text="La estragegia de media movil se basa en el calculo de dos medias moviles que se corresponden con medias al corto y largo plazo. En funcion de los cruces que se produzcan entre ellas se generan señales de compra o señales de venta")
        elif (self.estrategia == "Bandas"):
            self.descripcion_creativa.configure(text="La estrategia de las bandas de bollinger se basa en comparar 2 de las 3 componentes que tiene este indicador con el precio de la misma accion. Si el precio se encuentra por debajo de la banda baja generara una señal de compra, y si se encuentra el precio por encima de la banda alta se generara señal de venta")
        elif (self.estrategia == "Estocastico"):
            self.descripcion_creativa.configure(text="La estrategia de Estocastico se basa en el cruce de dos de sus componentes que son la linea K y D. Ademas le añadimos el calculo del RSI, y en funcion de si se cumplen las dos condiciones se generara una señal de compra o venta")
        #Subtitulo "Resultados del backtesting"
        self.label_resultado = tk.Label(self.frame_opciones, text="Resultados del backtesting", font=("Berlin Sans FB", 12, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_resultado.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        #Frame para los resultados
        self.frame_resultados = tk.Frame(self.frame_opciones, bg=COLOR_CUERPO_PRINCIPAL, width=200, height=100)
        self.frame_resultados.grid(row=3, column=0, columnspan=3, sticky="nsew")

        #Label para la rentabilidad
        print("Rentabilidad: ", self.rentabilidad)
        self.rent100 = 100 + float(self.rentabilidad)
        self.rent100string = str(self.rent100)
        self.texto = "La rentabilidad obtenida en base a esta operación es de: " + self.rentabilidad + "%. Esto quiere decir que por cada 100 euros invertidos, se obtienen " + self.rent100string + " euros. En las siguientes gráficas se muestra la evolución de la rentabilidad y los precios de compra y venta. En la primera de ellas se muestra la rentabilidad obtenida en cada operación, mientras que en la segunda se muestra el precio de compra y venta de cada operación. En la tabla se muestran los resultados de cada operación."
        self.descripcion_rentabilidad = tk.Label(self.frame_resultados, justify="left", text=self.texto, font=("Aptos", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.descripcion_rentabilidad.pack(pady=10, padx=5, anchor="w", side="top", fill="x")

        #Grafica de la rentabilidad
        print("Graficando rentabilidad")
        print("Dataframe: ", self.dataFrame)


        # FRAMES
        # Crear un marco general
        self.frame_general_graficas = tk.Frame(self.frame_resultados, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_general_graficas.pack(pady=10, padx=10, anchor="center", side="top", fill="x")

        # Crear un marco para la gráfica de la izquierda
        self.frame_grafica = tk.Frame(self.frame_general_graficas, bg=COLOR_CUERPO_PRINCIPAL, width=200, height=100)
        self.frame_grafica.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Crear un marco para la gráfica de la derecha
        self.frame_grafica_precios = tk.Frame(self.frame_general_graficas, bg="blue", width=200, height=100)
        self.frame_grafica_precios.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Crear un marco para la tabla
        self.frame_tabla = tk.Frame(self.frame_general_graficas, bg="blue")
        self.frame_tabla.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    


        
        # Crear la figura de la gráfica
        df_valid_rentabilidad = self.dataFrame[~self.dataFrame['Rentabilidad'].isna()]
        self.figura = plt.Figure(figsize=(3, 2), dpi=100)
        self.ax = self.figura.add_subplot(111)

        # Graficar la rentabilidad
        if self.estrategia == "Futbol" or self.estrategia == "Formula1" or self.estrategia == "Cine":
            self.ax.plot(df_valid_rentabilidad['Fecha'], df_valid_rentabilidad['Rentabilidad'], color='r', marker='o')
        else:
            self.ax.plot(df_valid_rentabilidad['time'], df_valid_rentabilidad['Rentabilidad'], color='b', marker='o')

        # Numerar los puntos en la gráfica de rentabilidad con números simples
        for i, rentabilidad in enumerate(df_valid_rentabilidad['Rentabilidad']):
            
            if self.estrategia == "Futbol" or self.estrategia == "Formula1" or self.estrategia == "Cine":
                self.ax.annotate(str(i+1), (df_valid_rentabilidad['Fecha'].iloc[i], rentabilidad), ha='center', va='bottom')
            else:
                self.ax.annotate(str(i+1), (df_valid_rentabilidad['time'].iloc[i], rentabilidad), ha='center', va='bottom')


        self.ax.set_title('Rentabilidad de la operación')
        self.ax.set_xlabel('Fecha')
        self.ax.set_ylabel('Rentabilidad')
        self.ax.grid()
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_grafica)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

         
        #Grafica de los precios
        print("Graficando precios")


        # Crear la figura de la gráfica, puntos con 
        if self.estrategia == "Futbol" or self.estrategia == "Formula1" or self.estrategia == "Cine":
            df_valid_precios = self.dataFrame[~self.dataFrame['Precio'].isna()]
        else:
            df_valid_precios = self.dataFrame[~self.dataFrame['price'].isna()]
        
        valores_comprar = df_valid_precios.loc[df_valid_precios['Decision'] == 'Compra']
        valores_vender = df_valid_precios.loc[df_valid_precios['Decision'] == 'Venta']

        self.figura_precios = plt.Figure(figsize=(3, 2), dpi=100)
        self.ax_precios = self.figura_precios.add_subplot(111)

        
        if self.estrategia == "Futbol" or self.estrategia == "Formula1" or self.estrategia == "Cine":
            self.ax_precios.plot(valores_comprar['Fecha'], valores_comprar['Precio'], color='b', marker='o')
            self.ax_precios.plot(valores_vender['Fecha'], valores_vender['Precio'], color='r', marker='o')
        else:
            self.ax_precios.plot(valores_comprar['time'], valores_comprar['price'], color='b', marker='o')
            self.ax_precios.plot(valores_vender['time'], valores_vender['price'], color='r', marker='o')



        # Crear la lista de etiquetas con el formato "X"
        if self.estrategia == "Futbol" or self.estrategia == "Formula1" or self.estrategia == "Cine":
            etiquetas = ['{}'.format(i+1) for i, _ in enumerate(valores_vender['Precio'])]
        else:
            etiquetas = ['{}'.format(i+1) for i, _ in enumerate(valores_vender['price'])]

        # Numerar los puntos
        for i, txt in enumerate(etiquetas):
            if self.estrategia == "Futbol" or self.estrategia == "Formula1" or self.estrategia == "Cine":
                self.ax_precios.annotate(txt, (valores_vender['Fecha'].iloc[i], valores_vender['Precio'].iloc[i]))
            else:
                self.ax_precios.annotate(txt, (valores_vender['time'].iloc[i], valores_vender['price'].iloc[i]))

        self.ax_precios.set_title('Precio de la operación')
        self.ax_precios.set_xlabel('Fecha')
        self.ax_precios.set_ylabel('Precio')
        self.ax_precios.grid()
        self.canvas_precios = FigureCanvasTkAgg(self.figura_precios, master=self.frame_grafica_precios)
        self.canvas_precios.draw()
        self.canvas_precios.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


 #Tabla de resultados
        print("------------------------------------")
        print("Creando tabla de resultados")


        # Crear la tabla con matplotlib con las columnas: "Num Operación", "Rentabilidad", "Precio de Venta"
        self.figura_tabla = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax_tabla = self.figura_tabla.add_subplot(111)
        self.ax_tabla.axis('off')

        # Obtener los datos de las columnas
        num_operacion = [str(i + 1) for i in range(len(df_valid_rentabilidad))]
        
        #Obtener la rentabilidad y los precios de venta de las operaciones cuando Decision sea Venta
        if self.estrategia == "Futbol" or self.estrategia == "Formula1" or self.estrategia == "Cine":
            precios_venta = df_valid_precios.loc[df_valid_precios['Decision'] == 'Venta']['Precio'].tolist()
        else:
            precios_venta = df_valid_precios.loc[df_valid_precios['Decision'] == 'Venta']['price'].tolist()
        rentabilidad = df_valid_rentabilidad['Rentabilidad'].tolist()
        # Formatear los valores para que solo muestren dos decimales
        rentabilidad = ["{:.2f}".format(valor) for valor in rentabilidad]

        # Combinar los datos en una lista de listas para la tabla
        data = []
        for i in range(len(num_operacion)):
            data.append([num_operacion[i], rentabilidad[i], precios_venta[i]])

        print("------------------------------------")
        print("------------------------------------")
        print("------------------------------------")
        print("------------------------------------")

        print("Data: ", data)
        # Crear la tabla con los datos
        self.ax_tabla.table(cellText=data, colLabels=['Num Operación', 'Rentabilidad', 'Precio de Venta'], cellLoc='center', loc='center')

        # Crear el lienzo de matplotlib en el marco
        self.canvas_tabla = FigureCanvasTkAgg(self.figura_tabla, master=self.frame_tabla)
        self.canvas_tabla.draw()
        # Ajustar el relleno (padding) del widget pack a cero
        self.canvas_tabla.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
        # Configurar el borde del widget a cero
        self.canvas_tabla.get_tk_widget().configure(borderwidth=0)




    
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
        #Ajustar el tamaño del titulo
        self.label_titulo_informacion.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.25), "bold"))

        #Ajaustar los labels
        self.label_info.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.15), "bold"))
        self.label_resultado.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.15), "bold"))

        #Ajustar el tamaño del frame de descripción y el wraplength
        self.frame_info_inicial.configure(width=self.frame_width-25)
        self.descripcion_creativa.configure(wraplength=self.frame_width-25)
        self.frame_resultados.configure(width=self.frame_width-25)
        self.descripcion_rentabilidad.configure(wraplength=self.frame_width-25)

        #Ajustar el tamaño de las graficas
        self.frame_general_graficas.configure(width=self.frame_width-25)
        self.frame_grafica.configure(width=(self.frame_width-25)/2)
        self.frame_grafica_precios.configure(width=(self.frame_width-25)/2)
        self.frame_tabla.configure(width=self.frame_width-25)

        #Ajustar el tamaño de las graficas
        self.canvas.get_tk_widget().configure(width=(self.frame_width-25)/2, height=(self.frame_height)/4)
        self.canvas_precios.get_tk_widget().configure(width=(self.frame_width-25)/2, height=(self.frame_height)/4)
        self.canvas_tabla.get_tk_widget().configure(width=self.frame_width-25, height=self.frame_height/4)


    def limpiar_panel(self,panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()