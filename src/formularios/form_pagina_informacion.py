import tkinter as tk
from PIL import Image, ImageTk
from config import COLOR_CUERPO_PRINCIPAL
from tkinter import ttk, messagebox, Canvas, Entry, Text, Button, PhotoImage

class FormularioPagInformacion(tk.Toplevel):
    
    def __init__(self, panel_principal):

        #Configuración inicial de la ventana
        self.cuerpo_principal = tk.Frame(panel_principal, width=1366, height=667)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
        
        self.cuerpo_principal.configure(bg = "#FFFFFF")


        canvas = Canvas(
            self.cuerpo_principal,
            bg = "#FFFFFF",
            height = 667,
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
            333.0,
            image=image_image_1
        )


        self.titulo_mercado = ttk.Label(self.cuerpo_principal, text="Información del Proyecto:")
        self.titulo_mercado.place(x=683.0, y=40, width=400, height=38.0, anchor='center')
        self.titulo_mercado.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 24), anchor='center')


        self.titulo_mercado = ttk.Label(self.cuerpo_principal, text="Descripción del Proyecto:")
        self.titulo_mercado.place(x=35.0, y=100, width=300, height=38.0)
        self.titulo_mercado.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 18))

        self.text_descripcion = tk.Text(self.cuerpo_principal, wrap=tk.WORD, height=10, width=50)
        self.text_descripcion.place(x=35.0, y=150, width=1295, height=200)
        self.text_descripcion.insert(tk.END, """
        Trabajo de Fin de Grado: Aplicación de Análisis de Precios de Acciones

        Este proyecto se centra en el desarrollo de una aplicación que tiene como objetivo realizar comparativas exhaustivas de análisis sobre los precios de las acciones en el mercado financiero. La aplicación emplea diversas características y sucesos reales para evaluar y entender las fluctuaciones en los precios de las acciones.

        Características principales:
        - Análisis detallado de datos históricos de precios de acciones.
        - Identificación y consideración de características específicas de las acciones.
        - Evaluación de eventos y sucesos reales que impactan en los mercados financieros.

        La aplicación proporciona una interfaz intuitiva para que los usuarios exploren y comprendan mejor el comportamiento del mercado. Además, permite comparar diferentes análisis y escenarios, facilitando la toma de decisiones informadas en el ámbito financiero.

        Este proyecto busca no solo ofrecer una herramienta práctica para analistas financieros y profesionales del mercado, sino también servir como un aporte significativo al campo de estudio de la inversión y finanzas.

        ¡Explora, analiza y comprende el mundo financiero con nuestra aplicación de Análisis de Precios de Acciones!
        """)

        self.titulo_mercado = ttk.Label(self.cuerpo_principal, text="Participantes:")
        self.titulo_mercado.place(x=35.0, y=375, width=175, height=38.0)
        self.titulo_mercado.configure(background='#30A4B4', foreground='black', font=('Calistoga Regular', 18))

        self.frame_participantes = tk.Frame(self.cuerpo_principal)
        self.frame_participantes.place(x=35.0, y=425, width=750, height=175)
        
        self.imagenes_participantes = []  # Lista para almacenar las referencias a las imágenes

        participantes = [
            {"nombre": "Alvaro Cordero", "imagen": "src/imagenes/participantes/alvaro.png"},
            {"nombre": "David Viejo", "imagen": "src/imagenes/participantes/david.png"},
            {"nombre": "Cristian Manzanas", "imagen": "src/imagenes/participantes/cristian.png"},
            {"nombre": "Notkero Gomez", "imagen": "src/imagenes/participantes/notkero.png"},
            {"nombre": "Jose Antonio del rio", "imagen": "src/imagenes/participantes/jose.png"},
        ]

        self.imagenes_participantes = []

        for i, participante in enumerate(participantes):
            nombre = participante["nombre"]
            imagen_path = participante["imagen"]

            imagen = Image.open(imagen_path)
            imagen = imagen.resize((125, 125), Image.BICUBIC)  # Ajusta el tamaño de la imagen según sea necesario
            imagen_tk = ImageTk.PhotoImage(imagen)

            label_imagen_participante = tk.Label(self.frame_participantes, image=imagen_tk)
            label_imagen_participante.grid(row=0, column=i, padx=(10, 10), pady=(10, 0), sticky="n")  # Ajusta padx, pady y sticky

            label_participante = tk.Label(self.frame_participantes, text=nombre)
            label_participante.grid(row=1, column=i, padx=(10, 10), pady=(0, 10), sticky="s")  # Ajusta padx, pady y sticky

            # Asegúrate de mantener una referencia a las imágenes para evitar que se eliminen
            label_imagen_participante.image = imagen_tk
            self.imagenes_participantes.append(imagen_tk)




        

        self.cuerpo_principal.mainloop()
