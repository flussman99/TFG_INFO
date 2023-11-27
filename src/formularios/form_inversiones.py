import tkinter as tk
from tkinter import ttk
from datetime import datetime
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL , COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA


class FormularioInversiones(tk.Toplevel):
   """"" 
    def __init__(self, panel_principal):

        self.title("Calculadora de Rentabilidad")
        self.config(bg=COLOR_CUERPO_PRINCIPAL)  # Ajusta esto según tu configuración
        self.geometry("400x200")  # Ajusta el tamaño según tus necesidades

        # Crear y configurar widgets
        self.accion_label = ttk.Label(self, text="Seleccione una acción:")
        self.acciones = ["AAPL", "GOOGL", "MSFT", "TSLA"]  # Lista de acciones de ejemplo
        self.accion_combobox = ttk.Combobox(self, values=self.acciones)
        self.accion_combobox.set(self.acciones[0])

        self.fecha_inicio_label = ttk.Label(self, text="Fecha de inicio (YYYY-MM-DD):")
        self.fecha_inicio_entry = ttk.Entry(self)

        self.fecha_fin_label = ttk.Label(self, text="Fecha de fin (YYYY-MM-DD):")
        self.fecha_fin_entry = ttk.Entry(self)

        self.calcular_button = ttk.Button(self, text="Calcular Rentabilidad", command=self.calcular_rentabilidad)

        self.resultado_label = ttk.Label(self, text="Resultado:")

        # Ubicar widgets en la ventana
        self.accion_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.accion_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.fecha_inicio_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.fecha_inicio_entry.grid(row=1, column=1, padx=10, pady=10)

        self.fecha_fin_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.fecha_fin_entry.grid(row=2, column=1, padx=10, pady=10)

        self.calcular_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.resultado_label.grid(row=4, column=0, columnspan=2, pady=10)

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
ventana = tk.Tk()

# Crear la instancia de la clase FormularioInversiones
formulario = FormularioInversiones(ventana)

# Iniciar el bucle de eventos
ventana.mainloop()
"""