import threading
import MetaTrader5 as mt5 #Importamos libreria de metatrader le metemos el as para utilizarla con un nombre mas corto
import tick_reader as tr
import ordenes as orders
#importslope_abs_rel, orders
import Rsi_Macd, MediaMovil,Bandas_Bollinger,Estocastico
import pandas as pd
import os
import queue

class Bot:
    
    # Attributes
    threads = []
    ticks = []
    ticksRSI = []
    ticksMedia = []
    ticksBandas = []
    ticksEstocasticos = []
    pill2kill = threading.Event()
    almacenar_frame_rentabilidad = queue.Queue()
    
    trading_data = {
        "lotage": 1.0,
	    "time_period": 0,
	    "avg_spread": -1,
	    "market": "",
	    "buy_model": None,
	    "sell_Model": None
    }
    
    # Methods
    def __init__(self, lotage: float):
        """Constructor of the bot. It justs fills the needed informartion for the bot.

        Args:
            lotage (float): Lotage to be used by the bot.
        """
        self.trading_data['lotage'] = lotage
        self.trading_data['avg_spread'] = 0

    import os

    def guar_excell(self, nombre_estrategia: str):
        try:
            # Verificar si el archivo Excel existe
            if os.path.isfile(f'{nombre_estrategia}.xlsx'):
                # Leer el archivo Excel existente
                df = pd.read_excel(f'{nombre_estrategia}.xlsx')

                # Guardar una copia del DataFrame en un nuevo archivo Excel con el nombre proporcionado
                df.to_excel(f'{nombre_estrategia}_copia.xlsx', index=False)
                print(f"Copia del archivo Excel generada correctamente como '{nombre_estrategia}_copia.xlsx'.")
            else:
                print(f"No se encontró el archivo '{nombre_estrategia}.xlsx'.")
        except Exception as e:
            print("Error al generar la copia del archivo Excel:", str(e))



    def establecer_frecuencia_accion(self, frecuencia, market: str):
        """
        Args:
            time_period (int): Time period of the bot, 24h * 3600 (in seconds)
            market (str): Market to operate in.
        """
        time_period=self.calcular_frecuencia(frecuencia)
        self.trading_data['time_period'] = time_period
        self.trading_data['market'] = market
    
    def get_ticks(self) -> list:
        """Method to get the ticks.

        Returns:
            list: List of ticks
        """
        return self.ticks
    
    def get_profit(self, inicio_txt, fin_txt):
        tr.txt_to_int_fecha(inicio_txt)
        tr.txt_to_int_fecha(fin_txt)

        # PROBAR AQUI ESTA FUNCION PARA SACAR MARGEN DE BENEFICIO

        # mt5.order_calc_profit(ORDER_TYPE_SELL, self.trading_data['market'], 1, precio_inicio, precio_fin)
        
        # https://www.mql5.com/en/docs/python_metatrader5/mt5ordercalcprofit_py
        

    def thread_tick_reader(self, inicio_txt, fin_txt,estrategia_txt):
        """Function to launch the tick reader thread.
        """
        
        
        t = threading.Thread(target=tr.thread_tick_reader, 
                             args=(self.ticks, self.trading_data, inicio_txt, fin_txt,estrategia_txt,self.almacenar_frame_rentabilidad))
        self.threads.append(t)
        t.start()
        print('Thread - tick_reader. LAUNCHED')

        # Obtener el resultado de la almacenar_frame_rentabilidad
        frame, rentabilidad = self.almacenar_frame_rentabilidad.get()#saca el dato de la cola
        
        return frame, rentabilidad
        
    
    def thread_Futbol(self,inicio_txt, fin_txt,pais_txt,url_txt,estrategia_txt,cuando_comprar,cuando_vender,equipo_txt):
        """Function to launch the tick reader thread.
        """
        tr.thread_Futbol(self.ticks, self.trading_data, inicio_txt, fin_txt,pais_txt,url_txt,estrategia_txt,cuando_comprar,cuando_vender,equipo_txt,self.almacenar_frame_rentabilidad)
        # t = threading.Thread(target=tr.thread_Futbol, 
        #                      args=(self.ticks, self.trading_data, inicio_txt, fin_txt,pais_txt,url_txt,estrategia_txt,cuando_comprar,cuando_vender,equipo_txt,self.almacenar_frame_rentabilidad))
        # self.threads.append(t)
        # t.start()
        print('Thread - tick_reader. LAUNCHED')
        # Obtener el resultado de la almacenar_frame_rentabilidad
        frame, rentabilidad = self.almacenar_frame_rentabilidad.get()#saca el dato de la cola
        
        return frame, rentabilidad
    
    def thread_F1(self, inicio_txt, fin_txt, pais_txt, url_txt, estrategia_txt, cuando_actuar, piloto_txt):
        """Function to launch the tick reader thread.
        """
        tr.thread_F1(self.ticks, self.trading_data, inicio_txt, fin_txt,pais_txt,url_txt,estrategia_txt,cuando_actuar,piloto_txt, self.almacenar_frame_rentabilidad)
        # t = threading.Thread(target=tr.thread_Futbol, 
        #                      args=(self.ticks, self.trading_data, inicio_txt, fin_txt,pais_txt,url_txt,estrategia_txt,cuando_comprar,cuando_vender,equipo_txt,self.almacenar_frame_rentabilidad))
        # self.threads.append(t)
        # t.start()
        print('Thread - tick_reader. LAUNCHED')
        # Obtener el resultado de la almacenar_frame_rentabilidad
        frame, rentabilidad = self.almacenar_frame_rentabilidad.get()#saca el dato de la cola
        
        return frame, rentabilidad

    # def ticks_directo(self , estrategia):
    #     """Function to launch the tick reader thread.
    #     """
    #     t = threading.Thread(target=tr.ticks_directo, 
    #                          args=(self.pill2kill, self.ticks, self.trading_data, estrategia))
    #     self.threads.append(t)
    #     t.start()
    #     print('Thread - tick_reader. LAUNCHED')

    
    def thread_slope_abs_rel(self):
        """Function to launch the thread for calculating the slope
        and, the absolute and relative points in the chart.
        """
        #t = threading.Thread(target=slope_abs_rel.thread_slope_abs_rel, 
                             #args=(self.pill2kill, self.ticks, self.indicators))
        #self.threads.append(t)
        #t.start()
        print('Thread - slope_abs_rel. LAUNCHED')
    

    #Poner threads para cada estrategia 
        
    def thread_RSI_MACD(self):
        """Function to launch the thread for calculating the MACD.
        """
        t = threading.Thread(target=Rsi_Macd.thread_rsi_macd, 
                            args=(self.pill2kill, self.ticksRSI, self.trading_data))
        self.threads.append(t)
        t.start()
        print('Thread - RSI_MACD. LAUNCHED')
        print("Hilos en la lista threads:", self.threads)
    
    def thread_MediaMovil(self):
        """Function to launch the thread for calculating the MACD.
        """
        t = threading.Thread(target=MediaMovil.thread_MediaMovil, 
                            args=(self.pill2kill, self.ticksMedia, self.trading_data))
        self.threads.append(t)
        t.start()
        print('Thread - MediaMovil. LAUNCHED')

    def thread_bandas(self):
        
        t = threading.Thread(target=Bandas_Bollinger.thread_bandas, 
                            args=(self.pill2kill, self.ticksBandas, self.trading_data))
        self.threads.append(t)
        t.start()
        print('Thread - BandasBollinger. LAUNCHED')
        print("Hilos en la lista threads:", self.threads)

    def thread_estocastico(self):
        
        t = threading.Thread(target=Estocastico.thread_estocastico, 
                            args=(self.pill2kill, self.ticksEstocasticos, self.trading_data))
        self.threads.append(t)
        t.start()
        print('Thread - Estocastico. LAUNCHED')    
    
    
    def thread_orders(self,estrategia_directo):
        t = threading.Thread(target=orders.thread_orders, 
                             args=(self.pill2kill, self.trading_data,estrategia_directo))
        self.threads.append(t)
        t.start()
        print('Thread - orders. LAUNCHED')
        print("Hilos en la lista threads:", self.threads)
    
    def kill_threads(self):
        """Function to kill all the loaded threads.
        """
        print('Threads - Stopping threads')
        self.pill2kill.set()
        for thread in self.threads:
            thread.join()
    
    def wait(self):
        """Function to make the thread wait.
        """
        # Input para detener a los hilos
        print('\nPress ENTER to stop the bot\n')
        input()
        self.kill_threads()
        mt5.shutdown()

    def get_trading_data(self):
        # Function to get the .

        # Initialize an empty list to store the names of the symbols
        trading_data = []

        # Get the list of all available symbols
        symbols = mt5.symbols_get()

        exchanges = set(symbol.name.split('.')[1] for symbol in symbols if '.' in symbol.name)
        exchanges_list = list(exchanges)
        exchanges_list.insert(0, 'DIVISES')

        # Add the name of each symbol to the list
        for symbol in symbols:
            trading_data.append(symbol.name)

        return trading_data, exchanges_list
    

    
    
    def calcular_frecuencia(self, frecuencia_txt):
        # Obtener valores de la frecuencia en segundos
        if frecuencia_txt == "1M":
            frecuencia = 60
        elif frecuencia_txt == "3M":
            frecuencia = 180
        elif frecuencia_txt == "5M":
            frecuencia = 300
        elif frecuencia_txt == "10M":
            frecuencia = 600
        elif frecuencia_txt == "15M":
            frecuencia = 900
        elif frecuencia_txt == "30M":
            frecuencia = 1800
        elif frecuencia_txt == "1H":
            frecuencia = 3600
        elif frecuencia_txt == "2H":
            frecuencia = 7200
        elif frecuencia_txt == "4H":
            frecuencia = 14400
        elif frecuencia_txt == "Daily":
            frecuencia = 86400
        elif frecuencia_txt == "Weekly":
            frecuencia = 604800
        elif frecuencia_txt == "Monthly":
            frecuencia = 2592000
        else:
            frecuencia = 0
        return frecuencia
