import tkinter as tk
import util.util_ventana as util_ven
from tkinter import ttk, messagebox, Canvas, Entry, Text, Button, PhotoImage


#Aquí habrá que hacer que cuando se acceda a la sesión Perfil, nos salga el login, pero que cuando estemos logeados nos salga información
#sobre el perfil del usuario
class FormularioInicioDesign(tk.Toplevel):

    def __init__(self, panel_principal):

        #Configuración inicial de la ventana
        self.cuerpo_principal = tk.Frame(panel_principal, width=798, height=553)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
        
        self.cuerpo_principal.configure(bg = "#FFFFFF")


        canvas = Canvas(
            self.cuerpo_principal,
            bg = "#FFFFFF",
            height = 553,
            width = 798,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        image_image_1 = PhotoImage(
            file="src/imagenes/assets/fondo.png")
        image_1 = canvas.create_image(
            399.0,
            276.0,
            image=image_image_1
        )

        image_image_2 = PhotoImage(
            file="src/imagenes/assets/logo_grande.png")
        image_2 = canvas.create_image(
            399.0,
            277.0,
            image=image_image_2
        )

        #self.cuerpo_principal.resizable(False, False)

        # self.title('Metatrader')
        # self.iconbitmap("./src/imagenes/favicon.ico")
        # w, h = 1024, 600
        # util_ven.centrar_ventana(self, w, h)
