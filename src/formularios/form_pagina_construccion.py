import tkinter as tk
from config import COLOR_CUERPO_PRINCIPAL

class FormularioPagConstruccion(tk.Toplevel):
    
    def __init__(self, panel_principal, logo):
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP,fill=tk.X,expand=False)

        self.barra_inferior = tk.Frame(panel_principal)
        self.barra_inferior.pack(side=tk.RIGHT,fill='both',expand=True)

        self.labelTitulo = tk.Label(self.barra_superior, text="Página en construcción")
        self.labelTitulo.config(fg="#222d33",font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        
        self.label_imagen = tk.Label(self.barra_inferior, image=logo)
        self.barra_inferior.place(x=0,y=0,relwidth=1, relheight=1)
        self.label_imagen.config(fg="#fff", font=("Roboto", 10), bg=COLOR_CUERPO_PRINCIPAL)