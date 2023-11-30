import tkinter as tk
from PIL import Image, ImageTk
from config import COLOR_CUERPO_PRINCIPAL

class FormularioPagInformacion(tk.Toplevel):
    
    def __init__(self, panel_principal, logo):
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.barra_inferior = tk.Frame(panel_principal)
        self.barra_inferior.pack(side=tk.RIGHT, fill='both', expand=True)

        self.labelTitulo = tk.Label(self.barra_superior, text="Información del proyecto")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.label_descripcion = tk.Label(self.barra_inferior, text="Descripción del proyecto:")
        self.label_descripcion.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.text_descripcion = tk.Text(self.barra_inferior, wrap=tk.WORD, height=10, width=50)
        self.text_descripcion.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
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

        self.label_participantes = tk.Label(self.barra_inferior, text="Participantes:")
        self.label_participantes.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.frame_participantes = tk.Frame(self.barra_inferior)
        self.frame_participantes.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.imagenes_participantes = []  # Lista para almacenar las referencias a las imágenes

        participantes = [
            {"nombre": "Alvaro Cordero", "imagen": "src/imagenes/participantes/alvaro.png"},
            {"nombre": "David Viejo", "imagen": "src/imagenes/participantes/david.png"},
            {"nombre": "Cristian Manzanas", "imagen": "src/imagenes/participantes/cristian.png"},
            {"nombre": "Notkero Gomez", "imagen": "src/imagenes/participantes/notkero.png"},
            {"nombre": "Jose Antonio del rio", "imagen": "src/imagenes/participantes/participantes.png"},
        ]

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


