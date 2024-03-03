import tkinter as tk
from tkinter import ttk, Canvas, Entry, Button, PhotoImage, Checkbutton, IntVar
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
import time
"from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL , COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA"


class FormularioInversiones(tk.Toplevel):
   
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



        self.titulo_mercado = ttk.Label(self.cuerpo_principal, text="Seleccione el Mercado:")
        self.titulo_mercado.place(x=35.0, y=0, width=200, height=38.0)
        self.titulo_mercado.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
        

        # Create the combobox
        self.mercados_var = tk.StringVar(value=mercados)
        self.combo_mercados = ttk.Combobox(self.cuerpo_principal, textvariable=self.mercados_var, values=mercados)
        self.combo_mercados.set(list(mercados)[0])


        self.combo_mercados.place(x=34.0, y=38.0, width=640, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
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

        self.titulo_acciones = ttk.Label(self.cuerpo_principal, text="Seleccione la Acción:")
        self.titulo_acciones.place(x=684.0, y=0, width=200, height=38.0)
        self.titulo_acciones.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        self.acciones_var = tk.StringVar(value=acciones)
        self.combo_acciones = ttk.Combobox(self.cuerpo_principal, textvariable=self.acciones_var, values=acciones)
        self.combo_acciones.place(x=684.0, y=38.0, width=640, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_acciones.current(0)  # Establece la opción por defecto
        self.combo_acciones.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        self.original_acciones = acciones

        self.combo_acciones.bind('<KeyRelease>', filter_options)
        self.combo_acciones.bind('<<ComboboxSelected>>', reload_options)



        cuadro_informacion_image = PhotoImage(
            file="src/imagenes/assets/boton_grafico_operaciones.png")
        cuadro_informacion = Button(
            canvas,
            image=cuadro_informacion_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        cuadro_informacion.place(
            x=35.0,
            y=334.0,
            width=1298.0,
            height=309.0
        )

        #         cuadro_informacion_image = PhotoImage(file="src/imagenes/assets/boton_grafico_operaciones.png")
        #         self.cuadro_informacion = tk.Label(
        #             image=cuadro_informacion_image,
        #             font=("Arial", 14),
        #             compound="top",  # Para que el texto aparezca sobre la imagen
        #             padx=10,  # Espaciado horizontal dentro del label
        #             pady=10   # Espaciado vertical dentro del label
        #         )
        #         self.cuadro_informacion.place(
        #             x=34.0,
        #             y=334.0,
        #             width=1298.0,
        #             height=309.0
        #         )
        


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

        self.titulo_estrategia = ttk.Label(self.cuerpo_principal, text="Seleccione una estrategia:")
        self.titulo_estrategia.place(x=35.0, y=96, width=200, height=38.0)
        self.titulo_estrategia.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        estrategia = ['RSI', 'Media Movil', 'Bandas', 'Estocastico']
        self.estrategia_var = tk.StringVar(value=estrategia)
        self.combo_estrategia = ttk.Combobox(self.cuerpo_principal, textvariable=self.estrategia_var, values=estrategia)
        self.combo_estrategia.place(x=35.0, y=131.0, width=200.0, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_estrategia.current(0)  # Establece la opción por defecto
        self.combo_estrategia.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        self.original_estrategia = estrategia

        self.combo_estrategia.bind('<KeyRelease>', filter_options)
        self.combo_estrategia.bind('<<ComboboxSelected>>', reload_options)


        self.titulo_frecuencia = ttk.Label(self.cuerpo_principal, text="Seleccione una frecuencia:")
        self.titulo_frecuencia.place(x=35.0, y=189, width=200, height=38.0)
        self.titulo_frecuencia.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        frecuencia = ['1M', '2M', '3M', '4M', '5M', '6M', '10M', '12M', '15M', '20M', '30M', '1H', '2H', '3H', '4H', '6H', '8H', '12H', 'Daily', 'Weekly', 'Monthly']
        self.frecuencia_var = tk.StringVar(value=frecuencia)
        self.combo_frecuencia = ttk.Combobox(self.cuerpo_principal, textvariable=self.frecuencia_var, values=frecuencia)
        self.combo_frecuencia.place(x=35.0, y=224.0, width=200.0, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_frecuencia.current(0)  # Establece la opción por defecto
        self.combo_frecuencia.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
                
        self.original_frecuencia = frecuencia

        self.combo_frecuencia.bind('<KeyRelease>', filter_options)
        self.combo_frecuencia.bind('<<ComboboxSelected>>', reload_options)



        self.titulo_fecha_inicio = ttk.Label(self.cuerpo_principal, text="Seleccione la fecha Inicial:")
        self.titulo_fecha_inicio.place(x=270.0, y=96, width=200, height=38.0)
        self.titulo_fecha_inicio.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        self.fecha_inicio_entry = DateEntry(
            canvas, 
            date_pattern='yyyy/mm/dd',
            background='darkblue', 
            foreground='white', 
            borderwidth=2
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
            borderwidth=2
        )
        self.fecha_fin_entry.place(
            x=270.0,
            y=224.0,
            width=200.0,
            height=38.0
        )

        self.titulo_rentabilidad = ttk.Label(self.cuerpo_principal, text="Seleccione el cálculo de rentabilidad:")
        self.titulo_rentabilidad.place(x=505.0, y=96, width=250, height=38.0)
        self.titulo_rentabilidad.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
        
        
        opciones_calculo = ['Rentabilidad Simple', 'Rentabilidad Diaria', 'Rentabilidad Acumulada', 'Rentabilidad media Geometrica']
        self.opciones_calculo_var = tk.StringVar(value=opciones_calculo)
        self.combo_calculo = ttk.Combobox(self.cuerpo_principal, textvariable=self.opciones_calculo_var, values=opciones_calculo)
        self.combo_calculo.place(x=505.0, y=131.0, width=250.0, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_calculo.current(0)  # Establece la opción por defecto
        self.combo_calculo.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))



        calcular_button = ttk.Button(canvas, text="Ticks en directo", command=self.tickdirecto)
        calcular_button.place(
            x=900.0,
            y=150.0,
            width=300.0,
            height=38.0
        )



        ticks_button = ttk.Button(self.cuerpo_principal, text="Mostrar información:", command=self.coger_ticks)
        ticks_button.place(
            x=500.0,
            y=210.0,
            width=200.0,
            height=38.0
        )


        guardar = ttk.Button(self.cuerpo_principal, text="Guardar", command=self.guardar_excell)
        guardar.place(
            x=900.0,
            y=100.0,
            width=300.0,
            height=38.0
        )

        self.cuerpo_principal.mainloop()


        
    def guardar_excell(self):
        estrategia_txt = self.combo_estrategia.get()
        self.b.guar_excell(estrategia_txt)


    def tickdirecto(self):
        frecuencia_txt = self.combo_frecuencia.get()
        accion_txt = self.combo_acciones.get()
        frec = self.calcular_frecuencia(frecuencia_txt)
        self.b.set_info(frec, accion_txt) 
        self.b.thread_RSI_MACD()

    def coger_ticks(self):
        
        frecuencia_txt = self.combo_frecuencia.get()
        accion_txt = self.combo_acciones.get()
        inicio_txt = self.fecha_inicio_entry.get()
        fin_txt = self.fecha_fin_entry.get()
        estrategia_txt = self.combo_estrategia.get()

        frec = self.calcular_frecuencia(frecuencia_txt)

        self.b.set_info(frec, accion_txt) 
        #if parte backtestin
        self.b.thread_tick_reader(inicio_txt, fin_txt,estrategia_txt)

        #if abrir operacion       
        self.b.thread_orders()

        #if elegir tipo de operacion
        if estrategia_txt == 'RSI':
            self.b.thread_RSI_MACD()

        elif estrategia_txt == 'Media Movil':
            self.b.thread_MediaMovil()

        elif estrategia_txt == 'Bandas':
            self.b.thread_Bandas()

        elif estrategia_txt == 'Estocastico':
            self.b.thread_Estocastico()


        #self.informacion()

        #self.b.wait() 
        time.sleep(8) #Espera 15 segundos para seguir haciendo cosas


        self.informacion()


    def informacion(self):

        estrategia = self.combo_estrategia.get()
        opcion = self.combo_calculo.get()

        df = pd.read_excel('RSI.xlsx')

        # Calcular la rentabilidad de la estrategia, sumar las rentabilidades cuando decision es -1
        rentabilidad_estrategia = df.loc[df['Decision'] == '-1', 'Rentabilidad'].sum()


        # Obtener el primer y último precio de la columna 'price'
        primer_precio = df['price'].iloc[0]
        ultimo_precio = df['price'].iloc[-1]

        # Calcular la rentabilidad basica de la accion
        rentabilidad_basica = (ultimo_precio - primer_precio) / primer_precio * 100

        self.resultado_label = ttk.Label(self.cuerpo_principal, text=f"La rentabilidad del periodo es de: {rentabilidad_basica:.2f}%")
        self.resultado_label.place(x=750.0, y=210.0, width=300.0, height=38.0)
        

        # Filtrar los datos donde "Decision" es igual a -1
        df_decision_minus_1 = df[df['Decision'] == '-1']

        # Crear la figura y el eje
        fig, ax = plt.subplots()

        # Graficar la rentabilidad en función del tiempo para Decision = -1
        ax.plot(df_decision_minus_1['time'].dt.strftime('%d-%m'), df_decision_minus_1['Rentabilidad'], label='Decision = -1')

        # Configurar la leyenda, etiquetas de ejes, etc. según tus necesidades
        ax.legend()
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Rentabilidad')
        ax.set_title('Rentabilidad en función del tiempo')

        # Crear el widget de canvas para la gráfica
        canvas = FigureCanvasTkAgg(fig, master=self.cuerpo_principal)
        canvas_widget = canvas.get_tk_widget()

        # Colocar el widget de canvas en un lugar específico
        canvas_widget.place(x=50, y=380, width=600, height=250)

        self.info_rentabilidad_estrategia = tk.Text(self.cuerpo_principal, wrap="word")
        self.info_rentabilidad_estrategia.insert(tk.END, f"En base a la estrategia {estrategia}, la rentabilidad obtenida es de: {rentabilidad_estrategia:.2f}% ")
        self.info_rentabilidad_estrategia.place(x=50, y=340, width=600, height=30.0)
        self.info_rentabilidad_estrategia.configure(background='#30A4B4', foreground='white', font=('Calistoga Regular', 10))


        if opcion == 'Rentabilidad Diaria':
            # Cálculo de rentabilidad diaria
            df['RentabilidadDiaria'] = (df['price'] - df['price'].shift(1)) / df['price'].shift(1) * 100

            # Crear una nueva figura
            self.figura = Figure(figsize=(6, 2), dpi=100)
            ax = self.figura.add_subplot(111)

            
            # Graficar la rentabilidad a lo largo del tiempo con suavizado exponencial
            ax.plot(df['time'], df['RentabilidadDiaria'], marker='o', linestyle='-', alpha=0.5)  # Añade alpha para hacer las líneas más transparentes
            ax.plot(df['time'], df['RentabilidadDiaria'].ewm(span=50).mean(), color='red', label='Suavizado Exponencial')
            ax.set_title('Rentabilidad a lo largo del tiempo')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Rentabilidad')
            ax.grid(True)

            # Establecer el locator de fechas en días y ajustar el formato de fecha
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            # Rotar las etiquetas del eje x 
            #ax.tick_params(axis='x', rotation=45)

            # Crear el widget de canvas para la gráfica
            canvas = FigureCanvasTkAgg(self.figura, master=self.cuerpo_principal)
            canvas_widget = canvas.get_tk_widget()

            # Colocar el widget de canvas en un lugar específico
            canvas_widget.place(x=700, y=380, width=600, height=250)
            
            self.info_rentabilidad_opcion = tk.Text(self.cuerpo_principal, wrap="word")
            self.info_rentabilidad_opcion.insert(tk.END, f"En base a la siguiente grafica podemos observar la rentabilidad diaria con suavizado exponencial.")
            self.info_rentabilidad_opcion.place(x=700, y=340, width=600, height=30.0)
            self.info_rentabilidad_opcion.configure(background='#30A4B4', foreground='white', font=('Calistoga Regular', 10))
            
        elif opcion == 'Rentabilidad Acumulada':
            # Cálculo de rentabilidad acumulada
            df['Rentabilidad Acumulada'] = (1 + df['Rentabilidad'] / 100).cumprod() * 100

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

            # Crear el widget de canvas para la gráfica
            canvas = FigureCanvasTkAgg(self.figura, master=self.cuerpo_principal)
            canvas_widget = canvas.get_tk_widget()

            # Colocar el widget de canvas en un lugar específico
            canvas_widget.place(x=700, y=380, width=600, height=250)

            self.info_rentabilidad_opcion = tk.Text(self.cuerpo_principal, wrap="word")
            self.info_rentabilidad_opcion.insert(tk.END, f"En la siguiente grafica podemos observar la rentabilidad acumulada a lo largo del tiempo.")
            self.info_rentabilidad_opcion.place(x=700, y=340, width=600, height=30.0)
            self.info_rentabilidad_opcion.configure(background='#30A4B4', foreground='white', font=('Calistoga Regular', 10))

        elif opcion == 'Rentabilidad media Geometrica':
            # Cálculo de rentabilidad media geométrica
            rentabilidad_media_geom = (df['Rentabilidad'] / 100 + 1).prod() ** (1 / len(df)) - 1
            print(f'Rentabilidad media geométrica: {rentabilidad_media_geom:.4f}%')

            self.info_rentabilidad_opcion = tk.Text(self.cuerpo_principal, wrap="word")
            self.info_rentabilidad_opcion.insert(tk.END, f"La rentabilidad media geométrica es de: {rentabilidad_media_geom:.4f}%")
            self.info_rentabilidad_opcion.place(x=700, y=340, width=600, height=30.0)
            self.info_rentabilidad_opcion.configure(background='#30A4B4', foreground='white', font=('Calistoga Regular', 10))

        
        




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

        
        print("ESTO ES UNA PRUEBOTA")
        print("ESTO ES UNA PRUEBOTA")
        print("ESTO ES UNA PRUEBOTA")


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
        #df.to_excel('media.xlsx', index=False)

    


# Crear la ventana principal
#ventana = tk.Tk()

# Crear la instancia de la clase FormularioInversiones
#formulario = FormularioInversiones(ventana)

# Iniciar el bucle de eventos
#ventana.mainloop()
