import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sys
"from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL , COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA"


class FormularioInversiones(tk.Toplevel):
   
    def __init__(self, panel_principal):

        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.grid(row=0, column=0, sticky="nsew")

        self.cuerpo_principal = tk.Frame(panel_principal)
        self.cuerpo_principal.grid(row=1, column=0, sticky="nsew")


        title = tk.Label(self.cuerpo_principal, text="Operaciones de inversión", font=('Times',30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.grid(row=1, column=1)


        texto_acciones = ttk.Label(self.cuerpo_principal, text="Seleccione una acción:")
        acciones = ["AAPL", "GOOGL", "MSFT", "TSLA"]  # Lista de acciones de ejemplo
        combo_acciones = ttk.Combobox(self.cuerpo_principal, values=acciones)
        combo_acciones.set(acciones[0])


        texto_acciones.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        combo_acciones.grid(row=2, column=1, padx=10, pady=10)


        fecha_inicio_label = ttk.Label(self.cuerpo_principal, text="Fecha de inicio (YYYY-MM-DD):")
        fecha_inicio_entry = ttk.Entry(self.cuerpo_principal)

        fecha_fin_label = ttk.Label(self.cuerpo_principal, text="Fecha de fin (YYYY-MM-DD):")
        fecha_fin_entry = ttk.Entry(self.cuerpo_principal)

        calcular_button = ttk.Button(self.cuerpo_principal, text="Calcular Rentabilidad", command=self.calcular_rentabilidad)

        resultado_label = ttk.Label(self.cuerpo_principal, text="Resultado:")


        fecha_inicio_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        fecha_inicio_entry.grid(row=3, column=1, padx=10, pady=10)

        fecha_fin_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        fecha_fin_entry.grid(row=4, column=1, padx=10, pady=10)

        calcular_button.grid(row=5, column=0, columnspan=2, pady=10)

        resultado_label.grid(row=6, column=0, columnspan=2, pady=10)


        #self.config(bg=COLOR_CUERPO_PRINCIPAL)  # Ajusta esto según tu configuración


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
