import tkinter as tk
from config import  COLOR_CUERPO_PRINCIPAL
import mysql.connector
from configDB import DBConfig
from tkinter import ttk, messagebox, Canvas, Entry, Text, Button, PhotoImage

class FormularioPerfil():

    def obtener_dimensiones(self):
        print("Obteniendo dimensiones")
        self.frame_width = self.frame_azul.winfo_width() * 0.6
        self.frame_height = self.frame_azul.winfo_height() * 0.8

        print(self.frame_width)
        print(self.frame_height)

    def __init__(self, panel_principal, user_id):

        # Obtención id del usuario
        self.id_user = user_id

        # Dimensiones del frame
        self.frame_width = 1
        self.frame_height = 1

        # Tamaño de la fuente basado en las dimensiones del frame
        self.font_size = int(min(self.frame_width, self.frame_height) * 0.2)

        # Crear un frame interno para el panel azul
        self.frame_azul = tk.Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL, bd=0, highlightthickness=0)
        self.frame_azul.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.8)

        # Conexión a la base de datos
        self.conn = mysql.connector.connect(
                    host=DBConfig.HOST,
                    user=DBConfig.USER,
                    password=DBConfig.PASSWORD,
                    database=DBConfig.DATABASE,
                    port=DBConfig.PORT
                )


        #Tabla Inversiones por usuario
        self.label_tabla = tk.Label(self.frame_azul, bg=COLOR_CUERPO_PRINCIPAL, text="MIS INVERSIONES GUARDADAS", font=("Helvetica", int(self.font_size*0.25)), fg="grey")
        self.label_tabla.pack(padx=0)

        # Crear una tabla en el frame azul
        self.tabla = ttk.Treeview(self.frame_azul)
        self.tabla["columns"] = ("Nombre", "Tipo", "Fecha Inicio", "Fecha Fin", "Rentabilidad", "Datos")
        self.tabla.column("#0", width=0, stretch=tk.NO)
        self.tabla.column("Nombre", width=100)
        self.tabla.column("Tipo", width=100)
        self.tabla.column("Fecha Inicio", width=100)
        self.tabla.column("Fecha Fin", width=100)
        self.tabla.column("Rentabilidad", width=100)
        self.tabla.column("Datos", width=200)
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Tipo", text="Tipo")
        self.tabla.heading("Fecha Inicio", text="Fecha Inicial")
        self.tabla.heading("Fecha Fin", text="Fecha Final")
        self.tabla.heading("Rentabilidad", text="Rentabilidad")
        self.tabla.heading("Datos", text="Datos")
        self.tabla.pack(fill=tk.BOTH, expand=True)

        # Obtener el cursor para ejecutar consultas
        cursor = self.conn.cursor()

        # Consulta para obtener los datos de la tabla Inversiones segun el id_user correspondiente
        consulta = "SELECT nombre, tipo, fecha_inicio, fecha_fin, rentabilidad, datos FROM Inversiones WHERE id_usuario = %s"
        datos = (self.id_user,) 
        cursor.execute(consulta, datos)
        
        # Recorrer los resultados y agregarlos a la tabla
        for fila in cursor.fetchall():
            nombre, tipo, fecha_inicio, fecha_fin, rentabilidad, datos = fila
            self.tabla.insert("", tk.END, values=(nombre, tipo, fecha_inicio, fecha_fin, rentabilidad, datos))

        # Cerrar el cursor y la conexión
        cursor.close()
        self.conn.close()

    def cambiar_user(self, id_user):
        self.id_user = id_user
