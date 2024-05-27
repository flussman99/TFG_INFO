import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from config2 import COLOR_CUERPO_PRINCIPAL
import util.util_imagenes as util_img
from bot import Bot as bt
import mysql.connector
from configDB import DBConfig
from Formula1 import SF1_backtesting as SF1
from tkcalendar import DateEntry
import tkinter as tk
from datetime import datetime, timedelta
from formularios.formulario_mas_informacion import FormularioBackTestingMasInformacion


class FormularioBackTestingFormula1():

    def __init__(self, panel_principal, id_user):

        self.id_user = id_user
        self.b = bt(1)

        self.frame_width = 0
        self.frame_height = 0

        #Frame principal
        self.frame_principal = tk.Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Frame superior 
        self.frame_superior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL, width=399, height=276)
        self.frame_superior.pack(fill=tk.BOTH)

        #Titulo frame superior
        self.label_titulo_formula1 = tk.Label(self.frame_superior, text="Backtesting Operaciones Fórmula 1", font=("Berlin Sans FB", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="#2d367b")
        self.label_titulo_formula1.place(relx=0.05, rely=0.1)

        # Frame inferior (con scrollbar)
        self.frame_inferior = tk.Frame(self.frame_principal, bg=COLOR_CUERPO_PRINCIPAL, width=399, height=276)
        self.frame_inferior.pack(fill=tk.BOTH)

        #VARIABLES
        #Inicializar Labels
        self.label_ano = None
        self.label_piloto = None
        self.label_accion = None
        self.label_metodo_comprar = None
        self.label_metodo_vender = None
        self.label_comparativa = None
        self.label_rentabilidad = None
        self.label_rentabilidad_futbol = None
        self.label_rentabilidad_comparativa = None
        self.label_rentabilidad_comparativa_dato = None

        self.ibex35 = None
        self.sp500 = None
        self.plazo_fijo = None

        self.label_rentabilidad_ibex35 = None
        self.label_rentabilidad_sp500 = None
        self.label_rentabilidad_plazo_fijo = None

        self.var_ibex35 = None
        self.var_sp500 = None
        self.var_plazo_fijo = None

        #Inicializar ComboBoxs
        self.combo_anos = None
        self.combo_pilotos = None
        self.combo_acciones = None
        self.combo_metodos_comprar = None
        self.combo_metodos_vender = None
        self.combo_comparativa = None


        #Inicializar imagenes
        self.imagen_piloto = None
        self.label_imagen_piloto = None

        #Inicializar variables
        self.label_fecha_inicio = None
        self.label_fecha_fin = None
        self.fecha_inicio_entry = None
        self.fecha_fin_entry = None

        self.fecha_lim = datetime.today()
        self.fecha_ini = datetime.today()

        #Variables SF1
        self.acciones=SF1.acciones_escuderias
        self.standing=SF1.html_standings_files
        self.calendar=SF1.html_calendars_files
        self.pilotosTeams=SF1.html_pilotTeams_files
        self.imagenes_pilotos=SF1.imagenes_pilotos
        self.imagenes_escuderias=SF1.imagenes_escuderias
        self.paisAcciones = SF1.pais_Accion
        self.accionesAPI = SF1.acciones_api
        self.url = 'https://www.f1-fansite.com/f1-results/f1-standings-2024-championship'
        

        #Variables de la tabla
        self.frame_without_filter=None
        self.current_frame = None
        self.frame_with_filter=None
        self.frame_directo=None
        self.tree = None

        #Botones
        self.boton_empezar_backtesting = None
        self.boton_mostrar_operaciones = None
        self.boton_guardar_backtesting = None


        #ComboBoxs
        self.operacion_formula1()

        #esperar 100 milisegundos y llamar a la función on_parent_configure
        panel_principal.after(100, self.on_parent_configure2)   

        #Llamada a la función on_parent_configure cuando se redimensiona la ventana
        panel_principal.bind("<Configure>", self.on_parent_configure)

    def operacion_formula1(self):

        #Crear frame para añadir todo los combo boxs
        self.frame_combo_boxs = tk.Frame(self.frame_superior, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_combo_boxs.place(relx=0.05, rely=0.3)

        #Label de "Elige el año"
        self.label_ano = tk.Label(self.frame_combo_boxs, text="Elige el año", font=("Aptos", 15, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_ano.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        #ComboBox de años
        self.combo_anos = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_anos.grid(row=1, column=0, padx=10, pady=2, sticky="w")

        #Añadir años a la lista
        self.anos = SF1.obtener_listado_años()
        self.combo_anos["values"] = list(self.anos)

        #Al seleccionar un año se actualizan los pilotos
        self.combo_anos.bind("<<ComboboxSelected>>", self.actualizar_formula1_pilotos)
        
        #Actualizar vista al cambiar de accion        
        #self.combo_accion.bind("<<ComboboxSelected>>", self.actualizar_futbol_metodos)

        #Ajustar vista
        self.on_parent_configure(None)

    def actualizar_formula1_pilotos(self, event):

        if self.combo_pilotos is not None:
            self.combo_pilotos.destroy()
            self.label_piloto.destroy()
            if self.label_imagen_piloto is not None:
                self.label_imagen_piloto.destroy()
            if self.label_accion is not None:
                self.label_accion.destroy()
            self.combo_pilotos = None
            self.label_piloto = None
            self.label_imagen_piloto = None
            self.label_accion = None
        
        #Label de "Elige el piloto"
        self.label_piloto = tk.Label(self.frame_combo_boxs, text="Elige el piloto", font=("Aptos", 15, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_piloto.grid(row=0, column=1, padx=10, pady=2, sticky="w")

        #ComboBox de pilotos
        self.combo_pilotos = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
        self.combo_pilotos.grid(row=1, column=1, padx=10, pady=2, sticky="w")

        #Añadir pilotos a la lista
        self.pilotos = SF1.obtener_listado_pilotos(self.combo_anos.get())
        #Ordenar los pilotos alfabeticamente
        self.pilotos.sort()
        self.combo_pilotos["values"] = list(self.pilotos)

        #Al seleccionar un piloto se actualiza la imagen
        self.combo_pilotos.bind("<<ComboboxSelected>>", self.actualizar_formula1_imagen_piloto)

        #Si ya hay una fecha actualizarla
        if self.fecha_fin_entry is not None:
            self.set_dates()

        #Actualizar vista
        self.on_parent_configure(event)


    def actualizar_formula1_imagen_piloto(self, event):
        if self.label_imagen_piloto is not None:
            self.label_imagen_piloto.destroy()
            self.label_imagen_piloto = None
            self.label_accion.destroy()
            self.label_accion = None


        #Coger el piloto seleccionado
        self.piloto = self.combo_pilotos.get()
        #Poner imagen del piloto
        self.imagen_piloto = util_img.leer_imagen(self.imagenes_pilotos[self.piloto], (100,100))
        self.label_imagen_piloto = tk.Label(self.frame_superior, image=self.imagen_piloto, bg=COLOR_CUERPO_PRINCIPAL)
        self.label_imagen_piloto.place(relx=0.8, rely=0.1)

        #Coger el año seleccionado
        self.ano = self.combo_anos.get()
        #Label de accion
        self.accion = SF1.obtener_accion_escuderia(self.piloto, self.ano)
        self.label_accion = tk.Label(self.frame_combo_boxs, text="La acción selecionada es: " + self.accion, font=("Aptos", 15, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_accion.grid(row=2, column=0, columnspan=2, padx=10, pady=2, sticky="w")

        #Si ya hay una fecha actualizarla
        if self.fecha_fin_entry is not None:
            self.set_dates()

        #continuar
        self.actualizar_formula1_metodos(None)



    def actualizar_formula1_metodos(self, event):
        if self.label_metodo_comprar is None:
            #Label de "Elige cuando comprar"
            self.label_metodo_comprar = tk.Label(self.frame_combo_boxs, text="Elige cuando comprar", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_metodo_comprar.grid(row=3, column=0, padx=10, pady=2, sticky="w")

            #ComboBox de metodos comprar
            self.combo_metodos_comprar = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_metodos_comprar.grid(row=4, column=0, padx=10, pady=2, sticky="w")
            self.combo_metodos_comprar["values"] = ["Top 1", "Top 3", "Top 5", "Top 10", "No puntúa"]

            #label de "Elige cuando vender"
            self.label_metodo_vender = tk.Label(self.frame_combo_boxs, text="Elige cuando vender", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_metodo_vender.grid(row=3, column=1, padx=10, pady=2, sticky="w")

            #ComboBox de metodos vender
            self.combo_metodos_vender = ttk.Combobox(self.frame_combo_boxs, state="readonly", width=30)
            self.combo_metodos_vender.grid(row=4, column=1, padx=10, pady=2, sticky="w")
            self.combo_metodos_vender["values"] = ["Top 1", "Top 3", "Top 5", "Top 10", "No puntúa"]

        #Cuando o comprar o vender tenga un valor seleccionado quitar esa opcion del otro
        self.combo_metodos_comprar.bind("<<ComboboxSelected>>", self.actualizar_formula1_metodos_vender)
        self.combo_metodos_vender.bind("<<ComboboxSelected>>", self.actualizar_formula1_metodos_comprar)

        #Ajustar vista
        self.on_parent_configure(event)

    def actualizar_formula1_metodos_comprar(self, event):
        #Coger el metodo de vender seleccionado
        self.metodo_vender = self.combo_metodos_vender.get()
        
        #Quitar la opcion seleccionada en comprar del metodo vender
        if self.metodo_vender == "Top 3":
            self.combo_metodos_comprar["values"] = ["Top 1"]
        elif self.metodo_vender == "Top 5":
            self.combo_metodos_comprar["values"] = ["Top 1", "Top 3"]
        elif self.metodo_vender == "Top 10":
            self.combo_metodos_comprar["values"] = ["Top 1", "Top 3", "Top 5"]
        elif self.metodo_vender == "No puntúa":
            self.combo_metodos_comprar["values"] = ["Top 1", "Top 3", "Top 5", "Top 10"]
                
       
        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.combo_metodos_comprar.get() != "" and self.combo_metodos_vender.get() != "":
            self.actualizar_comparativa()

        #Actualizar vista
        self.on_parent_configure(event)

    def actualizar_formula1_metodos_vender(self, event):
        #Coger el metodo de comprar seleccionado
        self.metodo_comprar = self.combo_metodos_comprar.get()

        #Quitar opciones dependiendo de lo que se eliga en comprar, opciones especiales en cada caso 
        if self.metodo_comprar == "Top 1":
            self.combo_metodos_vender["values"] = ["Top 1", "Top 3", "Top 5", "Top 10", "No puntúa"]
        elif self.metodo_comprar == "Top 3":
            self.combo_metodos_vender["values"] = ["Top 3", "Top 5", "Top 10", "No puntúa"]
        elif self.metodo_comprar == "Top 5":
            self.combo_metodos_vender["values"] = ["Top 5", "Top 10", "No puntúa"]
        elif self.metodo_comprar == "Top 10":
            self.combo_metodos_vender["values"] = ["Top 10", "No puntúa"]
                
        
        #Llamar a demas atributos solo cuando metodo comprar y vender tenga un valor seleccionado
        if self.combo_metodos_comprar.get() != "" and self.combo_metodos_vender.get() != "":
            self.actualizar_comparativa()

        #Actualizar vista
        self.on_parent_configure(event)

    def actualizar_comparativa(self):
        if self.label_comparativa is None:
            
            #Label de "Comparativa"
            self.label_comparativa = tk.Label(self.frame_combo_boxs, text="Comparativa", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
            self.label_comparativa.grid(row=0, column=2, padx=10, pady=2, sticky="w")

            #CheckBox de comparativas
            self.var_ibex35 = tk.BooleanVar()
            self.var_sp500 = tk.BooleanVar()
            self.var_plazo_fijo = tk.BooleanVar()

            self.ibex35 = tk.Checkbutton(self.frame_combo_boxs, text="IBEX35", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_ibex35)
            self.ibex35.grid(row=1, column=2, padx=10, pady=2, sticky="w")
            self.sp500 = tk.Checkbutton(self.frame_combo_boxs, text="SP500", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_sp500)
            self.sp500.grid(row=2, column=2, padx=10, pady=2, sticky="w")
            self.plazo_fijo = tk.Checkbutton(self.frame_combo_boxs, text="Plazo Fijo", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black", variable=self.var_plazo_fijo)
            self.plazo_fijo.grid(row=3, column=2, padx=10, pady=2, sticky="w")

        #al mirar todos los datos actualizar el boton
        self.actualizar_formula1_ticks(None)

        #Ajustar vista
        self.on_parent_configure(None)

    def set_dates(self):
        print ("set_dates")
        print(self.piloto)
        min_year, max_year = SF1.obtener_periodo_valido(self.piloto, self.combo_anos.get())
        self.fecha_lim = min(datetime(max_year, 12, 31), datetime.today())
        self.fecha_ini = datetime(min_year, 1, 1)

        self.fecha_fin_entry.config(maxdate=self.fecha_lim)
        self.fecha_fin_entry.config(mindate=self.fecha_ini)
        self.fecha_fin_entry.set_date(self.fecha_lim)

        self.fecha_inicio_entry.config(maxdate=self.fecha_lim)
        self.fecha_inicio_entry.config(mindate=self.fecha_ini)
        self.fecha_inicio_entry.set_date(self.fecha_ini)
    
    def actualizar_formula1_ticks(self, event):

        if self.fecha_fin_entry is not None:
            self.fecha_fin_entry.destroy()
            self.fecha_fin_entry = None
            self.fecha_inicio_entry.destroy()
            self.fecha_inicio_entry = None
            self.label_fecha_inicio.destroy()
            self.label_fecha_inicio = None
            self.label_fecha_fin.destroy()
            self.label_fecha_fin = None

       
        #Label fecha inicio
        self.label_fecha_inicio = tk.Label(self.frame_combo_boxs, text="Fecha inicio", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_fecha_inicio.grid(row=5, column=0, padx=10, pady=2, sticky="w")

        #label fecha fin
        self.label_fecha_fin = tk.Label(self.frame_combo_boxs, text="Fecha fin", font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_fecha_fin.grid(row=5, column=1, padx=10, pady=2, sticky="w")

        #Date fecha inicio
        fecha_ayer = datetime.now() - timedelta(days = 1)
        self.fecha_inicio_entry = DateEntry(
            self.frame_combo_boxs, 
            date_pattern='yyyy/mm/dd',
            background='darkblue', 
            foreground='white', 
            borderwidth=2,
            maxdate=self.fecha_lim,
            mindate=self.fecha_ini
        )
        self.fecha_inicio_entry.grid(row=6, column=0, padx=10, pady=2, sticky="w")

        #Date fecha fin
        self.fecha_fin_entry = DateEntry(
            self.frame_combo_boxs,
            date_pattern='yyyy/mm/dd',
            background='darkblue',
            foreground='white',
            borderwidth=2,
            maxdate=self.fecha_lim,
            mindate=self.fecha_ini
        )
        self.fecha_fin_entry.grid(row=6, column=1, padx=10, pady=2, sticky="w")

        self.set_dates()

        # Boton de "Empezar backtesting"
        self.boton_empezar_backtesting = tk.Button(self.frame_combo_boxs, text="Empezar\nbacktesting", font=("Aptos", 12), bg="green", fg="white", command=self.empezar_backtesting) # wraplength determina el ancho máximo antes de que el texto se divida en dos líneas
        self.boton_empezar_backtesting.grid(row=5, column=2, rowspan=2, padx=10, pady=2, sticky="w")

        #Ajustar vista
        self.on_parent_configure(None)

    def empezar_backtesting(self):

        # Verificar si la interfaz de usuario ya ha sido creada
        if not hasattr(self, 'frame_datos'):
            # Si no ha sido creada, entonces crearla
            self.crear_interfaz_inferior()
        else:
            # Si ya ha sido creada, limpiar el Treeview
            if self.tree is not None:
                for item in self.tree.get_children():
                    self.tree.delete(item)

        self.rentabilidades_comparativas()

        # Llamar a la función para obtener nuevos datos
        self.coger_ticks()

        #Ajustar vista
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
        self.rentabilidad_f1 = tk.StringVar()
        self.rentabilidad_f1.set("0")
        self.label_rentabilidad_f1 = tk.Label(self.frame_datos, textvariable=self.rentabilidad_f1, font=("Aptos", 15), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.label_rentabilidad_f1.pack(side="left", padx=(0, 10), pady=5)

        # Boton de "Mostrar Operaciones"
        self.boton_mostrar_operaciones = tk.Button(self.frame_datos, text="Mostrar\noperaciones", font=("Aptos", 12), bg="green", fg="white", command=self.toggle_frames) 
        self.boton_mostrar_operaciones.pack(side="right", padx=(0, 10), pady=5)

        # Boton de "Guardar"
        self.boton_guardar_backtesting = tk.Button(self.frame_datos, text="Guardar\nbacktesting", font=("Aptos", 12), bg="green", fg="white", command=self.guardar_backtesting) 
        self.boton_guardar_backtesting.pack(side="right", padx=(0, 10), pady=5)

        #Boton "Más información"
        self.boton_mas_informacion = tk.Button(self.frame_datos, text="Más\ninformación", font=("Aptos", 12), bg="green", fg="white", command=self.mas_informacion)
        self.boton_mas_informacion.pack(side="right", padx=(0, 10), pady=5)

        #Crear un widget Treeview
        self.tree = ttk.Treeview(self.frame_inferior)
        self.tree.pack(side="left", fill="x")



    def rentabilidades_comparativas(self): #DAVID aqui necesito la rentabilidad de los indicadores
        
        inicio_txt = self.fecha_inicio_entry.get()
        fin_txt = self.fecha_fin_entry.get()
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
            

    def toggle_frames(self):
        if self.current_frame.equals(self.frame_without_filter):
            self.current_frame = self.frame_with_filter
        else:
            self.current_frame = self.frame_without_filter
        print("-----------------------------------")
        print(self.current_frame)
        # Limpiar el widget Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Añadir todos los datos del DataFrame al widget Treeview
        for index, row in self.current_frame.iterrows():
            self.tree.insert("", "end", values=tuple(row))


    def obtenerPais(self, accion_txt):
        print(accion_txt)
        mercado = accion_txt.split('.')[1]
        pais = self.paisAcciones.get(mercado)
        print(mercado, pais)
        return pais
    
    def obtenerAccion(self, accion_txt):
        accionApi = self.accionesAPI.get(accion_txt)
        if(accionApi == '' or accionApi is None):
            accionApi = accion_txt
        print(accionApi)
        return accionApi


    def coger_ticks(self):
        
        frecuencia_txt = "Daily"
        inicio_txt = self.fecha_inicio_entry.get()
        fin_txt = self.fecha_fin_entry.get()
        estrategia_txt = 'Formula1'
        piloto_txt = self.piloto
        cuando_comprar = self.combo_metodos_comprar.get()
        cuando_vender = self.combo_metodos_vender.get()
        self.accion = self.obtenerAccion(self.accion)
        pais_txt = self.obtenerPais(self.accion)
        self.accion = self.accion.split('.')[0]
   

        print("----------------------------------------")
        print(frecuencia_txt, self.accion, inicio_txt, fin_txt, estrategia_txt)

        self.b.establecer_frecuencia_accion(frecuencia_txt, self.accion) 
        self.frame_without_filter, rentabilidad = self.b.thread_creativas(inicio_txt,fin_txt,pais_txt,self.url,estrategia_txt, cuando_comprar, cuando_vender, piloto_txt)#pasas un vacio pq no necesitas ese valor sin ambargo en la del futbol si
        
        self.establecerRentabilidades(rentabilidad)
        self.treeview()

    def establecerRentabilidades(self, rentabilidad):
        #Rentabilidad F1
        self.rentabilidad_f1.set(str(rentabilidad))
        self.label_rentabilidad_f1.configure(textvariable=self.rentabilidad_f1)
   

    def treeview(self):

        self.frame_with_filter = self.frame_without_filter[self.frame_without_filter['Decision'].isin(['Compra', 'Venta'])]

        # Set the initial DataFrame to display
        self.current_frame = self.frame_without_filter
        print("-----------------------------------")
        print(self.current_frame)
        # Configurar las columnas del widget Treeview
        self.tree["columns"] = list(self.current_frame.columns)
        self.tree["show"] = "headings"  # Desactivar la columna adicional
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Limpiar el widget Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Añadir todos los datos del DataFrame al widget Treeview
        for index, row in self.current_frame.iterrows():
            self.tree.insert("", "end", values=tuple(row))
    
    def guardar_backtesting(self):
        
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

            # Si llegamos a este punto, el usuario ha introducido un nombre de inversión correcto
            break

        if(nombre_inversión is None):
            return
        
        # Le damos valor al tipo de inversión que esta haciendo el usuario
        tipo = "Backtesting F1"

        # Cogemos la acción en la que ha invertido el usuario
        accion = self.accion

        # Cogemos la fecha de inicio y la de fin de la inversión
        fecha_ini = self.fecha_inicio_entry.get()
        fecha_fin = self.fecha_fin_entry.get()

        # Cogemos cuando toma las decisiones de comprar y vender el usuario
        compra = self.combo_metodos_comprar.get()
        venta = self.combo_metodos_vender.get()

        # Le damos valor a la frecuencia
        frecuencia = "Diaria"

        # Cogemos la rentabilidad de la inversión
        rentabilidad = str(self.rentabilidad_f1.get()) + "%"

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


    def mas_informacion(self):  
        FormularioBackTestingMasInformacion(self.frame_principal, self.frame_without_filter, "Formula1", self.rentabilidad_f1.get())

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
        self.frame_superior.configure(width=self.frame_width, height=self.frame_height*0.6)
        self.frame_inferior.configure(width=self.frame_width, height=self.frame_height*0.4)

        #Ajustar el tamaño del titulo
        self.label_titulo_formula1.configure(font=("Berlin Sans FB",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.2), "bold"))

        #Ajustar el tamaño del boton iniciar backtesting
        if self.boton_empezar_backtesting is not None:
            self.boton_empezar_backtesting.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_empezar_backtesting.configure(width=int(self.frame_width * 0.015))

        #Ajustar el tamaño de los botones
        if self.boton_mostrar_operaciones is not None:
            self.boton_guardar_backtesting.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_mostrar_operaciones.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_mas_informacion.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1), "bold"))
            self.boton_guardar_backtesting.configure(width=int(self.frame_width * 0.015))
            self.boton_mostrar_operaciones.configure(width=int(self.frame_width * 0.015))
            self.boton_mas_informacion.configure(width=int(self.frame_width * 0.015))

        #ajustar el tamaño de las fechas
        if self.fecha_inicio_entry is not None:
            self.label_fecha_inicio.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.label_fecha_fin.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.fecha_inicio_entry.configure(width=int(self.frame_width * 0.02))
            self.fecha_fin_entry.configure(width=int(self.frame_width * 0.02))

        if self.label_rentabilidad_ibex35 is not None:
            self.label_rentabilidad_ibex35.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
        if self.label_rentabilidad_sp500 is not None:
            self.label_rentabilidad_sp500.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
        if self.label_rentabilidad_plazo_fijo is not None:
            self.label_rentabilidad_plazo_fijo.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

        #Ajustar el tamaño de los labels
        if self.label_ano is not None:
            self.label_ano.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
            self.combo_anos.configure(width=int(self.frame_width * 0.02))

            if self.label_piloto is not None:
                self.label_piloto.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                self.combo_pilotos.configure(width=int(self.frame_width * 0.02))

                if self.label_accion is not None:
                    self.label_accion.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                    
                    if self.label_metodo_comprar is not None:
                        self.label_metodo_comprar.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                        self.combo_metodos_comprar.configure(width=int(self.frame_width * 0.02))

                        if self.label_metodo_vender is not None:
                            self.label_metodo_vender.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                            self.combo_metodos_vender.configure(width=int(self.frame_width * 0.02))

                            if self.label_comparativa is not None:
                                self.label_comparativa.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                self.ibex35.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                self.sp500.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                self.plazo_fijo.configure(font=("Aptos",  int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))

                                if self.label_rentabilidad is not None:
                                    self.label_rentabilidad.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
                                    self.label_rentabilidad_f1.configure(font=("Aptos", int(int(min(self.frame_width, self.frame_height) * 0.2)*0.1)))
