import tkinter as tk
from tkinter import ttk
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


class FormularioInversiones(tk.Toplevel):
   
    def __init__(self, panel_principal):

        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.grid(row=0, column=0, sticky="nsew")

        panel_principal.grid_rowconfigure(0, weight=1)
        panel_principal.grid_columnconfigure(0, weight=1) 

        self.cuerpo_principal = tk.Frame(panel_principal, width=500, height=500)
        self.cuerpo_principal.grid(row=1, column=0, sticky="nsew")

        panel_principal.grid_rowconfigure(1, weight=1)  
        panel_principal.grid_columnconfigure(0, weight=1)  
        

        self.labelTitulo = tk.Label(self.barra_superior, text="Operaciones de inversión")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.grid(row=1, column=0, padx=10, pady=10)

              
              
        # Function to filter the options
        def filter_options(event):

            combobox = event.widget
            options = combobox.cget('values')
            data = combobox.get()

            if combobox == self.combo_acciones:
                options = self.original_acciones
            elif combobox == self.combo_mercados:
                options = self.original_mercados  
            elif combobox == self.combo_frecuencia:
                options = self.original_frecuencia 
            elif combobox == self.combo_estrategia:
                options = self.original_estrategia 

            if data:
                # Filter the options
                filtered_options = [option for option in options if option.startswith(data)]
            else:
                # If the data is empty, reset the options to the original list
                filtered_options = options

            combobox['values'] = filtered_options

            if hasattr(filter_options, 'job'):
                self.cuerpo_principal.after_cancel(filter_options.job)

            # Schedule a new job
            filter_options.job = self.cuerpo_principal.after(2000, combobox.event_generate, '<Down>')

        def filter_acciones(event):
            # Get selected market
            selected_market = self.combo_mercados.get()

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
            elif combobox == self.combo_estrategia:
                combobox['values'] = self.original_estrategia


        texto_acciones = ttk.Label(self.cuerpo_principal, text="Seleccione una acción:")
        self.b = bt(1)  # COMO HACERLO MEJOR??
        acciones, mercados = self.b.get_trading_data()  # Lista de acciones
        #self.combo_acciones = ttk.Combobox(self.cuerpo_principal, values=acciones)
        #self.combo_acciones.set(acciones[0])
        # Create the combobox
        self.acciones_var = tk.StringVar(value=acciones)
        self.mercados_var = tk.StringVar(value=mercados)
        self.combo_acciones = ttk.Combobox(self.cuerpo_principal, textvariable=self.acciones_var, values=acciones)
        self.combo_mercados = ttk.Combobox(self.cuerpo_principal, textvariable=self.mercados_var, values=mercados)
        self.combo_acciones.set(acciones[0])
        self.combo_mercados.set(list(mercados)[0])

        self.original_acciones = acciones
        self.original_mercados = mercados

        self.combo_acciones.bind('<KeyRelease>', filter_options)
        self.combo_acciones.bind('<<ComboboxSelected>>', reload_options)
        self.combo_mercados.bind('<<ComboboxSelected>>', filter_acciones)


        texto_acciones.grid(row=2, column=0, padx=10, pady=10)
        self.combo_acciones.grid(row=2, column=1, padx=10, pady=10)
        self.combo_mercados.grid(row=2, column=2, padx=10, pady=10)
    

        self.fecha_label = ttk.Label(self.cuerpo_principal, text="Fecha de inicio y fin (YYYY/MM/DD):")
        self.fecha_inicio_entry = DateEntry(self.cuerpo_principal, date_pattern='yyyy/mm/dd')
        self.fecha_fin_entry = DateEntry(self.cuerpo_principal, date_pattern='yyyy/mm/dd')


        texto_tiempos = ttk.Label(self.cuerpo_principal, text="Seleccione una frecuencia y una estrategia de inversión:")
        frecuencia = ['1M', '2M', '3M', '4M', '5M', '6M', '10M', '12M', '15M', '20M', '30M', '1H', '2H', '3H', '4H', '6H', '8H', '12H', 'Daily', 'Weekly', 'Monthly']
        self.original_frecuencia = frecuencia
        estrategia = ['RSI', 'Media Movil', 'Bandas', 'Estocastico']
        self.original_estrategia = estrategia

        self.frecuencia_var = tk.StringVar(value=frecuencia)
        self.combo_frecuencia = ttk.Combobox(self.cuerpo_principal, textvariable=self.frecuencia_var, values=frecuencia)
        self.combo_frecuencia.set(frecuencia[0])

        self.estrategia_var = tk.StringVar(value=estrategia)
        self.combo_estrategia = ttk.Combobox(self.cuerpo_principal, textvariable=self.estrategia_var, values=estrategia)
        self.combo_estrategia.set(estrategia[0])
        
        self.combo_frecuencia.bind('<KeyRelease>', filter_options)
        self.combo_frecuencia.bind('<<ComboboxSelected>>', reload_options)

        self.combo_estrategia.bind('<KeyRelease>', filter_options)
        self.combo_estrategia.bind('<<ComboboxSelected>>', reload_options)

        self.fecha_label.grid(row=4, column=0, padx=10, pady=10)
        self.fecha_inicio_entry.grid(row=4, column=1, padx=10, pady=10)
        self.fecha_fin_entry.grid(row=4, column=2, padx=10, pady=10)

        texto_tiempos.grid(row=3, column=0, padx=10, pady=10)
        self.combo_frecuencia.grid(row=3, column=1, padx=10, pady=10)
        self.combo_estrategia.grid(row=3, column=2, padx=10, pady=10)

        opciones_calculo = ['Rentabilidad Simple', 'Rentabilidad Diaria', 'Rentabilidad Acumulada', 'Rentabilidad media Geometrica']
        self.opciones_calculo_var = tk.StringVar(value=opciones_calculo)
        self.combo_calculo_label = ttk.Label(self.cuerpo_principal, text="Elige la opción de cálculo de rentabilidad:")
        self.combo_calculo = ttk.Combobox(self.cuerpo_principal, textvariable=self.opciones_calculo_var, values=opciones_calculo)
        self.combo_calculo.set(opciones_calculo[0])

        calcular_button = ttk.Button(self.cuerpo_principal, text="Calcular Rentabilidad", command=self.calcular_rentabilidad)

        self.resultado_label = ttk.Label(self.cuerpo_principal, text="Resultado:")

        ticks_button = ttk.Button(self.cuerpo_principal, text="Mostrar información:", command=self.coger_ticks)

        guardar = ttk.Button(self.cuerpo_principal, text="Guardar", command=self.guardar_excell)

        self.combo_calculo_label.grid(row=5, column=0, padx=10, pady=10)
        self.combo_calculo.grid(row=5, column=1, padx=10, pady=10)
        calcular_button.grid(row=6, column=0, columnspan=2, pady=10)

        ticks_button.grid(row=7, column=0, columnspan=2, pady=10)
        guardar.grid(row=7, column=1, columnspan=2, pady=10)

        self.resultado_label.grid(row=6, column=1, columnspan=2, pady=10)

        #self.config(bg=COLOR_CUERPO_PRINCIPAL)  # Ajusta esto según tu configuración

        

    def coger_ticks(self):
        
        frecuencia_txt = self.combo_frecuencia.get()
        accion_txt = self.combo_acciones.get()
        inicio_txt = self.fecha_inicio_entry.get()
        fin_txt = self.fecha_fin_entry.get()
        estrategia_txt = self.combo_estrategia.get()

        frec = self.calcular_frecuencia(frecuencia_txt)

        self.b.set_info(frec, accion_txt) 
