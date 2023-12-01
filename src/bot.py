import threading
import MetaTrader5 as mt5 #Importamos libreria de metatrader le metemos el as para utilizarla con un nombre mas corto
import tick_reader as tr
#importslope_abs_rel, orders
#import MACD, RSI

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
    def __init__(self, lotage: float, time_period: int, market: str):
        """Constructor of the bot. It justs fills the needed informartion for the bot.

        Args:
            lotage (float): Lotage to be used by the bot.
            time_period (int): Time period of the bot, 24h * 3600 (in seconds)
            market (str): Market to operate in.
        """
        self.trading_data['lotage'] = lotage
        self.trading_data['time_period'] = time_period
        self.trading_data['market'] = market
        self.trading_data['avg_spread'] = 0
    
    def get_ticks(self) -> list:
        """Method to get the ticks.

        Returns:
            list: List of ticks
        """
        return self.ticks
    
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
    
    def thread_MACD(self):
        """Function to launch the thread for calculating the MACD.
        """
        #t = threading.Thread(target=MACD.thread_macd, 
         #                    args=(self.pill2kill, self.ticks, self.indicators, self.trading_data))
        #self.threads.append(t)
        #t.start()
        print('Thread - MACD. LAUNCHED')
    
    def thread_RSI(self):
        #t = threading.Thread(target=RSI.thread_RSI, 
        #                     args=(self.pill2kill, self.ticks, self.indicators))
        #self.threads.append(t)
        #t.start()
        print('Thread - RSI. LAUNCHED')
    
    def thread_orders(self):
        #t = threading.Thread(target=orders.thread_orders, 
         #                    args=(self.pill2kill, self.trading_data))
        #self.threads.append(t)
        #t.start()
        print('Thread - orders. LAUNCHED')

    def mt5_login(self,usr:int, passw:str, serv:str) -> bool:
        """Function to initialize the metatrader 5 aplication
        and login wiht our account details.

        Args:
            usr (int): User ID.
            password (str): Password

        Returns:
            bool: True if everything is OK, False if not
        """
        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            return False
        
        authorized=mt5.login(login=usr,password=passw,server=serv)
        if authorized:
            # display trading account data 'as is'
            #print(mt5.account_info())
            # display trading account data in the form of a list
            print("Show account_info()._asdict():")
            account_info_dict = mt5.account_info()._asdict()

            for prop in account_info_dict:
                print("  {}={}".format(prop, account_info_dict[prop]))

        else:
            print("failed to connect at account #{}, error code: {}".format(usr, mt5.last_error()))
            return False

        return True
    
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
        # Function to get the trading data.

        # Initialize an empty list to store the names of the symbols
        trading_data = []

        # Get the list of all available symbols
        symbols = mt5.symbols_get()

        # Add the name of each symbol to the list
        for symbol in symbols:
            trading_data.append(symbol.name)

        return trading_data