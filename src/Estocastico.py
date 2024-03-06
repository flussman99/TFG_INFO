
from ta.momentum import StochasticOscillator
import tick_reader as tr
import pandas as pd
import MetaTrader5 as mt5
from ta.momentum import RSIIndicator
import datetime as dt
import pytz
import time
TIMEZONE=pytz.timezone("Etc/UTC")





# Global variables
CUR_RSI=None
CUR_K =None
CUR_D =None

MAX_LEN = 9


def backtesting(market: str, prices: list):
   

    prices_frame = pd.DataFrame(prices, columns=['time', 'price'])
    
    stoch = StochasticOscillator(prices_frame['price'], prices_frame['price'], prices_frame['price'], window=14, smooth_window=3)
    rsi= RSIIndicator(prices_frame["price"], window=14, fillna=False)

    stoch_values = stoch.stoch()

    stoch_values_d = stoch_values.rolling(window=3).mean()

    prices_frame['%K'] = stoch_values
    prices_frame['%D'] = stoch_values_d
    prices_frame["RSI"] = rsi.rsi()


    decisiones = []
    rentabilidad=[]
    posicion_abierta=False


    for index, row in prices_frame.iterrows():
        K = row['%K']
        D=row['%D']
        rsi = row['RSI']

        precioCompra= row['price']
        # Comparar las medias móviles
        if K < D and  rsi > 60 and posicion_abierta == True:
            decisiones.append("-1")#VENDO
            posicion_abierta=False
            rentabilidad.append(tr.calcular_rentabilidad(guardar,row['price']))
        elif K > D and rsi < 35 and posicion_abierta == False:
            decisiones.append("1")#COMPRO
            rentabilidad.append(None)
            posicion_abierta=True
            guardar=precioCompra
        else:
            decisiones.append("NO SE REALIZA OPERACION")#COMPRO
            rentabilidad.append(None)

    # Agregar la lista de decisiones como una nueva columna al DataFrame
    prices_frame['Decision'] = decisiones
    prices_frame['Rentabilidad'] = rentabilidad

    print(prices_frame)

    tr.rentabilidad_total( prices_frame['Rentabilidad'])
    tr.frameToExcel(prices_frame,'Estocastico.xlsx')


def thread_estocastico(pill2kill, ticks: list, trading_data: dict):
    """Function executed by a thread that calculates
    the  RSI and MACD and the SIGNAL.

    Args:
        pill2kill (Threading.Event): Event for stopping the thread's execution.
        ticks (list): List with prices.
        indicators (dict): Dictionary where the data is going to be stored.
        trading_data (dict): Dictionary where the data about our bot is stored.
    """
    global CUR_D, CUR_K, CUR_RSI
    
    # Wait if there are not enough elements
    #while len(ticks) < 14 and not pill2kill.wait(1.5):
     #   print("[THREAD - MACD] - Waiting for ticks")
    

    #date_from = dt.datetime.now(tz=TIMEZONE)

    #HABRA QUE HACER USO DE OTRA FUNCION COMO LA DE COPY RANGE, EN LA QUE EL FINAL DE COPIAR LOS TICKS ES ACTUAL, Y 
    # EN FUNCION DEL NUMERO DE TICKS Y EL INTERVALO QUE NOS HAGA FALTA, NOS IREMOS A UN DIA U OTRO

    date_from = dt.datetime(2024, 2, 6, tzinfo=TIMEZONE)

    loaded_ticks=mt5.copy_ticks_from(trading_data['market'],date_from,25,mt5.COPY_TICKS_ALL)

    
    print(loaded_ticks)

    for tick in loaded_ticks:
        ticks.append([pd.to_datetime(tick[0], unit='s'),tick[2]])
    prices_frame = pd.DataFrame(ticks, columns=['time', 'price'])

    # esto es lo que habra que hacer
    # second_to_include = 0
    # for tick in loaded_ticks:
    #     # Every X seconds we add a value to the list
    #     if tick[0] > second_to_include + trading_data['time_period']:
    #         ticks.append([pd.to_datetime(tick[0], unit='s'),tick[2]])
    #         second_to_include = tick[0]
    
    print("\nDisplay RSI THREAD")
    print(prices_frame)
    print("[THREAD - tick_reader] - Taking ticks")
    
    while not pill2kill.wait(1):
        # Every trading_data['time_period'] seconds we add a tick to the list
        tick = mt5.symbol_info_tick(trading_data['market'])#esta funcion tenemos los precios
        # print(tick)
        if tick is not None:
            ticks.append([pd.to_datetime(tick[0], unit='s'),tick[2]])
            print("Nuevo tick añadido:", ticks[-1])
            prices_frame = pd.DataFrame(ticks, columns=['time', 'price'])#refresco el prices_frame
            # print(prices_frame)

            rsi= RSIIndicator(prices_frame["price"], window=14, fillna=False)
            prices_frame["RSI"] = rsi.rsi()
            CUR_RSI=rsi.rsi()

            stoch = StochasticOscillator(prices_frame['price'], prices_frame['price'], prices_frame['price'], window=14, smooth_window=3)
            stoch_values = stoch.stoch()
            stoch_values_d = stoch_values.rolling(window=3).mean()
            prices_frame['%K'] = stoch_values
            prices_frame['%D'] = stoch_values_d

            CUR_K=stoch_values
            CUR_D=stoch_values_d

            print(prices_frame)

        time.sleep(trading_data['time_period'])
        
        
           

def check_buy() -> bool:
   if CUR_K > CUR_D  and CUR_RSI < 35:
        return True
   return False




def check_sell() -> bool:
   if CUR_K < CUR_D  and CUR_RSI > 65:
        return True
   return False