#if parte backtestin
        self.b.thread_tick_reader(inicio_txt, fin_txt)
 #if abrir operacion       
        self.b.thread_orders()
#if elegir tipo de operacion
        if estrategia_txt == 'RSI':
            self.b.thread_RSI_MACD()
        elif estrategia_txt == 'Media Movil':
            self.b.thread_MediaMovil()


        #b.wait() esto yo no utilizo para nada

        #a partir de aqui comento

        # lista_segundos = self.b.get_ticks()
        # xAxis = []
        # yAxis = []
        # i = 1
        # print("Ticks received:",len(lista_segundos))

        # print("Display obtained ticks 'as is'")
        # count = 0
        # for tick in lista_segundos:
        #     count+=1
        #     print(tick)
        #     if count >= frec:
        #         break
        # ticks_frame = pd.DataFrame(lista_segundos)
        # print(ticks_frame.head(10))

        # # Prepare data for plotting
        # xAxis = list(range(len(lista_segundos)))
        # #yAxis = [tick.price for tick in lista_segundos]
        # yAxis = lista_segundos

        # for tick in lista_segundos:

        #     datetime_obj = tick[0].strftime('%Y-%m-%d %H:%M:%S')

        #     xAxis.append(datetime_obj)
        #     yAxis.append(tick[1])

        # # Create a new figure
        # fig.clear()
        
        # fig = Figure(figsize=(5, 4), dpi=100)

        # # Add a subplot to the figure
        # ax = fig.add_subplot(111)

        # # Plot data
        # ax.plot(xAxis, yAxis)

        # # Create a canvas and add it to your Tkinter window
        # canvas = FigureCanvasTkAgg(fig, master=self.cuerpo_principal)  # 'self.cuerpo_principal' should be the parent widget
        # canvas.draw()
        # canvas.get_tk_widget().grid(row=9, column=0)  # Adjust grid parameters as needed



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


    def calcular_rentabilidad(self):
        # Obtener valores de los widgets
        accion = self.combo_acciones.get()
        fecha_inicio_str = self.fecha_inicio_entry.get()
        fecha_fin_str = self.fecha_fin_entry.get()
        frec_str = self.combo_frecuencia.get()
        frec = self.calcular_frecuencia(frec_str)

        self.b.set_info(frec, accion) 


        df = pd.read_excel('media.xlsx')

        # Obtener el primer y último precio de la columna 'price'
        primer_precio = df['price'].iloc[0]
        ultimo_precio = df['price'].iloc[-1]

        # Calcular la rentabilidad
        rentabilidad = (ultimo_precio - primer_precio) / primer_precio * 100

        #calcular la rentabilidad diaria
        df['Rentabilidad'] = (df['price'] - df['price'].shift(1)) / df['price'].shift(1) * 100

        # Cálculo de rentabilidad acumulada
        df['Rentabilidad Acumulada'] = (1 + df['Rentabilidad'] / 100).cumprod() * 100

        # Cálculo de rentabilidad acumulada 2
        #df['Rentabilidad Acumulada2'] = df['Rentabilidad'].cumsum()

        # Cálculo de rentabilidad acumulada 3
        #df['Rentabilidad Acumulada3'] = (df['price'] - df['price'].iloc[0]) / df['price'].iloc[0] * 100

        
        

        # Imprimir el resultado
        print(f'Rentabilidad: {rentabilidad:.4f}%')

        if self.combo_calculo.get() == 'Rentabilidad Diaria':
            # Cálculo de rentabilidad diaria

            print("ESTO ES UNA PRUEBOTA")
            print(df['price'].shift(1))
            print(df['price'])
            print(df)


            # Crear una nueva figura
            self.figura = Figure(figsize=(6, 2), dpi=100)
            ax = self.figura.add_subplot(111)

            
            # Graficar la rentabilidad a lo largo del tiempo con suavizado exponencial
            ax.plot(df['time'], df['Rentabilidad'], marker='o', linestyle='-', alpha=0.5)  # Añade alpha para hacer las líneas más transparentes
            ax.plot(df['time'], df['Rentabilidad'].ewm(span=50).mean(), color='red', label='Suavizado Exponencial')
            ax.set_title('Rentabilidad a lo largo del tiempo')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Rentabilidad')
            ax.grid(True)

            # Establecer el locator de fechas en días y ajustar el formato de fecha
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            # Rotar las etiquetas del eje x 
            #ax.tick_params(axis='x', rotation=45)

            # Crear un widget de Tkinter para la figura
            canvas = FigureCanvasTkAgg(self.figura, master=self.cuerpo_principal)
            canvas.draw()
            canvas.get_tk_widget().grid(row=9, column=0, columnspan=2, pady=20)
            

            
        elif self.combo_calculo.get() == 'Rentabilidad Acumulada':
            
            # Crear una nueva figura
            self.figura = Figure(figsize=(6, 2), dpi=100)
            ax = self.figura.add_subplot(111)

            # Graficar la rentabilidad acumulada
            ax.plot(df['time'], df['Rentabilidad Acumulada'], marker='o', linestyle='-', color='green')
            ax.set_title('Rentabilidad Acumulada')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Rentabilidad Acumulada')
            ax.grid(True)

            # Establecer el locator de fechas en días y ajustar el formato de fecha
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            # Rotar las etiquetas del eje x 
            #ax.tick_params(axis='x', rotation=45)

            # Crear un widget de Tkinter para la figura
            canvas = FigureCanvasTkAgg(self.figura, master=self.cuerpo_principal)
            canvas.draw()
            canvas.get_tk_widget().grid(row=9, column=0, columnspan=2, pady=20)

        elif self.combo_calculo.get() == 'Rentabilidad media Geometrica':
            # Cálculo de rentabilidad media geométrica
            rentabilidad_media_geom = (df['Rentabilidad'] / 100 + 1).prod() ** (1 / len(df)) - 1
            print(f'Rentabilidad media geométrica: {rentabilidad_media_geom:.4f}%')

        else:
           pass

        # Actualizar la etiqueta de resultado
        if rentabilidad is not None:
            self.resultado_label.config(text=f"Rentabilidad: {rentabilidad:.2f}%")
        else:
            self.resultado_label.config(text="Error al calcular la rentabilidad")

        #Guardar el df
        df.to_excel('media.xlsx', index=False)

    


# Crear la ventana principal
#ventana = tk.Tk()

# Crear la instancia de la clase FormularioInversiones
#formulario = FormularioInversiones(ventana)

# Iniciar el bucle de eventos
#ventana.mainloop()
