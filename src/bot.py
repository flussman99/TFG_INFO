import threading
import MetaTrader5 as mt5 #Importamos libreria de metatrader le metemos el as para utilizarla con un nombre mas corto
import tick_reader as tr
import ordenes as orders
#importslope_abs_rel, orders
import Rsi_Macd, MediaMovil

class Bot:
    
    # Attributes
    threads = []
    ticks = []
    pill2kill = threading.Event()
    
    trading_data = {
        "lotage": 0.0,
	    "time_period": 0,
	    "avg_spread": -1,
	    "market": "",
	    "buy_model": None,
	    "sell_Model": None
    }

    indicators = {
        "MACD": {"MACD": 0.0, "SIGNAL": 0.0},
        "RSI": 0.0,
        "slope": 0.0,
        "absolute_max": {"time": 0.0, "difference": 0.0},
        "absolute_min": {"time": 0.0, "difference": 0.0},
        "relative_min": {"time": 0.0, "difference": 0.0},
        "relative_max": {"time": 0.0, "difference": 0.0}
    }
    
    # Methods
    def __init__(self, lotage: float):
        """Constructor of the bot. It justs fills the needed informartion for the bot.

        Args:
            lotage (float): Lotage to be used by the bot.
        """
        self.trading_data['lotage'] = lotage
        self.trading_data['avg_spread'] = 0

    def set_info(self, time_period: int, market: str):
        """
        Args:
            time_period (int): Time period of the bot, 24h * 3600 (in seconds)
            market (str): Market to operate in.
        """
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
        

    def thread_tick_reader(self, inicio_txt, fin_txt):
        """Function to launch the tick reader thread.
        """
        t = threading.Thread(target=tr.thread_tick_reader, 
                             args=(self.pill2kill, self.ticks, self.trading_data, inicio_txt, fin_txt))
        self.threads.append(t)
        t.start()
        print('Thread - tick_reader. LAUNCHED')
    
    def thread_slope_abs_rel(self):
        """Function to launch the thread for calculating the slope
        and, the absolute and relative points in the chart.
        """
        #t = threading.Thread(target=slope_abs_rel.thread_slope_abs_rel, 
                             #args=(self.pill2kill, self.ticks, self.indicators))
        #self.threads.append(t)
        #t.start()
        print('Thread - slope_abs_rel. LAUNCHED')
    
    def thread_RSI_MACD(self):
        """Function to launch the thread for calculating the MACD.
        """
        t = threading.Thread(target=Rsi_Macd.thread_rsi_macd, 
                            args=(self.pill2kill, self.ticks, self.indicators, self.trading_data))
        self.threads.append(t)
        t.start()
        print('Thread - RSI_MACD. LAUNCHED')
    
    def thread_MediaMovil(self):
        """Function to launch the thread for calculating the MACD.
        """
        t = threading.Thread(target=MediaMovil.MediaMovil, 
                            args=(self.pill2kill, self.ticks, self.indicators, self.trading_data))
        self.threads.append(t)
        t.start()
        print('Thread - MediaMovil. LAUNCHED')
    
    def thread_orders(self):
        t = threading.Thread(target=orders.thread_orders, 
                             args=(self.pill2kill, self.trading_data))
        self.threads.append(t)
        t.start()
        print('Thread - orders. LAUNCHED')
    
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