import tkinter as tk
from config import  COLOR_CUERPO_PRINCIPAL


class FormularioPerfil():

    def __init__(self, panel_principal, logo):

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame( panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame( panel_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # Primer Label con texto
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Página en construcción")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)
