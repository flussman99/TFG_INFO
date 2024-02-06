import tkinter as tk
from config import COLOR_CUERPO_PRINCIPAL

class FormularioAjustes(tk.Toplevel):
    
    def __init__(self, panel_principal):
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.barra_inferior = tk.Frame(panel_principal)
        self.barra_inferior.pack(side=tk.RIGHT, fill='both', expand=True)

        self.labelTitulo = tk.Label(self.barra_superior, text="Ajustes")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)



