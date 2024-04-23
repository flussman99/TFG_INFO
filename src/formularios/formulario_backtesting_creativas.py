import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Entry, Text, Button, PhotoImage
from config2 import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_imagenes as util_img
import pandas as pd
import psutil
import os
import sys 
from bot import Bot as bt
import MetaTrader5 as mt5 #Importamos libreria de metatrader le metemos el as para utilizarla con un nombre mas corto
import matplotlib.pyplot as plt
import mysql.connector
from configDB import DBConfig


class FormularioBackTestingCreativas():

    def __init__(self, panel_principal):

        self.frame_width = 0
        self.frame_height = 0

        #Frame principal
        self.frame_principal = tk.Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Frame superior 
        self.frame_superior = tk.Frame(self.frame_principal, bg="lightblue")
        self.frame_superior.pack(fill=tk.BOTH, expand=True)

        #Titulo frame superior
        self.label_titulo = tk.Label(self.frame_superior, text="Backtesting Operaciones Creativas", font=("Berlin Sans FB", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_titulo.place(relx=0.05, rely=0.1)

        # Frame inferior (con scrollbar)
        self.frame_inferior = tk.Frame(self.frame_principal, bg="lightgray")
        self.frame_inferior.pack(fill=tk.BOTH, expand=True)

        #ComboBoxs
        self.crear_combo_boxs()

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)   

        #Llamada a la función on_parent_configure cuando se redimensiona la ventana
        panel_principal.bind("<Configure>", self.on_parent_configure)

    def crear_combo_boxs(self):
        #Crear frame para añadir todo los combo boxs
        self.frame_combo_boxs = tk.Frame(self.frame_superior, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_combo_boxs.place(relx=0.05, rely=0.3)

        #Label de "Elige operación creativa"
        self.label_operacion_creativa = tk.Label(self.frame_combo_boxs, text="Elige operación creativa", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_operacion_creativa.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        #ComboBox de operaciones creativas
        self.combo_operaciones_creativas = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_operaciones_creativas.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        self.combo_operaciones_creativas["values"] = ["Fútbol", "Fórmula 1", "Películas", "Operacion 4", "Operacion 5"]

        #Opcion seleccionada
        self.opcion = self.combo_operaciones_creativas.get()

        #Evento de cambio de valor en el combobox
        self.combo_operaciones_creativas.bind("<<ComboboxSelected>>", self.actualizar_vista_opcion)

    def actualizar_vista_opcion(self, event):
        self.opcion = self.combo_operaciones_creativas.get()
        print("---------------------")
        if self.opcion == "Fútbol":
            print("Fútbol")
            self.operacion_futbol()
        elif self.opcion == "Fórmula 1":
            self.operacion_formula1()
        elif self.opcion == "Películas":
            self.operacion_peliculas()
        
        self.on_parent_configure(event)

    def operacion_futbol(self):
        print("Operacion futbol")
        #label de "Elige la liga"
        self.label_liga = tk.Label(self.frame_combo_boxs, text="Elige la liga", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_liga.grid(row=0, column=1, padx=10, pady=2, sticky="w")

        #ComboBox de ligas
        self.combo_ligas = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_ligas.grid(row=1, column=1, padx=10, pady=2, sticky="w")
        self.combo_ligas["values"] = ["Liga Santander", "Premier League", "Serie A", "Bundesliga", "Ligue 1"]
    
        #Opcion seleccionada
        self.liga = self.combo_ligas.get()

        #Actualizar vista al cambiar de liga
        self.combo_ligas.bind("<<ComboboxSelected>>", self.actualizar_vista_liga)

    def operacion_formula1(self):
        pass

    def operacion_peliculas(self):
        pass

    def actualizar_vista_liga(self, event):
        self.liga = self.combo_ligas.get()
        print("---------------------")
        if self.liga == "Liga Santander":
            print("Liga Santander")
            self.operacion_liga_santander()
        elif self.liga == "Premier League":
            print("Premier League")
        elif self.liga == "Serie A":
            print("Serie A")
        elif self.liga == "Bundesliga":
            print("Bundesliga")
        elif self.liga == "Ligue 1":
            print("Ligue 1")
        
        self.on_parent_configure(event)
    
    def operacion_liga_santander(self):

        print("Liga santander")
        #Label de "Elige el equipo"
        self.label_equipo = tk.Label(self.frame_combo_boxs, text="Elige el equipo", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_equipo.grid(row=0, column=2, padx=10, pady=2, sticky="w")

        #ComboBox de equipos
        self.combo_equipos = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_equipos.grid(row=1, column=2, padx=10, pady=2, sticky="w")

        #Dependiendo de la liga seleccionada se cargan los equipos
        if self.liga == "Liga Santander":
            self.combo_equipos["values"] = ["Real Madrid", "Barcelona", "Atlético de Madrid", "Valencia"]
        elif self.liga == "Premier League":
            self.combo_equipos["values"] = ["Arsenal", "Manchester United", "Manchester City", "Chelsea", "Liverpool"]
        elif self.liga == "Serie A":
            self.combo_equipos["values"] = ["Inter de Milán", "Milán", "Juventus", "Atalanta", "Napoli"]
        elif self.liga == "Bundesliga":
            self.combo_equipos["values"] = ["Bayern de Múnich", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen"]
        elif self.liga == "Ligue 1":
            self.combo_equipos["values"] = ["Lille", "PSG", "Mónaco", "Lyon", "Marsella"]



    def obtener_dimensiones(self):
        print("Obteniendo dimensiones")
        self.frame_width = self.frame_principal.winfo_width() 
        self.frame_height = self.frame_principal.winfo_height()
        print("Ancho: ", self.frame_width)
        print("Alto: ", self.frame_height)

    def on_parent_configure(self, event):
        # Se llama cuando cambia el tamaño de la ventana
        self.obtener_dimensiones()
        self.update()

    def on_parent_configure2(self):
        # Se llama cuando cambia el tamaño de la ventana
        if (self.frame_width != self.frame_principal.winfo_width() or self.frame_height != self.frame_principal.winfo_height()):
            self.obtener_dimensiones()
            self.update()
        self.frame_principal.after(1000, self.on_parent_configure2)

    def update(self):
        #Ajustar el tamaño del titulo
        self.label_titulo.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.2), "bold"))
        
        #Ajustar label elegir operacion creativa
        self.label_operacion_creativa.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

        #Ajustar with combobox
        self.combo_operaciones_creativas.configure(width=int(self.frame_width * 0.02))
        
        #Ajustar label elegir liga
        if self.opcion == "Fútbol":
            self.label_liga.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.combo_ligas.configure(width=int(self.frame_width * 0.02))
