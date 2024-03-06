

from ta.momentum import RSIIndicator
from ta.trend import MACD
import tick_reader as tr
import pandas as pd
import MetaTrader5 as mt5
import datetime as dt
import pytz
import time
TIMEZONE=pytz.timezone("Etc/UTC")



# Global variables
MACDs = []
CUR_MACD = None
CUR_SIGNAL = None
CUR_RSI = None


MAX_LEN = 9


def backtesting(nombre:str, prices: list):
    # Crear un DataFrame de la lista prices
    prices_frame = pd.DataFrame(prices, columns=['time', 'price'])
    rsi= RSIIndicator(prices_frame["price"], window=14, fillna=False)
    macd = MACD(prices_frame['price'], window_slow=26, window_fast=12, window_sign=9)
    
    prices_frame['macd'] = macd.macd()
    prices_frame['macd_signal'] = macd.macd_signal()
    
    prices_frame["RSI"] = rsi.rsi()
    decisiones = []
    rentabilidad=[]
    posicion_abierta=False

    for index, row in prices_frame.iterrows():
        rsi = row['RSI']
        macd_fila=row['macd']
        macd_si=row['macd_signal']
        precioCompra= row['price']
        # Comparar las medias móviles
        if rsi > 65 and macd_fila < macd_si and posicion_abierta == True:
            decisiones.append("-1")#VENDO
            posicion_abierta=False
            rentabilidad.append(tr.calcular_rentabilidad(guardar,row['price']))
        elif rsi < 35 and macd_fila > macd_si and posicion_abierta == False:
            decisiones.append("1")#COMPRO
            rentabilidad.append(None)
            posicion_abierta=True
            guardar=precioCompra
        else:
            decisiones.append("NO SE REALIZA OPERACION")#COMPRO
            rentabilidad.append(None)

    # Agregar la lista de decisiones como una nueva columna al DataFrame
    prices_frame['Decision'] = decisiones
    prices_frame['Rentabilidad']= rentabilidad

    print(prices_frame)

    tr.rentabilidad_total( prices_frame['Rentabilidad'])
    tr.frameToExcel(prices_frame, nombre + '.xlsx') 


def thread_rsi_macd(pill2kill, ticks: list, trading_data: dict):
    """Function executed by a thread that calculates
    the  RSI and MACD and the SIGNAL.

    Args:
        pill2kill (Threading.Event): Event for stopping the thread's execution.
        ticks (list): List with prices.
        trading_data (dict): Dictionary where the data about our bot is stored.
    """
    global MACDs, CUR_SIGNAL, CUR_MACD, CUR_RSI
    
    # Wait if there are not enough elements
    #while len(ticks) < 14 and not pill2kill.wait(1.5):
     #   print("[THREAD - MACD] - Waiting for ticks")
    #date_from = dt.datetime.now(tz=TIMEZONE)

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

            macd = MACD(prices_frame['price'], window_slow=26, window_fast=12, window_sign=9)
            prices_frame['macd'] = macd.macd()
            prices_frame['macd_signal'] = macd.macd_signal()
            CUR_MACD=macd.macd()
            CUR_SIGNAL=macd.macd_signal()

            print(prices_frame)

        time.sleep(trading_data['time_period'])
        
        
           

def check_buy() -> bool:
    """Function to check if the MACD indicator
    allows a buy operation"""

    #Poner variable global el rsi y el macd, hacer comprobacion como en backtesting, y luego la 
    #operacion abierta se comprueba en ordenes.

    if CUR_SIGNAL >= CUR_MACD and CUR_RSI < 35 :
        return True
    return False


def check_sell() -> bool:
    """Function to check if the MACD indicator
    allows a buy operation"""

    if CUR_SIGNAL <= CUR_MACD and CUR_RSI > 65:
        return True
    return False


