import tkinter as tk
from tkinter import ttk, Canvas, Entry, Button, PhotoImage, Checkbutton, IntVar
from datetime import datetime, timedelta
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
from tkinter import Scrollbar
import matplotlib.ticker as ticker


"from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA"


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
        self.combo_mercados.set("NAS")  # Establece la opción por defecto
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
        self.combo_acciones.set("ACS.MAD")  # Establece la opción por defecto
        self.combo_acciones.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        self.original_acciones = acciones

        self.combo_acciones.bind('<KeyRelease>', filter_options)
        self.combo_acciones.bind('<<ComboboxSelected>>', reload_options)


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
        

        self.titulo_estrategia = ttk.Label(self.cuerpo_principal, text="Seleccione una estrategia:")
        self.titulo_estrategia.place(x=35.0, y=96, width=200, height=38.0)
        self.titulo_estrategia.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))

        estrategia = ['RSI', 'Media Movil', 'Bandas', 'Estocastico', 'Futbol']
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

        frecuencia = ['1M', '3M', '5M', '10M', '15M', '30M', '1H', '2H', '4H','Daily', 'Weekly', 'Monthly']        
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

        self.titulo_rentabilidad = ttk.Label(self.cuerpo_principal, text="Seleccione el cálculo de rentabilidad:")
        self.titulo_rentabilidad.place(x=505.0, y=96, width=250, height=38.0)
        self.titulo_rentabilidad.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))
        
        
        opciones_calculo = ['Rentabilidad Diaria', 'Rentabilidad Acumulada', 'Rentabilidad media Geometrica']
        self.opciones_calculo_var = tk.StringVar(value=opciones_calculo)
        self.combo_calculo = ttk.Combobox(self.cuerpo_principal, textvariable=self.opciones_calculo_var, values=opciones_calculo)
        self.combo_calculo.place(x=505.0, y=131.0, width=250.0, height=38.0)  # Ajusta el tamaño y la posición según sea necesario
        self.combo_calculo.current(0)  # Establece la opción por defecto
        self.combo_calculo.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 12))




        ticks_button = ttk.Button(self.cuerpo_principal, text="Mostrar información:", command=self.coger_ticks)
        ticks_button.place(
            x=505.0,
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


    def coger_ticks(self):
        
        frecuencia_txt = self.combo_frecuencia.get()
        accion_txt = self.combo_acciones.get()
        inicio_txt = self.fecha_inicio_entry.get()
        fin_txt = self.fecha_fin_entry.get()
        estrategia_txt = self.combo_estrategia.get()

        print("----------------------------------------")
        print(frecuencia_txt, accion_txt, inicio_txt, fin_txt, estrategia_txt)

        self.b.establecer_frecuencia_accion(frecuencia_txt, accion_txt) 

        #if parte backtestin
        self.b.thread_tick_reader(inicio_txt, fin_txt,estrategia_txt)

        

        self.informacion()


    def informacion(self):

        estrategia = self.combo_estrategia.get()
        opcion = self.combo_calculo.get()


        if estrategia == 'RSI':
            df = pd.read_excel('RSI.xlsx')

        elif estrategia == 'Media Movil':
            df = pd.read_excel('Media Movil.xlsx')

        elif estrategia == 'Bandas':
            df = pd.read_excel('Bandas.xlsx')

        elif estrategia == 'Estocastico':
            df = pd.read_excel('Estocastico.xlsx')

        # Calcular la rentabilidad de la estrategia, sumar las rentabilidades cuando decision es -1
        rentabilidad_estrategia = df.loc[df['Decision'] == '-1', 'Rentabilidad'].sum()

        self.valor_rentabilidad_estrategia = tk.Text(self.cuerpo_principal, wrap="word")
        self.valor_rentabilidad_estrategia.insert(tk.END, f"En base a la estrategia {estrategia}, la rentabilidad obtenida es de: {rentabilidad_estrategia:.2f}% ")
        self.valor_rentabilidad_estrategia.place(x=50, y=270, width=600, height=30.0)
        self.valor_rentabilidad_estrategia.configure(background='#30A4B4', foreground='white', font=('Calistoga Regular', 14))
        
        # Obtener el primer y último precio de la columna 'price'
        primer_precio = df['price'].iloc[0]
        ultimo_precio = df['price'].iloc[-1]

        print("-----------------Datos-----------------------")
        print(primer_precio, ultimo_precio)
        print(df)
        

        # Crea el widget Text con la informacion de la grafica de la estratgeia.
        self.info_rentabilidad_estrategia = tk.Text(self.cuerpo_principal, wrap="word")
        self.info_rentabilidad_estrategia.insert(tk.END, f"En la siguiente gráfica podemos observar, en azul la rentabilidad de las operaciones de compra-venta utilizando la estrategia {estrategia}. Cuando la rentabilida es positiva, significa que hemos obtenido beneficios, es decir, si hubiesemos invertido 100€, y la rentabilidad de la primera operacion fuera de 5%, hubiesemos tenido un beneficio de 5€, quedandonos con un total de 105€. En caso de que la rentabilidad fuera negativa, en vez de beneficios hubiesemos obtenido perdidas. En naranja podemos observar la rentabilidad acumulada de dichas operaciones. Es una manera de ver el rendimiento global de las decisiones financieras tomadas a lo largo del tiempo")
        self.info_rentabilidad_estrategia.place(x=50, y=310, width=600, height=80.0)
        self.info_rentabilidad_estrategia.configure(background='#30A4B4', foreground='white', font=('Calistoga Regular', 9))
        
        # Crea la barra deslizante
        scrollbar = Scrollbar(self.cuerpo_principal, command=self.info_rentabilidad_estrategia.yview)
        scrollbar.place(x=650, y=310, height=80.0)

        # Configura la barra deslizante con el widget Text
        self.info_rentabilidad_estrategia.config(yscrollcommand=scrollbar.set)

        # Filtrar los datos donde "Decision" es igual a -1
        df_decision_minus_1 = df[df['Decision'] == '-1']

        # Crear la figura y el eje
        fig, ax = plt.subplots()

        # Obtener el número de operaciones y la rentabilidad
        num_operaciones = range(1, df_decision_minus_1.shape[0] + 1)
        rentabilidad = df_decision_minus_1['Rentabilidad']

        # Calcular el acumulado de la rentabilidad
        rentabilidad_acumulada = rentabilidad.cumsum()

        # Graficar la rentabilidad en función del tiempo para Decision = -1
        ax.plot(num_operaciones, rentabilidad, marker='o', linestyle='-', label='Rentabilidad de las operaciones')
        ax.plot(num_operaciones, rentabilidad_acumulada, marker='o', linestyle='-', label='Rentabilidad Acumulada')
        ax.grid(True)

        # Configurar la leyenda, etiquetas de ejes, etc. según tus necesidades
        ax.legend()
        ax.set_ylabel('Rentabilidad')
        ax.set_title('Rentabilidad en función de las operaciones')

        # Crear el widget de canvas para la gráfica
        canvas = FigureCanvasTkAgg(fig, master=self.cuerpo_principal)
        canvas_widget = canvas.get_tk_widget()

        # Colocar el widget de canvas en un lugar específico
        canvas_widget.place(x=50, y=400, width=600, height=250)


        # Calcular la rentabilidad basica de la accion
        rentabilidad_basica = (ultimo_precio - primer_precio) / primer_precio * 100

        # Mostrar la rentabilidad básica
        self.valor_rentabilidad_basica = tk.Text(self.cuerpo_principal, wrap="word")
        self.valor_rentabilidad_basica.insert(tk.END, f"En base a la estrategia básica, la rentabilidad obtenida es de: {rentabilidad_basica:.2f}% ")
        self.valor_rentabilidad_basica.place(x=700, y=270, width=600, height=30.0)
        self.valor_rentabilidad_basica.configure(background='#30A4B4', foreground='white', font=('Calistoga Regular', 14))


        if opcion == 'Rentabilidad Diaria':

            df['date'] = pd.to_datetime(df['time'])
            df = df.set_index('date')

            # Calcular la rentabilidad diaria
            df['RentabilidadDiaria'] = (df['price'] - df['price'].shift(1)) / df['price'].shift(1) * 100

            # Calcular la rentabilidad media diaria
            rentabilidad_media_diaria = df.groupby(df.index.date)['RentabilidadDiaria'].mean()

            rentabilidad_acumulada_basica = rentabilidad_media_diaria.cumsum()


            # Crear una nueva figura
            self.figura = Figure(figsize=(6, 2), dpi=100)
            ax = self.figura.add_subplot(111)

            # Graficar la rentabilidad a lo largo del tiempo
            ax.plot(rentabilidad_media_diaria.index, rentabilidad_media_diaria.values, marker='o', linestyle='-', color='b')
            ax.plot(rentabilidad_acumulada_basica.index, rentabilidad_acumulada_basica.values, marker='o', linestyle='-', color='orange')
            ax.set_title('Rentabilidad en función del tiempo')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Rentabilidad')
            ax.grid(True)

            # Establecer el locator de fechas en días y ajustar el formato de fecha
            ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

            # Crear el widget de canvas para la gráfica
            canvas = FigureCanvasTkAgg(self.figura, master=self.cuerpo_principal)
            canvas_widget = canvas.get_tk_widget()

            # Colocar el widget de canvas en un lugar específico
            canvas_widget.place(x=700, y=400, width=600, height=250)
            
            self.info_rentabilidad_opcion = tk.Text(self.cuerpo_principal, wrap="word")
            self.info_rentabilidad_opcion.insert(tk.END, f"En base a la siguiente grafica podemos observar la rentabilidad diaria.")
            self.info_rentabilidad_opcion.place(x=700, y=310, width=600, height=80.0)
            self.info_rentabilidad_opcion.configure(background='#30A4B4', foreground='white', font=('Calistoga Regular', 10))

             # Crea la barra deslizante
            scrollbar2 = Scrollbar(self.cuerpo_principal, command=self.info_rentabilidad_estrategia.yview)
            scrollbar2.place(x=1300, y=310, height=80.0)

            # Configura la barra deslizante con el widget Text
            self.info_rentabilidad_estrategia.config(yscrollcommand=scrollbar2.set)
            
        elif opcion == 'Rentabilidad Acumulada':
            df['date'] = pd.to_datetime(df['time'])
            df = df.set_index('date')

            # Calcular la rentabilidad diaria
            df['RentabilidadDiaria'] = (df['price'] - df['price'].shift(1)) / df['price'].shift(1) * 100

            # Calcular la rentabilidad acumulada diaria
            df['RentabilidadAcumulada'] = (1 + df['RentabilidadDiaria']).cumprod()


            # Crear una nueva figura
            self.figura = Figure(figsize=(6, 2), dpi=100)
            ax = self.figura.add_subplot(111)

            # Graficar la rentabilidad acumulada
            ax.plot(df.index, df['RentabilidadAcumulada'], marker='o', linestyle='-', color='r',markersize=2)
            ax.set_title('Rentabilidad Acumulada')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Rentabilidad Acumulada')
            ax.grid(True)

            # Establecer el locator de fechas en días y ajustar el formato de fecha
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

            # Rotar las etiquetas del eje x 
            #ax.tick_params(axis='x', rotation=45)

            # Crear el widget de canvas para la gráfica
            canvas = FigureCanvasTkAgg(self.figura, master=self.cuerpo_principal)
            canvas_widget = canvas.get_tk_widget()

            # Colocar el widget de canvas en un lugar específico
            canvas_widget.place(x=700, y=380, width=600, height=250)

            rentabilidad_acumulada_final = df['RentabilidadAcumulada'].iloc[-1]

            self.info_rentabilidad_opcion = tk.Text(self.cuerpo_principal, wrap="word")
            self.info_rentabilidad_opcion.insert(tk.END, f"En la siguiente grafica podemos observar la rentabilidad acumulada a lo largo del tiempo. La rentabilidad acumulada final es de: {rentabilidad_acumulada_final:.2f}%.")
            self.info_rentabilidad_opcion.place(x=700, y=340, width=600, height=40.0)
            self.info_rentabilidad_opcion.configure(background='#30A4B4', foreground='white', font=('Calistoga Regular', 10))

        elif opcion == 'Rentabilidad media Geometrica':
            # Cálculo de rentabilidad media geométrica
            rentabilidad_media_geom = (df['Rentabilidad'] / 100 + 1).prod() ** (1 / len(df)) - 1
            print(f'Rentabilidad media geométrica: {rentabilidad_media_geom:.4f}%')

            self.info_rentabilidad_opcion = tk.Text(self.cuerpo_principal, wrap="word")
            self.info_rentabilidad_opcion.insert(tk.END, f"La rentabilidad media geométrica es de: {rentabilidad_media_geom:.4f}%")
            self.info_rentabilidad_opcion.place(x=700, y=340, width=600, height=40.0)
            self.info_rentabilidad_opcion.configure(background='#30A4B4', foreground='white', font=('Calistoga Regular', 10))

        