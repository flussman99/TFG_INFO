import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL , COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from formularios.form_login import FormularioLoginDesign
from formularios.form_pagina_construccion import FormularioPagConstruccion


class FormularioMaestroDesign(tk.Tk):

    def __init__(self):
        super().__init__()
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
        self.controles_menu_lateral()
        #Función que controla todo lo que hay en el cuerpo
        self.controles_cuerpo()


    #Ventana principal
    def config_window(self):
        #configuración inicial de la ventana
        self.title('Interfaz Metatrader')
        self.iconbitmap("./src/imagenes/favicon.ico")
        w, h = 1024, 600
        #self.geometry("%dx%d+0+0" % (w, h))
        util_ventana.centrar_ventana(self, w, h)
        

    def paneles(self):
        #Creación de paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_CUERPO_PRINCIPAL, width=150)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)    
   
    def controles_barra_superior(self):
        #Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)
        
        #Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="MetaTrader")
        self.labelTitulo.config(fg='#fff', font=(
            "Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        #Botón del menú lateral
        self.botonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.botonMenuLateral.pack(side=tk.LEFT)

        #Etiqueta de información --> Cambiar cuando consigamos logearnos por el usuario que corresponda
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Usuario No Registrado")
        self.labelTitulo.config(fg='#fff', font=(
            "Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)

    def controles_menu_lateral(self):
        #Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

        #Etiqueta de perfil
        self.labelPerfil = tk.Label(
            self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        #Botones del menú lateral
        self.botonPanel = tk.Button(self.menu_lateral)
        self.botonPerfil = tk.Button(self.menu_lateral)
        self.botonInversiones = tk.Button(self.menu_lateral)
        self.botonInfo = tk.Button(self.menu_lateral)
        self.botonAjustes = tk.Button(self.menu_lateral)

        botones_info = [
            ("Inicio", "\uf109", self.botonPanel, self.abrir_panel_inicio),
            ("Perfil", "\uf007", self.botonPerfil, self.abrir_panel_perfil),
            ("Inversiones", "\uf03e", self.botonInversiones, self.abrir_panel_pag_construccion),
            ("Información", "\uf129", self.botonInfo,self.abrir_panel_pag_construccion),
            ("Ajustes", "\uf013", self.botonAjustes,self.abrir_panel_pag_construccion)
        ]

        for text, icon, button, comando in botones_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu, comando)

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu, comando):
        button.config(text=f" {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu,
                      command = comando)
        button.pack(side=tk.TOP)
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
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

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


    def abrir_panel_inicio(self):
        self.limpiar_panel(self.cuerpo_principal)
        self.controles_cuerpo()

    def abrir_panel_perfil(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioLoginDesign(self.cuerpo_principal)

    def abrir_panel_pag_construccion(self):
        self.limpiar_panel(self.cuerpo_principal)
        FormularioPagConstruccion(self.cuerpo_principal, self.imgconstruccion)

    #Esta función lo que hace es limpiar el Label que había antes en lo que vayamos a modificar
    #porque si no se estarían sobreponiendo hasta el infinito
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()
