import tkinter as tk
from tkinter import font
from config2 import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
# Nuevo
from formularios.formulario_inicio_sesion import FormularioInicioSesion
from formularios.formulario_clasicas import FormularioClasicas
from formularios.formulario_creativas import FormularioCreativas
from formularios.formulario_informacion import FormularioInformacion
from formularios.formulario_perfil import FormularioPerfil
import tkinter as tk
from tkinter import font
import bot as bt
import MetaTrader5 as mt5
import ordenes as ord


class FormularioMaestroDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        self.config_window()
        self.paneles()
        self.controles_barra_superior()        
        self.controles_menu_lateral()
        self.controles_cuerpo()

        #Al cerrar la ventana se cierra la aplicación
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def cerrar_aplicacion(self):
        print("------------Cerrando aplicación------------")
        #DAVID aqui para parar los threads BOTELLA DE AGUA
        if(bt.Bot is not None):
            bt.Bot.kill_threads(bt.Bot)
            print(bt.Bot.trading_data)
            ord.cerrar_todas_las_posiciones(bt.Bot.trading_data)
        bt.Bot = None
        self.destroy()
    
    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Consejo de Sabios')
        w, h = 1024, 600        
        util_ventana.centrar_ventana(self, w, h)        

    def paneles(self):        
         # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
    
    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Botón del menú lateral
        self.icono_menu = util_img.leer_imagen("src/imagenes/iconos/menu.png", (20, 20))

        self.buttonMenuLateral = tk.Button(self.barra_superior, image=self.icono_menu, bg=COLOR_BARRA_SUPERIOR,
                           command=self.toggle_panel, bd=0)
        self.buttonMenuLateral.pack(side=tk.LEFT, padx=(10, 10))

        # Logo en chiquitito
        self.logo_chiquitito = util_img.leer_imagen("src/imagenes/formulario_maestro/logo_reducido.png", (40, 40))
        self.labelLogoChiquitito = tk.Label(self.barra_superior, image=self.logo_chiquitito, bg=COLOR_BARRA_SUPERIOR)
        self.labelLogoChiquitito.pack(side=tk.LEFT)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Consejo de Sabios")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        #Booleano para saber si se ha iniciado sesión
        self.bool_inicio = False

        # Etiqueta de informacion
        self.labelUsuario = tk.Label(self.barra_superior, text="INICIAR SESIÓN", cursor="hand2")
        self.labelUsuario.bind("<Button-1>", self.abrir_panel_inicio_sesion)
        self.labelUsuario.config(fg="#fff", font=("Roboto", 10, "bold"), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelUsuario.pack(side=tk.RIGHT)
    
    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

        self.perfil = util_img.leer_imagen("src/imagenes/formulario_maestro/usuario.png", (70, 70))

         
        # Etiqueta de perfil
        self.labelPerfil = tk.Label(
            self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Botones del menú lateral
        
        self.boton_operaciones = tk.Button(self.menu_lateral, state=tk.DISABLED)
        self.boton_operaciones_creativas = tk.Button(self.menu_lateral, state=tk.DISABLED)
        self.boton_perfil = tk.Button(self.menu_lateral, state=tk.DISABLED)
        self.boton_informacion = tk.Button(self.menu_lateral, state=tk.DISABLED)        

        buttons_info = [
            ("Op. Clásicas", "\uf03e", self.boton_operaciones,self.abrir_panel_clasicas),
            ("Op. Creativas", "\uf129", self.boton_operaciones_creativas,self.abrir_panel_creativas),
            ("Perfil", "\uf129", self.boton_perfil,self.abrir_panel_perfil),
            ("Información", "\uf013", self.boton_informacion,self.abrir_panel_informacion)
        ]

        for text, icon, button,comando in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu,comando)                    
    
    def controles_cuerpo(self):
        # Define the width and height variables
        width = 500
        height = 300
        # Imagen en el cuerpo principal
        self.logo = util_img.leer_imagen("src/imagenes/formulario_maestro/logoSinFondo.png", (width, height))
        label = tk.Label(self.cuerpo_principal, image=self.logo,
                 bg=COLOR_CUERPO_PRINCIPAL)
        label.pack(fill='both', expand=True)       
  
    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu, comando):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu,
                      command = comando)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')
    # Nuevo

    def abrir_panel_inicio_sesion(self, event):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioInicioSesion(self.cuerpo_principal, self.controles_cuerpo, self.cambiar_estado_sesion, self.bool_inicio) 

    def abrir_panel_clasicas(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioClasicas(self.cuerpo_principal, self.user_id, self.deshabilitar_botones, self.habilitar_botones) 

    def abrir_panel_creativas(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioCreativas(self.cuerpo_principal, self.user_id, self.deshabilitar_botones, self.habilitar_botones) 

    def abrir_panel_informacion(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioInformacion(self.cuerpo_principal)

    def abrir_panel_perfil(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioPerfil(self.cuerpo_principal, self.user_id)                     

    def limpiar_panel(self,panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()

    def habilitar_botones(self):
        self.boton_operaciones.config(state="normal")
        self.boton_operaciones_creativas.config(state="normal")
        self.boton_perfil.config(state="normal")
        self.boton_informacion.config(state="normal")

    def deshabilitar_botones(self):
        self.boton_operaciones.config(state="disabled")
        self.boton_operaciones_creativas.config(state="disabled")
        self.boton_perfil.config(state="disabled")
        self.boton_informacion.config(state="disabled")

    def cambiar_estado_sesion(self, user_id):
        if self.bool_inicio == False:
            self.bool_inicio = True
            self.user_id = user_id
            self.labelUsuario.config(text="CERRAR SESIÓN")
            self.habilitar_botones()
        else:
            self.bool_inicio = False
            self.labelUsuario.config(text="INICIAR SESIÓN")
            self.boton_operaciones.config(state="disabled")
            self.boton_operaciones_creativas.config(state="disabled")
            self.boton_perfil.config(state="disabled")
            self.boton_informacion.config(state="disabled")