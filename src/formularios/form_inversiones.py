import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pandas as pd
import sys
from bot import Bot as bt
from tkcalendar import DateEntry
"from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL , COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA"


class FormularioInversiones(tk.Toplevel):
   
    def __init__(self, panel_principal):

        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.grid(row=0, column=0, sticky="nsew")

        panel_principal.grid_rowconfigure(0, weight=1)  # Add this line
        panel_principal.grid_columnconfigure(0, weight=1)  # Add this line

        self.cuerpo_principal = tk.Frame(panel_principal, width=500, height=500)
        self.cuerpo_principal.grid(row=1, column=0, sticky="nsew")

        panel_principal.grid_rowconfigure(1, weight=1)  # Add this line
        panel_principal.grid_columnconfigure(0, weight=1)  # Add this line
        

        title = tk.Label(self.cuerpo_principal, text="Operaciones de inversión", font=('Times',30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.grid(row=0, column=1, sticky="nsew")

              
              
        # Function to filter the options
        def filter_options(event):

            combobox = event.widget
            options = combobox.cget('values')
            data = combobox.get()

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


        texto_acciones = ttk.Label(self.cuerpo_principal, text="Seleccione una acción:")
        b = bt(1, 3600, "SAN.MAD")  # COMO HACERLO MEJOR??
        acciones, mercados = b.get_trading_data()  # Lista de acciones
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
    

        fecha_inicio_label = ttk.Label(self.cuerpo_principal, text="Fecha de inicio (YYYY/MM/DD):")
        self.fecha_inicio_entry = DateEntry(self.cuerpo_principal, date_pattern='yyyy/mm/dd')
        

        fecha_fin_label = ttk.Label(self.cuerpo_principal, text="Fecha de fin (YYYY/MM/DD):")
        self.fecha_fin_entry = DateEntry(self.cuerpo_principal, date_pattern='yyyy/mm/dd')


        texto_tiempos = ttk.Label(self.cuerpo_principal, text="Seleccione una frecuencia:")
        frecuencia = ["1M", "2M", "3M", "4M", "5M", "6M", "10M", "12M", "15M", "20M", "30M", "1H", "2H", "3H", "4H", "6H", "8H", "12H", "Daily", "Weekly", "Monthly"]  # Lista de frecuencias de ejemplo
        self.original_frecuencia = frecuencia

        self.frecuencia_var = tk.StringVar(value=frecuencia)
        self.combo_frecuencia = ttk.Combobox(self.cuerpo_principal, textvariable=self.frecuencia_var, values=frecuencia)
        self.combo_frecuencia.set(frecuencia[0])

        self.combo_frecuencia.bind('<KeyRelease>', filter_options)
        self.combo_frecuencia.bind('<<ComboboxSelected>>', reload_options)


        texto_tiempos.grid(row=3, column=0, padx=10, pady=10)
        self.combo_frecuencia.grid(row=3, column=1, padx=10, pady=10)

        calcular_button = ttk.Button(self.cuerpo_principal, text="Calcular Rentabilidad", command=self.calcular_rentabilidad)

        resultado_label = ttk.Label(self.cuerpo_principal, text="Resultado:")

        ticks_button = ttk.Button(self.cuerpo_principal, text="Sacar nº ticks", command=self.coger_ticks)


        fecha_inicio_label.grid(row=4, column=0, padx=10, pady=10)
        self.fecha_inicio_entry.grid(row=4, column=1, padx=10, pady=10)

        fecha_fin_label.grid(row=5, column=0, padx=10, pady=10)
        self.fecha_fin_entry.grid(row=5, column=1, padx=10, pady=10)


        calcular_button.grid(row=6, column=0, columnspan=2, pady=10)

        ticks_button.grid(row=7, column=0, columnspan=2, pady=10)

        resultado_label.grid(row=8, column=0, columnspan=2, pady=10)

        #self.config(bg=COLOR_CUERPO_PRINCIPAL)  # Ajusta esto según tu configuración

    def coger_ticks(self):
        
        frecuencia_txt = self.combo_frecuencia.get()
        accion_txt = self.combo_acciones.get()
        inicio_txt = self.fecha_inicio_entry.get()
        fin_txt = self.fecha_fin_entry.get()

        frec = self.calcular_frecuencia(frecuencia_txt)

        b = bt(1, frec, accion_txt)  # Cambiar esta acción por una lista que podamos elegir

        b.thread_tick_reader(inicio_txt, fin_txt)
        #b.wait()
        lista_segundos = b.get_ticks()
        xAxis = []
        yAxis = []
        i = 1
        print("Ticks received:",len(lista_segundos))

        print("Display obtained ticks 'as is'")
        count = 0
        for tick in lista_segundos:
            count+=1
            print(tick)
            if count >= frec:
                break
        ticks_frame = pd.DataFrame(lista_segundos)
        print(ticks_frame.head(10))


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
        accion = self.accion_combobox.get()
        fecha_inicio_str = self.fecha_inicio_entry.get()
        fecha_fin_str = self.fecha_fin_entry.get()

        # Validar las fechas (puedes agregar más validaciones según tus necesidades)
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
        except ValueError:
            self.resultado_label.config(text="Fechas inválidas")
            return

        # Llamar a la función que realiza el cálculo de rentabilidad (debes implementarla)
        rentabilidad = self.realizar_calculo_de_rentabilidad(accion, fecha_inicio, fecha_fin)

        # Actualizar la etiqueta de resultado
        if rentabilidad is not None:
            self.resultado_label.config(text=f"Rentabilidad: {rentabilidad:.2f}%")
        else:
            self.resultado_label.config(text="Error al calcular la rentabilidad")

    def realizar_calculo_de_rentabilidad(self, accion, fecha_inicio, fecha_fin):
        # Esta función debería realizar el cálculo de rentabilidad y devolver el resultado
        # Debes implementarla según tus necesidades
        # Retorna un valor de ejemplo (reemplázalo)
        return 0


# Crear la ventana principal
#ventana = tk.Tk()

# Crear la instancia de la clase FormularioInversiones
#formulario = FormularioInversiones(ventana)

# Iniciar el bucle de eventos
#ventana.mainloop()
