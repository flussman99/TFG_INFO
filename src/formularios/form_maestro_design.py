import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL , COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from formularios.form_login import FormularioLoginDesign
from formularios.form_pagina_construccion import FormularioPagConstruccion
from formularios.form_pagina_informacion import FormularioPagInformacion
from formularios.form_inversiones import FormularioInversiones
from formularios.form_operaciones import FormularioOperaciones
from formularios.form_operaciones_creativas import FormularioOperacionesCreativas
from formularios.form_inicio import FormularioInicioDesign
from formularios.form_ajustes import FormularioAjustes
import mysql.connector
from configDB import DBConfig

class FormularioMaestroDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        #Establecemos conexión con la base de datos
        self.conn = mysql.connector.connect(
            host=DBConfig.HOST,
            user=DBConfig.USER,
            password=DBConfig.PASSWORD,
            database=DBConfig.DATABASE,
            port=DBConfig.PORT
        )

        self.logo = util_img.leer_imagen("./src/imagenes/meta-trader-5-logo.png", (560,135))
        self.perfil = util_img.leer_imagen("./src/imagenes/usuario.png", (100,100))
        self.imgconstruccion = util_img.leer_imagen("./src/imagenes/construccion.png", (100,100))
        #Creación de la ventana principal
        self.config_window()
        #Creación de los paneles dentro de la ventana principal
        self.paneles()
        #Creación de los controles de la barra superior
        self.controles_barra_superior()
        #Creación de los controles de la barra lateral
        #self.controles_menu_lateral()
        #Función que controla todo lo que hay en el cuerpo
        self.controles_cuerpo()


    #Ventana principal
    def config_window(self):
        #configuración inicial de la ventana
        self.title('Interfaz Metatrader')
        self.iconbitmap("./src/imagenes/favicon.ico")
        #self.geometry("%dx%d+0+0" % (w, h))
        self.wm_state('zoomed')
        

    def paneles(self):
        #Creación de paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        # self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        # self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_CUERPO_PRINCIPAL, width=150)
        
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)    
   
    def controles_barra_superior(self):
        #Configuración de la barra superior
        ancho_menu = 15
        alto_menu = 35
        font_awesome = font.Font(family="FontAwesome", size=14)
        font_awesome_usuario = font.Font(family="FontAwesome", size=12)
        
        #Imagen de metatrader para la barra superior
        imagen_logo = Image.open("./src/imagenes/meta-trader-5-logo.png")
        imagen_logo = imagen_logo.resize((150, 35))
        self.imagen_logo = ImageTk.PhotoImage(imagen_logo)
        label_logo = tk.Label(self.barra_superior, image=self.imagen_logo, bg=COLOR_BARRA_SUPERIOR)
        label_logo.pack(side=tk.LEFT, padx=5)

        #Contenedor de los botones
        self.contenedor_botones = tk.Frame(self.barra_superior, bg=COLOR_BARRA_SUPERIOR)
        self.contenedor_botones.pack(side=tk.LEFT, padx=5)
        
        

        #Botón del menú lateral
        # self.botonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
        #                                    command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        # self.botonMenuLateral.pack(side=tk.LEFT)

        #Etiqueta de información --> Cambiar cuando consigamos logearnos por el usuario que corresponda
        
        self.usuario_logged = False
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Usuario No Registrado", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.config(fg='#fff', font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)



        #Botones menu superior
        self.botonPanel = tk.Button(self.contenedor_botones)
        self.botonPerfil = tk.Button(self.contenedor_botones)
        self.botonInversiones = tk.Button(self.contenedor_botones, state=tk.DISABLED)
        self.botonOperaciones = tk.Button(self.contenedor_botones, state=tk.DISABLED)
        self.botonOperacionesCreativas = tk.Button(self.contenedor_botones, state=tk.DISABLED)
        self.botonInfo = tk.Button(self.contenedor_botones)

        botones_info = [
            ("Inicio", "\uf109", self.botonPanel, self.abrir_panel_inicio),
            ("Perfil", "\uf007", self.botonPerfil, self.abrir_panel_perfil),
            ("Inversiones", "\uf1da", self.botonInversiones, self.abrir_panel_inversiones),
            ("Operaciones", "\uf201", self.botonOperaciones, self.abrir_panel_operaciones),
            ("Ops Creativas", "\uf1fc", self.botonOperacionesCreativas, self.abrir_panel_operaciones_creativas),
            ("Información", "\uf129", self.botonInfo, self.abrir_panel_informacion)
        ]

        for text, icon, button, comando in botones_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu, comando)

        self.contenedor_botones.place(relx=0.5 ,rely=0.5, anchor=tk.CENTER)


   
    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu, comando):
        button.config(text=f" {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white", width=ancho_menu, height=alto_menu,
                      command = comando)
        button.pack(side=tk.LEFT)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        #Asociamos eventos de enter y leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))


    def on_enter(self, event, button):
        #Cambiar el estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        #Restaurar el estilo al salir el ratón del botón
        button.config(bg=COLOR_BARRA_SUPERIOR, fg='white')

    def toggle_panel(self):
        #Abrir y cerrar el menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    def controles_cuerpo(self):
        #Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo_principal, image=self.logo,bg=COLOR_CUERPO_PRINCIPAL)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        self.abrir_panel_inicio()



    def abrir_panel_inicio(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioInicioDesign(self.cuerpo_principal)

    def abrir_panel_perfil(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioLoginDesign(self.cuerpo_principal, self.labelTitulo, self.botonInversiones, self.botonOperaciones, self.botonOperacionesCreativas, self.abrir_panel_inicio, self.conn)

    def abrir_panel_pag_construccion(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioPagConstruccion(self.cuerpo_principal, self.imgconstruccion)

    def abrir_panel_informacion(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioPagInformacion(self.cuerpo_principal)

    def abrir_panel_inversiones(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioInversiones(self.cuerpo_principal)

    def abrir_panel_operaciones(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioOperaciones(self.cuerpo_principal)

    def abrir_panel_operaciones_creativas(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioOperacionesCreativas(self.cuerpo_principal)


    def abrir_panel_ajustes(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioAjustes(self.cuerpo_principal)

    #Esta función lo que hace es limpiar el Label que había antes en lo que vayamos a modificar
    #porque si no se estarían sobreponiendo hasta el infinito
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()
