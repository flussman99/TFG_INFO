import tkinter as tk
from config import  COLOR_CUERPO_PRINCIPAL
import mysql.connector
from configDB import DBConfig
from tkinter import ttk

class FormularioPerfil():


    def __init__(self, panel_principal, user_id):

        # Obtención id del usuario
        self.id_user = user_id

        # Dimensiones del frame
        self.frame_width = 1
        self.frame_height = 1

        # Tamaño de la fuente basado en las dimensiones del frame
        self.font_size = int(min(self.frame_width, self.frame_height) * 0.2)

        # Crear un frame interno para el panel azul
        self.frame_principal = tk.Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL, bd=0, highlightthickness=0)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Conexión a la base de datos
        self.conn = mysql.connector.connect(
                    host=DBConfig.HOST,
                    user=DBConfig.USER,
                    password=DBConfig.PASSWORD,
                    database=DBConfig.DATABASE,
                    port=DBConfig.PORT
                )


        #Tabla Inversiones por usuario
        self.label_tabla = tk.Label(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL, text="MIS INVERSIONES GUARDADAS", font=("Berlin Sans FB", 21, "bold"), fg="#2d367b")
        self.label_tabla.pack(padx=0, anchor="n", fill=tk.X)

        # Crear una tabla en el frame principal
        self.tabla = ttk.Treeview(self.frame_principal)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), foreground="blue")
        self.tabla["columns"] = ("Nombre", "Tipo", "Accion", "Fecha Inicio", "Fecha Fin", "Compra", "Venta", "Frec.", "Rent.", "Rent. IBEX", "Rent. SP", "Rent. PF")
        self.tabla.column("#0", width=0, stretch=tk.NO)
        self.tabla.column("Nombre", width=100)
        self.tabla.column("Tipo", width=65)
        self.tabla.column("Accion", width=100)
        self.tabla.column("Fecha Inicio", width=55)
        self.tabla.column("Fecha Fin", width=55)
        self.tabla.column("Compra", width=100)
        self.tabla.column("Venta", width=100)
        self.tabla.column("Frec.", width=100)
        self.tabla.column("Rent.", width=100)
        self.tabla.column("Rent. IBEX", width=100)
        self.tabla.column("Rent. SP", width=100)
        self.tabla.column("Rent. PF", width=100)
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Tipo", text="Tipo")
        self.tabla.heading("Accion", text="Accion")
        self.tabla.heading("Fecha Inicio", text="Fecha Inicial")
        self.tabla.heading("Fecha Fin", text="Fecha Final")
        self.tabla.heading("Compra", text="Compra")
        self.tabla.heading("Venta", text="Venta")
        self.tabla.heading("Frec.", text="Frec.")
        self.tabla.heading("Rent.", text="Rent.")
        self.tabla.heading("Rent. IBEX", text="Rent. IBEX")
        self.tabla.heading("Rent. SP", text="Rent. SP")
        self.tabla.heading("Rent. PF", text="Rent. PF")
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Obtener el cursor para ejecutar consultas
        cursor = self.conn.cursor()

        # Consulta para obtener los datos de la tabla Inversiones segun el id_user correspondiente
        consulta = "SELECT nombre, tipo, accion, fecha_inicio, fecha_fin, compra, venta, frecuencia, rentabilidad, rentabilidad_ibex, rentabilidad_sp, rentabilidad_plazos  FROM Inversiones WHERE id_usuario = %s"
        datos = (self.id_user,) 
        cursor.execute(consulta, datos)
        
        # Recorrer los resultados y agregarlos a la tabla
        for fila in cursor.fetchall():
            nombre, tipo, accion, fecha_inicio, fecha_fin, compra, venta, frecuencia, rentabilidad, rentabilidad_ibex, rentabilidad_sp, rentabilidad_plazos = fila
            self.tabla.insert("", tk.END, values=(nombre, tipo, accion, fecha_inicio, fecha_fin, compra, venta, frecuencia, rentabilidad, rentabilidad_ibex, rentabilidad_sp, rentabilidad_plazos))

        # Cerrar el cursor y la conexión
        cursor.close()
        self.conn.close()

        self.tabla.bind("<Configure>", self.ajustar_tabla)

    def ajustar_tabla(self, event):
        width = event.width
        self.tabla.column("Nombre", width=int(width * 0.05))
        self.tabla.column("Tipo", width=int(width * 0.06))
        self.tabla.column("Accion", width=int(width * 0.06))
        self.tabla.column("Fecha Inicio", width=int(width * 0.05))
        self.tabla.column("Fecha Fin", width=int(width * 0.05))
        self.tabla.column("Compra", width=int(width * 0.035))
        self.tabla.column("Venta", width=int(width * 0.035))
        self.tabla.column("Frec.", width=int(width * 0.035))
        self.tabla.column("Rent.", width=int(width * 0.035))
        self.tabla.column("Rent. IBEX", width=int(width * 0.035))
        self.tabla.column("Rent. SP", width=int(width * 0.035))
        self.tabla.column("Rent. PF", width=int(width * 0.035))