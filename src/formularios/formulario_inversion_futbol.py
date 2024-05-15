import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Canvas, Entry, Text, Button, PhotoImage
from config2 import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_imagenes as util_img
from bot import Bot as bt
import tick_reader as tr
import mysql.connector
from configDB import DBConfig
import MetaTrader5 as mt5 #Importamos libreria de metatrader le metemos el as para utilizarla con un nombre mas corto
from EquiposdeFutbol import SBS_backtesting as SBS
import tkinter as tk
from datetime import datetime, timedelta
from formularios.formulario_mas_informacion import FormularioBackTestingMasInformacion
import ordenes as ORD  
import MetaTrader5 as mt5 



class FormularioInversionFutbol():

    def __init__(self, panel_principal, id_user, deshabilitar_botones, habilitar_botones):

        self.b = bt(1)
        self.id_user = id_user
        self.frame_width = 0
        self.frame_height = 0
        self.deshabilitar_botones = deshabilitar_botones
        self.habilitar_botones = habilitar_botones

        #Frame principal
        self.frame_principal = tk.Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Frame superior 
        self.frame_superior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL, width=399, height=276)
        self.frame_superior.pack(fill=tk.BOTH)

        #Titulo frame superior
        self.label_titulo_futbol = tk.Label(self.frame_superior, text="Inversión Operaciones Fútbol", font=("Berlin Sans FB", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_titulo_futbol.place(relx=0.05, rely=0.1)

        # Frame inferior (con scrollbar)
        self.frame_inferior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL, width=399, height=276)
        self.frame_inferior.pack(fill=tk.BOTH)

        #VARIABLES
        #Inicializar Labels
        self.label_liga = None
        self.label_equipo = None
        self.label_accion = None
        self.label_metodo_comprar = None
        self.label_metodo_vender = None
        self.label_inversion = None
        self.label_comparativa = None
        self.label_rentabilidad = None
        self.label_rentabilidad_futbol = None

        #Inicializar ComboBoxs
        self.combo_ligas = None
        self.combo_equipos = None
        self.combo_accion = None
        self.combo_metodos_comprar = None
        self.combo_metodos_vender = None
        
        self.ibex35 = None
        self.sp500 = None
        self.plazo_fijo = None

        self.label_rentabilidad_ibex35 = None
        self.label_rentabilidad_sp500 = None
        self.label_rentabilidad_plazo_fijo = None
        self.lotaje_usuario = None

        self.var_ibex35 = None
        self.var_sp500 = None
        self.var_plazo_fijo = None

        #Inicializar imagenes
        self.imagen_liga = None
        self.imagen_equipo = None
        self.imagen_accion = None

        #Inicializar variables
        self.label_lotaje = None
        self.label_stop_loss = None
        self.label_take_profit = None
        self.stop_loss_entry = None
        self.take_profit_entry = None
        self.lotaje_entry = None
        self.pais_seleccionado=None

        #Variables SBS
        self.ligas=SBS.ligas
        self.acciones=SBS.acciones
        self.pais=SBS.pais
        self.url=SBS.urls_equipos
        self.acronimos_acciones=SBS.acronimo_acciones_api
        self.acronimos_acciones_mt5=SBS.acronimo_acciones_mt5
        self.imagenes_liga=SBS.imagenes_ligas
        self.imagenes_equipos=SBS.imagenes_equipos

        #Variables de la tabla
        self.frame_without_filter=None
        self.current_frame = None
        self.frame_with_filter=None
        self.frame_directo=None
        self.tree = None
        self.tree_ticks = None

        #Botones
        self.boton_empezar_inversion_futbol = None
        self.boton_parar_inversion = None
        self.boton_guardar_inversion = None

        #Funciones recursivas
        self.funciones_recursivas=True

        #Indicadores comparacion 
        self.fecha_inicio_indicadores=0
        self.fecha_fin_indicadores=0

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

        #seguir
        self.operacion_futbol()

    def operacion_futbol(self):
        #label de "Elige la liga"
        self.label_liga = tk.Label(self.frame_combo_boxs, text="Elige la liga", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_liga.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        #ComboBox de ligas
        self.combo_ligas = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_ligas.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        self.combo_ligas["values"] = list(self.ligas.keys())
                
        #Ajustar vista
        self.on_parent_configure(None)

        #Actualizar vista al cambiar de liga
        self.combo_ligas.bind("<<ComboboxSelected>>", self.actualizar_futbol_equipo)

    def actualizar_futbol_equipo(self, event):
        #Coger la liga seleccionada
        self.liga = self.combo_ligas.get()

        #Poner todo vacio si ya se ha seleccionado algo
        if self.combo_equipos is not None:
            if self.combo_equipos == "":
                self.label_imagen_equipo.destroy()
            self.label_equipo.destroy()
            self.combo_equipos.destroy()
            self.label_imagen_liga.destroy()
            self.label_equipo = None
            self.combo_equipos = None
            if self.combo_accion is not None:
                self.label_imagen_equipo.destroy()
                self.label_accion.destroy()
                self.combo_accion.destroy()
                self.label_accion = None
                self.combo_accion = None

        if self.label_equipo is None:
            #Poner imagen de la liga
            self.imagen_liga = util_img.leer_imagen(self.imagenes_liga[self.liga], (10,10))
            self.label_imagen_liga = tk.Label(self.frame_superior, image=self.imagen_liga, bg=COLOR_CUERPO_PRINCIPAL)
            self.label_imagen_liga.place(relx=0.8, rely=0.1)

            #Label de "Elige el equipo"
            self.label_equipo = tk.Label(self.frame_combo_boxs, text="Elige el equipo", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_equipo.grid(row=0, column=1, padx=10, pady=2, sticky="w")

            #ComboBox de equipos
            self.combo_equipos = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_equipos.grid(row=1, column=1, padx=10, pady=2, sticky="w")
            self.combo_equipos["values"] = self.ligas[self.liga]

        #Ajustar vista
        self.on_parent_configure(event)

        #Actualizar vista al cambiar de equipo        
        self.combo_equipos.bind("<<ComboboxSelected>>", self.actualizar_futbol_accion)

    def actualizar_futbol_accion(self, event):
        #Coger el equipo seleccionado
        self.equipo = self.combo_equipos.get()
        #self.label_imagen_equipo.destroy()

        #Poner todo vacio si ya se ha seleccionado algo
        if self.combo_accion is not None:
            self.label_accion.destroy()
            self.combo_accion.destroy()
            self.label_accion = None
            self.combo_accion = None
        
        if self.label_accion is None:
            #Poner imagen del equipo
            self.imagen_equipo = util_img.leer_imagen(self.imagenes_equipos[self.equipo], (10,10))
            self.label_imagen_equipo = tk.Label(self.frame_superior, image=self.imagen_equipo, bg=COLOR_CUERPO_PRINCIPAL)
            self.label_imagen_equipo.place(relx=0.9, rely=0.1)
            
            #Label de "Elige acción"
            self.label_accion = tk.Label(self.frame_combo_boxs, text="Elige acción", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_accion.grid(row=0, column=2, padx=10, pady=2, sticky="w")

            #ComboBox de acciones
            self.combo_accion = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_accion.grid(row=1, column=2, padx=10, pady=2, sticky="w")
            self.combo_accion["values"] = self.acciones[self.equipo]
        
        #Actualizar vista al cambiar de accion        
        self.combo_accion.bind("<<ComboboxSelected>>", self.actualizar_futbol_metodos)

        #Ajustar vista
        self.on_parent_configure(event)

    def actualizar_futbol_metodos(self, event):
        #Coger la accion seleccionada
        self.accion = self.combo_accion.get()

        if self.label_metodo_comprar is None:
            #Label de "Elige cuando comprar"
            self.label_metodo_comprar = tk.Label(self.frame_combo_boxs, text="Elige cuando comprar", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_metodo_comprar.grid(row=2, column=0, padx=10, pady=2, sticky="w")

            #ComboBox de metodos comprar
            self.combo_metodos_comprar = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_metodos_comprar.grid(row=3, column=0, padx=10, pady=2, sticky="w")
            self.combo_metodos_comprar["values"] = ["Ganado", "Perdido", "Empatado", "Ganado/Empatado", "Empatado/Perdido", "Ganado/Perdido"]

            #label de "Elige cuando vender"
            self.label_metodo_vender = tk.Label(self.frame_combo_boxs, text="Elige cuando vender", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_metodo_vender.grid(row=2, column=1, padx=10, pady=2, sticky="w")

            #ComboBox de metodos vender
            self.combo_metodos_vender = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_metodos_vender.grid(row=3, column=1, padx=10, pady=2, sticky="w")
            self.combo_metodos_vender["values"] = ["Ganado", "Perdido", "Empatado", "Ganado/Empatado", "Empatado/Perdido", "Ganado/Perdido"]

        #Cuando o comprar o vender tenga un valor seleccionado quitar esa opcion del otro
        self.combo_metodos_comprar.bind("<<ComboboxSelected>>", self.actualizar_futbol_metodos_vender)
        self.combo_metodos_vender.bind("<<ComboboxSelected>>", self.actualizar_futbol_metodos_comprar)

        #Ajustar vista
        self.on_parent_configure(event)

    def actualizar_futbol_metodos_comprar(self, event):
        #Coger el metodo de vender seleccionado
        self.metodo_vender = self.combo_metodos_vender.get()
        
        #Quitar opciones dependiendo de lo que se eliga en vender, opciones especiales en cada caso
        if self.metodo_vender == "Ganado":
            self.combo_metodos_comprar["values"] = ["Perdido", "Empatado", "Empatado/Perdido"]
        elif self.metodo_vender == "Perdido":
            self.combo_metodos_comprar["values"] = ["Ganado", "Empatado", "Ganado/Empatado"]
        elif self.metodo_vender == "Empatado":
            self.combo_metodos_comprar["values"] = ["Ganado", "Perdido", "Ganado/Perdido"]
        elif self.metodo_vender == "Ganado/Empatado":
            self.combo_metodos_comprar["values"] = ["Perdido"]
        elif self.metodo_vender == "Empatado/Perdido":
            self.combo_metodos_comprar["values"] = ["Ganado"]
        elif self.metodo_vender == "Ganado/Perdido":
            self.combo_metodos_comprar["values"] = ["Empatado"]
       
        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.combo_metodos_comprar.get() != "" and self.combo_metodos_vender.get() != "":
            self.actualizar_comparativa()

        #Actualizar vista
        self.on_parent_configure(None)

    def actualizar_futbol_metodos_vender(self, event):
        #Coger el metodo de comprar seleccionado
        self.metodo_comprar = self.combo_metodos_comprar.get()

        #Quitar opciones dependiendo de lo que se eliga en comprar, opciones especiales en cada caso 
        if self.metodo_comprar == "Ganado":
            self.combo_metodos_vender["values"] = ["Perdido", "Empatado", "Empatado/Perdido"]
        elif self.metodo_comprar == "Perdido":
            self.combo_metodos_vender["values"] = ["Ganado", "Empatado", "Ganado/Empatado"]
        elif self.metodo_comprar == "Empatado":
            self.combo_metodos_vender["values"] = ["Ganado", "Perdido", "Ganado/Perdido"]
        elif self.metodo_comprar == "Ganado/Empatado":
            self.combo_metodos_vender["values"] = ["Perdido"]
        elif self.metodo_comprar == "Ganado/Perdido":
            self.combo_metodos_vender["values"] = ["Ganado"]
        elif self.metodo_comprar == "Ganado/Perdido":
            self.combo_metodos_vender["values"] = ["Empatado"]       
        
        
        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.combo_metodos_comprar.get() != "" and self.combo_metodos_vender.get() != "":
            self.actualizar_comparativa()

        #Actualizar vista
        self.on_parent_configure(None)

    def actualizar_comparativa(self):
        if self.label_comparativa is None:
            
            #Label de "Comparativa"
            self.label_comparativa = tk.Label(self.frame_combo_boxs, text="Comparativa", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_comparativa.grid(row=2, column=2, padx=10, pady=2, sticky="w")

            #CheckBox de comparativas
            self.var_ibex35 = tk.BooleanVar()
            self.var_sp500 = tk.BooleanVar()
            self.var_plazo_fijo = tk.BooleanVar()
            self.ibex35 = tk.Checkbutton(self.frame_combo_boxs, text="IBEX35", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_ibex35)
            self.ibex35.grid(row=3, column=2, padx=10, pady=2, sticky="w")
            self.sp500 = tk.Checkbutton(self.frame_combo_boxs, text="SP500", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_sp500)
            self.sp500.grid(row=3, column=3, padx=10, pady=2, sticky="w")
            self.plazo_fijo = tk.Checkbutton(self.frame_combo_boxs, text="Plazo Fijo", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_plazo_fijo)
            self.plazo_fijo.grid(row=3, column=4, padx=10, pady=2, sticky="w")

        #al mirar todos los datos actualizar el boton
        self.actualizar_lotajes(None)

        #Ajustar vista
        self.on_parent_configure(None)


    def actualizar_lotajes(self, event):
        if (self.label_stop_loss is None):
            #Entry stop loss
            self.label_stop_loss = tk.Label(self.frame_combo_boxs, text="Stop Loss", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_stop_loss.grid(row=4, column=0, padx=10, pady=2, sticky="w")

            self.stop_loss_entry = Entry(self.frame_combo_boxs, width=30)
            self.stop_loss_entry.grid(row=5, column=0, padx=10, pady=2, sticky="w")
        
        if (self.label_take_profit is None):
            #Entry take profit
            self.label_take_profit = tk.Label(self.frame_combo_boxs, text="Take Profit", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_take_profit.grid(row=4, column=1, padx=10, pady=2, sticky="w")

            self.take_profit_entry = Entry(self.frame_combo_boxs, width=30)
            self.take_profit_entry.grid(row=5, column=1, padx=10, pady=2, sticky="w")

        if self.label_lotaje is None:
            #Label lotaje
            self.label_lotaje = tk.Label(self.frame_combo_boxs, text="Lotaje", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_lotaje.grid(row=4, column=2, padx=10, pady=2, sticky="w")
            
            #Entry lotaje
            self.lotaje_entry = Entry(self.frame_combo_boxs, width=30)
            self.lotaje_entry.grid(row=5, column=2, padx=10, pady=2, sticky="w")

            # Información Lotaje del usuario
            lotaje_usu = mt5.account_info()
            self.lotaje_actual = lotaje_usu.balance
            self.lotaje_usuario = tk.Label(self.frame_combo_boxs, text="Balance disponible: " + str(self.lotaje_actual), font=("Aptos", 10), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.lotaje_usuario.grid(row=6, column=2, padx=10, pady=2, sticky="w")

            #Label inversion
            self.label_inversion = tk.Label(self.frame_combo_boxs, text="Inversión: ", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_inversion.grid(row=4, column=3, padx=10, pady=2, sticky="w")


        self.stop_loss_entry.bind("<KeyRelease>", self.actualizar_futbol_stop_loss)
        self.take_profit_entry.bind("<KeyRelease>", self.actualizar_futbol_take_profit)
        self.lotaje_entry.bind("<KeyRelease>", self.actualizar_futbol_lotaje)

        #Actualizar vista
        self.on_parent_configure(None)
    
    def guardar_inversion(self):
        # Conexión a la base de datos
        self.conn = mysql.connector.connect(
                    host=DBConfig.HOST,
                    user=DBConfig.USER,
                    password=DBConfig.PASSWORD,
                    database=DBConfig.DATABASE,
                    port=DBConfig.PORT
                )
        
        # Para ponerle nombre a la inversión, realizamos este bucle hasta que el usuario ingrese un nombrenombre_inversión = ""
        nombre_inversión = ""
        while True:
            # Dejamos que el usuario ingrese el nombre de la inversión que ha realizado
            nombre_inversión = simpledialog.askstring("Guardar inversión", "Ingrese el nombre de la inversión:", parent=self.frame_principal)

            if nombre_inversión is None:
                # Si se hace clic en Cancelar, salimos del bucle
                break

            if not nombre_inversión:
                # En el caso de que no se haya ingresado un nombre, mostramos mensaje de error y volvemos a pedirlo
                messagebox.showerror("Error", "Debes ingresar un nombre para tu inversión.")
                continue
            
            if self.nombre_inversion_existe(nombre_inversión):
                messagebox.showerror("Error", "Ya existe una inversión con ese nombre.")
                continue
            
            # Si llegamos a este punto, el usuario ha ingresado un nombre de inversión válido
            break

        if(nombre_inversión is None):
            return
        
        # Le damos valor al tipo de inversión que esta haciendo el usuario
        tipo = "Inversión Fútbol"

        # Cogemos la acción en la que ha invertido el usuario	
        accion = self.combo_accion.get()

        # Cogemos la fecha de inicio y la de fin de la inversión
        # Hay que cogerlo del treeview
        fecha_ini, fecha_fin = self.obtener_primer_ultimo_valor_fecha()

        #Cogemos cuando toma las decisiones de comprar y vender el usuario
        compra = self.combo_metodos_comprar.get()
        venta = self.combo_metodos_comprar.get()

        #Le damos valor a la frecuencia
        frecuencia = "Diaria"

        # Cogemos la rentabilidad de la inversión
        rentabilidad = str(self.rentabilidad_futbol.get()) + "%"

        # Cogemos la rentabilidad de los índices seleccionados
        if self.var_ibex35.get():
            rentabilidad_ibex = str(self.rentIbex35) + "%"
        else:
            rentabilidad_ibex = "No aplica"

        if self.var_sp500.get():
            rentabilidad_sp500 = str(self.rentSP) + "%"
        else:
            rentabilidad_sp500 = "No aplica"
        
        if self.var_plazo_fijo.get():
            rentabilidad_plazos = str(self.rentPF) + "%"
        else:
            rentabilidad_plazos = "No aplica"
        # Guardamos la inversión en la base de datos
        cursor = self.conn.cursor()
        try:
            # Realizamos la consulta para insertar los datos en la tabla Inversiones
            consulta = "INSERT INTO Inversiones (id_usuario, nombre, tipo, accion, fecha_inicio, fecha_fin, compra, venta, frecuencia, rentabilidad, rentabilidad_ibex, rentabilidad_sp, rentabilidad_plazos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            datos = (self.id_user, nombre_inversión, tipo, accion, fecha_ini, fecha_fin, compra, venta, frecuencia ,rentabilidad, rentabilidad_ibex, rentabilidad_sp500, rentabilidad_plazos)
            cursor.execute(consulta, datos)
        except Exception as e:
            print(e)
        
        # Cerramos el cursor y la conexxión
        cursor.close()
        self.conn.commit()
        self.conn.close()
    
    def obtener_primer_ultimo_valor_fecha(self):
        fechas = []
        for item in self.tree.get_children():
            # Obtener el índice de la columna "Fecha" en el Treeview
            indice_fecha = self.tree["columns"].index("Fecha")
            fecha = self.tree.item(item)["values"][indice_fecha]
            fechas.append(fecha)
        
        if fechas:
            primer_fecha = min(fechas)
            ultimo_fecha = max(fechas)
            return primer_fecha, ultimo_fecha
        else:
            return None, None

    def nombre_inversion_existe(self, nombre_inversion):
        # Obtener el cursor para ejecutar consultas
        cursor = self.conn.cursor()

        # Consulta para obtener los datos de la tabla Inversiones segun el id_user correspondiente
        consulta = "SELECT COUNT(*) FROM Inversiones WHERE id_usuario = %s AND nombre = %s"
        datos = (self.id_user, nombre_inversion) 
        cursor.execute(consulta, datos)
        cantidad = cursor.fetchone()[0]

        # Cerrar el cursor
        cursor.close()

        return cantidad > 0

    def actualizar_futbol_stop_loss(self, event):
        if self.stop_loss_entry.get() == "" and self.boton_empezar_inversion_futbol is not None:
            self.boton_empezar_inversion_futbol.configure(state="disabled")

        try:
            aux_loss = float(self.stop_loss_entry.get())

            # Aquí puedes usar 'aux', que contendrá el valor convertido a entero
        except ValueError:
            # Si no se puede convertir a entero, se maneja la excepción aquí
            # Por ejemplo, podrías mostrar un mensaje de error al usuario
            messagebox.showerror("Error", "El valor ingresado no es un número entero válido")

        #Actualizar vista
        self.on_parent_configure(event)

        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.lotaje_entry.get() != "" and self.stop_loss_entry.get() != "" and self.take_profit_entry.get() != "":
            self.actualizar_boton_inversion()

    def actualizar_futbol_take_profit(self, event):
        if self.take_profit_entry.get() == "" and self.boton_empezar_inversion_futbol is not None:
            self.boton_empezar_inversion_futbol.configure(state="disabled")

        try:
            aux_profit = float(self.take_profit_entry.get())

            # Aquí puedes usar 'aux', que contendrá el valor convertido a entero
        except ValueError:
            # Si no se puede convertir a entero, se maneja la excepción aquí
            # Por ejemplo, podrías mostrar un mensaje de error al usuario
            messagebox.showerror("Error", "El valor ingresado no es un número entero válido")

        #Actualizar vista
        self.on_parent_configure(event)

        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.lotaje_entry.get() != "" and self.stop_loss_entry.get() != "" and self.take_profit_entry.get() != "":
            self.actualizar_boton_inversion()

    def actualizar_futbol_lotaje(self, event):
        if self.lotaje_entry.get() == "" and self.boton_empezar_inversion_futbol is not None:
            self.boton_empezar_inversion_futbol.configure(state="disabled")

        try:
            aux = float(self.lotaje_entry.get())

            # Aquí puedes usar 'aux', que contendrá el valor convertido a entero
        except ValueError:
            # Si no se puede convertir a entero, se maneja la excepción aquí
            # Por ejemplo, podrías mostrar un mensaje de error al usuario
            messagebox.showerror("Error", "El valor ingresado no es un número entero válido")

    
        #Cambiar texto inversion
        self.valor_precio = self.getValorPrecio()
        self.valor_inversion = round(float(self.lotaje_entry.get()) * self.valor_precio, 2)
        self.label_inversion.configure(text="Inversión: " + str(self.valor_inversion))

        #Actualizar vista
        self.on_parent_configure(event)

        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.lotaje_entry.get() != "" and self.stop_loss_entry.get() != "" and self.take_profit_entry.get() != "":
            self.actualizar_boton_inversion()


    def getValorPrecio(self):
        accion=self.acronimos_acciones_mt5.get(self.combo_accion.get())
        selected = mt5.symbol_select(accion, True)
        print(accion)
        if selected:
            tick = mt5.symbol_info_tick(accion)
            precio=tick[2]
            
        return precio


    def actualizar_boton_inversion(self):

        # Boton de "Empezar inversion"
        self.boton_empezar_inversion_futbol = tk.Button(self.frame_combo_boxs, text="Empezar\ninversión", font=("Aptos", 12), bg="green", fg="white", command=self.empezar_inversion) # wraplength determina el ancho máximo antes de que el texto se divida en dos líneas
        self.boton_empezar_inversion_futbol.grid(row=4, column=4, rowspan=2, padx=10, pady=2, sticky="w")

        #Actualizar vista
        self.on_parent_configure(None)

    def empezar_inversion(self):

        # Verificar si se ha seleccionado una liga, un equipo, una acción, un método de compra, un método de venta y un lotaje
        if self.combo_ligas.get() == "" or self.combo_equipos.get() == "" or self.combo_accion.get() == "" or self.combo_metodos_comprar.get() == "" or self.combo_metodos_vender.get() == "" or self.lotaje_entry.get() == "":
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return
        
        # Deshabilitar los ComboBoxs, los Entry y el Botón de "Empezar inversión"
        self.deshabilitar_botones()
        self.combo_ligas.configure(state="disabled")
        self.combo_equipos.configure(state="disabled")
        self.combo_accion.configure(state="disabled")
        self.combo_metodos_comprar.configure(state="disabled")
        self.combo_metodos_vender.configure(state="disabled")
        self.stop_loss_entry.configure(state="disabled")
        self.take_profit_entry.configure(state="disabled")
        self.lotaje_entry.configure(state="disabled")
        self.boton_empezar_inversion_futbol.configure(state="disabled")
        self.ibex35.configure(state="disabled")
        self.sp500.configure(state="disabled")
        self.plazo_fijo.configure(state="disabled")



        # Verificar si la interfaz de usuario ya ha sido creada
        if not hasattr(self, 'frame_datos'):
            # Si no ha sido creada, entonces crearla
            self.crear_interfaz_inferior()
        else:
            # Si ya ha sido creada, limpiar el Treeview
            if self.tree is not None:
                print("LIMPIANDO TREEVIEW PARTIDOS")
                for item in self.tree.get_children():
                    self.tree.delete(item)
            if self.tree_ticks is not None:
                print("LIMPIANDO TREEVIEW TICkS")
                for item in self.tree_ticks.get_children():
                    self.tree_ticks.delete(item)

        

        self.tickdirecto()

        self.on_parent_configure(None)

    def crear_interfaz_inferior(self):
        # Frame para mostrar los datos
        self.frame_datos = tk.Frame(self.frame_inferior, bg=COLOR_CUERPO_PRINCIPAL, width=399)
        self.frame_datos.pack(side="top", fill=tk.BOTH, expand=True)

        # Crear una sub-frame para las etiquetas
        self.frame_rentabilidades = tk.Frame(self.frame_inferior, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_rentabilidades.pack(side="top", anchor="w", padx=(10, 0), pady=5)

        # Label de "Rentabilidad"
        self.label_rentabilidad = tk.Label(self.frame_datos, text="Rentabilidad", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad.pack(side="left", padx=(10, 0), pady=5)

        # Rentabilidad
        self.rentabilidad_futbol = tk.StringVar()
        self.rentabilidad_futbol.set("0")
        self.label_rentabilidad_futbol = tk.Label(self.frame_datos, textvariable=self.rentabilidad_futbol, font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_futbol.pack(side="left", padx=(0, 10), pady=5)

        # Boton de "Parar Inversión"
        self.boton_parar_inversion = tk.Button(self.frame_datos, text="Parar\ninversión", font=("Aptos", 12), bg="green", fg="white", command=self.parar_inversion) 
        self.boton_parar_inversion.pack(side="right", padx=(0, 10), pady=5)

        # Crear un contenedor para los Treeviews
        self.tree_container = tk.Frame(self.frame_inferior)
        self.tree_container.pack(side="left", fill="both", expand=True)

        # Frame para el primer Treeview
        self.frame_tree = tk.Frame(self.tree_container)
        self.frame_tree.grid(row=0, column=0, sticky="nsew")

        # Frame para el segundo Treeview
        self.frame_tree_ticks = tk.Frame(self.tree_container)
        self.frame_tree_ticks.grid(row=0, column=1, sticky="nsew")

        # Primer Treeview
        self.tree = ttk.Treeview(self.frame_tree)
        self.tree.pack(side="left", fill="both", expand=True)

        # Segundo Treeview
        self.tree_ticks = ttk.Treeview(self.frame_tree_ticks)
        self.tree_ticks.pack(side="right", fill="both", expand=True)

        self.tree_container.grid_rowconfigure(0, weight=1)
        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_columnconfigure(1, weight=1)

    def rentabilidades_comparativas(self): #DAVID aqui necesito la rentabilidad de los indicadores
        inicio_txt=self.fecha_inicio_indicadores
        fin_txt=self.fecha_fin_indicadores
        frecuencia_txt = "Daily"
        #Ibex35 si está seleccionado
        if self.var_ibex35.get():
            if self.label_rentabilidad_ibex35 is not None:
                self.label_rentabilidad_ibex35.destroy()
                self.label_rentabilidad_ibex35 = None
            indicador='IBEX35'
            self.rentIbex35 = self.b.rentabilidadIndicador(frecuencia_txt,inicio_txt,fin_txt,indicador) 
            self.label_rentabilidad_ibex35 = tk.Label(self.frame_rentabilidades, text="Rentabilidad IBEX35: "+str(self.rentIbex35), font=("Aptos", 10), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_rentabilidad_ibex35.pack(side="left", padx=(0, 10), pady=5)
        else:
            if self.label_rentabilidad_ibex35 is not None:
                self.label_rentabilidad_ibex35.destroy()
                self.label_rentabilidad_ibex35 = None
    
        #SP500 si está seleccionado
        if self.var_sp500.get():
            if self.label_rentabilidad_sp500 is not None:
                self.label_rentabilidad_sp500.destroy()
                self.label_rentabilidad_sp500 = None
            indicador='SP500'
            self.rentSP = self.b.rentabilidadIndicador(frecuencia_txt,inicio_txt,fin_txt,indicador) 
            self.label_rentabilidad_sp500 = tk.Label(self.frame_rentabilidades, text="Rentabilidad SP500: "+str(self.rentSP), font=("Aptos", 10), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_rentabilidad_sp500.pack(side="left", padx=(0, 10), pady=5)
        else:
            if self.label_rentabilidad_sp500 is not None:
                self.label_rentabilidad_sp500.destroy()
                self.label_rentabilidad_sp500 = None

        #Plazo fijo si está seleccionado
        if self.var_plazo_fijo.get():
            if self.label_rentabilidad_plazo_fijo is not None:
                self.label_rentabilidad_plazo_fijo.destroy()
                self.label_rentabilidad_plazo_fijo = None
            indicador='Plazo Fijo'
            self.rentPF = self.b.rentabilidadIndicador(frecuencia_txt,inicio_txt,fin_txt,indicador) 
            self.label_rentabilidad_plazo_fijo = tk.Label(self.frame_rentabilidades, text="Rentabilidad Plazo Fijo: "+str(self.rentPF), font=("Aptos", 10), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_rentabilidad_plazo_fijo.pack(side="left", padx=(0, 10), pady=5)
        else:
            if self.label_rentabilidad_plazo_fijo is not None:
                self.label_rentabilidad_plazo_fijo.destroy()
                self.label_rentabilidad_plazo_fijo = None
            
            
   

    def tickdirecto(self):
        cuando_comprar = self.combo_metodos_comprar.get()
        cuando_vender = self.combo_metodos_vender.get()
        accion_txt = self.acronimos_acciones_mt5.get(self.combo_accion.get())
        url_txt = self.url.get(self.combo_equipos.get())
        estrategia = 'Futbol'
        equipo_txt = self.combo_equipos.get()
        frecuencia_txt = "Daily"
        print(equipo_txt, accion_txt, estrategia,url_txt)
        lotaje_txt=self.lotaje_entry.get()
        stoploss_txt=self.stop_loss_entry.get()
        takeprofit_txt=self.take_profit_entry.get()

        if ',' in stoploss_txt:
            stoploss_txt = stoploss_txt.replace(",", ".")
            
        if ',' in takeprofit_txt:
            takeprofit_txt = takeprofit_txt.replace(",", ".")
            
        self.b.establecer_inversion_directo(frecuencia_txt, accion_txt,lotaje_txt,stoploss_txt,takeprofit_txt)#le pasamos el acronimo de MT5 que es donde invierto
        self.fecha_inicio_indicadores=datetime.now().date() #para los sp500, ibex
        
        accion_txt_comparador = self.acronimos_acciones[self.combo_accion.get()]
        self.pais_seleccionado = self.pais[accion_txt_comparador]



        self.b.thread_Futbol(equipo_txt, url_txt, cuando_comprar,cuando_vender)
        self.b.thread_orders_creativas(estrategia)
        self.funciones_recursivas = True#se puedene ejecutar las funciones recursivas
        self.actualiar_partidos()
        self.actualiar_frame()

    def actualiar_partidos(self):
        if(self.funciones_recursivas):
            print("partidos")
            # if(SBS.FRAMEDIRECTO.empty):
            #     self.frame_principal.after(10000, self.actualiar_partidos)#10s
            self.frame_directo=SBS.FRAMEDIRECTO
            print("-------------------FRAME TICKS PARTIDO-------------------")
            print(self.frame_directo)
            self.treeview_partidos()
            self.frame_principal.after(7000, self.actualiar_partidos)
    
    def actualiar_frame(self):
        if(self.funciones_recursivas):
            print("ticks")
            # if(ORD.FRAMETICKS.empty):
            #     self.frame_principal.after(10000, self.actualiar_frame)
            self.frame_ticks=ORD.FRAMETICKS
            print("-------------------FRAME TICKS -------------------")
            print(self.frame_ticks)
            self.treeview_ticks()
            self.frame_principal.after(7000, self.actualiar_frame)

    def treeview_partidos(self):
        self.current_frame =self.frame_directo

        # Configurar las columnas del widget Treeview
        self.tree["columns"] = list(self.current_frame.columns)
        self.tree["show"] = "headings"  # Desactivar la columna adicional
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=50)

        # Limpiar el widget Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Añadir todos los datos del DataFrame al widget Treeview
        for index, row in self.current_frame.iterrows():
            self.tree.insert("", "end", values=tuple(row))

        
    def treeview_ticks(self):
        self.current_frame2 = self.frame_ticks

        # Configurar las columnas del widget Treeview
        self.tree_ticks["columns"] = list(self.current_frame2.columns)
        self.tree_ticks["show"] = "headings"  # Desactivar la columna adicional
        for col in self.tree_ticks["columns"]:
            self.tree_ticks.heading(col, text=col)
            self.tree_ticks.column(col, width=50)

        # Limpiar el widget Treeview
        for row in self.tree_ticks.get_children():
            self.tree_ticks.delete(row)

        # Añadir todos los datos del DataFrame al widget Treeview
        for index, row in self.current_frame2.iterrows():
            self.tree_ticks.insert("", "end", values=tuple(row))

    def parar_inversion(self):

        # Habilitar los ComboBoxs, los Entry y el Botón de "Empezar inversión"
        self.habilitar_botones()
        self.combo_ligas.configure(state="normal")
        self.combo_equipos.configure(state="normal")
        self.combo_accion.configure(state="normal")
        self.combo_metodos_comprar.configure(state="normal")
        self.combo_metodos_vender.configure(state="normal")
        self.stop_loss_entry.configure(state="normal")
        self.take_profit_entry.configure(state="normal")
        self.lotaje_entry.configure(state="normal")
        self.boton_empezar_inversion_futbol.configure(state="normal")
        self.ibex35.configure(state="normal")
        self.sp500.configure(state="normal")
        self.plazo_fijo.configure(state="normal")

        # Boton de "Guardar"
        self.boton_guardar_inversion = tk.Button(self.frame_datos, text="Guardar\ninversión", font=("Aptos", 12), bg="green", fg="white", command=self.guardar_inversion) 
        self.boton_guardar_inversion.pack(side="right", padx=(0, 10), pady=5)
        self.boton_guardar_inversion.configure(state="normal")

        #Parar todos los elementos corriendo
        self.funciones_recursivas=False #paro la ejecucion de las funciones recursivas
        self.b.kill_threads()
        frame_inversiones_finalizadas=self.b.parar_inversion()
        frame_partidos_final=self.b.parar_partidos()
        self.frame_ticks=frame_inversiones_finalizadas
        self.frame_directo=frame_partidos_final
        
        #Calcular la rentabilidad de la comparativa
        self.fecha_fin_indicadores=datetime.now().date()#para los sp500, ibex
        self.rentabilidades_comparativas()
        
        self.establecerRentabilidades()
        
        self.treeview_partidos()
        self.treeview_ticks()
   
    def establecerRentabilidades(self):
        #Rentabilidad Futbol
        rentabilidades = self.frame_ticks[self.frame_ticks['Rentabilidad'] != '-']['Rentabilidad']
        if rentabilidades.empty:
            # Handle the case when 'Rentabilidad' column is not found or has no valid values
            suma_rentabilidades = 0
        else:
            # Continue with your existing logic for processing 'Rentabilidad' values
            suma_rentabilidades = rentabilidades.sum().round(2)
            # Rest of your code here
        
        self.rentabilidad_futbol.set(str(suma_rentabilidades))
        self.label_rentabilidad_futbol.configure(textvariable=self.rentabilidad_futbol)
 


    def limpiar_panel(self,panel):
        # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()

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

        #Ajustas el tamaño de los frames
        self.frame_superior.configure(width=self.frame_width, height=self.frame_height*0.5)
        self.frame_inferior.configure(width=self.frame_width, height=self.frame_height*0.5)

        #Ajustar el tamaño del titulo
        self.label_titulo_futbol.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.2), "bold"))

        #Ajustar info ticks
        if self.label_stop_loss is not None:
            self.label_stop_loss.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.label_take_profit.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.stop_loss_entry.configure(width=int(self.frame_width * 0.02))
            self.take_profit_entry.configure(width=int(self.frame_width * 0.02))
        
        if self.boton_empezar_inversion_futbol is not None:
            self.boton_empezar_inversion_futbol.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_empezar_inversion_futbol.configure(width=int(self.frame_width * 0.015))

        if self.label_rentabilidad is not None:
            self.label_rentabilidad.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.label_rentabilidad_futbol.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.boton_parar_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_parar_inversion.configure(width=int(self.frame_width * 0.015))

        #Ajustar label elegir liga
        if self.label_liga is not None:
            #Ajustar liga
            self.label_liga.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.combo_ligas.configure(width=int(self.frame_width * 0.02))
            
            if self.combo_ligas is not None and self.combo_ligas.get() != "": 
                self.imagen_liga = util_img.leer_imagen(self.imagenes_liga[self.liga], (int(self.frame_width * 0.08), int(self.frame_width * 0.08)))
                self.label_imagen_liga.configure(image=self.imagen_liga)

            #ajustar botones
            if self.boton_parar_inversion is not None:
                self.boton_parar_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
                self.boton_parar_inversion.configure(width=int(self.frame_width * 0.01))

            if self.label_rentabilidad_ibex35 is not None:
                self.label_rentabilidad_ibex35.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            if self.label_rentabilidad_sp500 is not None:
                self.label_rentabilidad_sp500.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            if self.label_rentabilidad_plazo_fijo is not None:
                self.label_rentabilidad_plazo_fijo.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

            #Ajustar equipo
            if self.combo_equipos is not None:
                self.label_equipo.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                self.combo_equipos.configure(width=int(self.frame_width * 0.02))

                if self.combo_equipos.get() != "":
                    self.imagen_equipo = util_img.leer_imagen(self.imagenes_equipos[self.equipo], (int(self.frame_width * 0.08), int(self.frame_width * 0.08)))
                    self.label_imagen_equipo.configure(image=self.imagen_equipo)

                #Ajustar accion
                if self.combo_accion is not None:
                    self.label_accion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                    self.combo_accion.configure(width=int(self.frame_width * 0.02))
                
                    #Ajustar metodo comprar
                    if self.combo_metodos_comprar is not None:
                        self.label_metodo_comprar.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.combo_metodos_comprar.configure(width=int(self.frame_width * 0.02))

                    #Ajustar metodo vender
                    if self.combo_metodos_vender is not None:
                        self.label_metodo_vender.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.combo_metodos_vender.configure(width=int(self.frame_width * 0.02))

                    #Ajustar comparativa
                    if self.label_comparativa is not None:
                        self.label_comparativa.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.ibex35.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.sp500.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.plazo_fijo.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
        

                        #Ajustar lotaje
                        if self.lotaje_entry is not None:
                            self.label_lotaje.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.lotaje_entry.configure(width=int(self.frame_width * 0.02))
                            self.label_inversion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        
                        if self.lotaje_usuario is not None:
                            self.lotaje_usuario.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.lotaje_usuario.configure(width=int(self.frame_width * 0.02))



            


            
