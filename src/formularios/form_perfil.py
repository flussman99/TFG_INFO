import tkinter as tk
import util.util_ventana as util_ven

#Aquí habrá que hacer que cuando se acceda a la sesión Perfil, nos salga el login, pero que cuando estemos logeados nos salga información
#sobre el perfil del usuario
class FormularioPerfilDesign(tk.Toplevel):

    def __init__(self) -> None:
        super().__init__()
    
    def config_window(self):
        #Configuración inicial de la ventana
        self.title('Metatrader')
        self.iconbitmap("./src/imagenes/favicon.ico")
        w, h = 1024, 600
        util_ven.centrar_ventana(self, w, h)
