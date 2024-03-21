

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


        
   
def load_ticks_directo(ticks: list, market: str, time_period: int):
    
    # Loading data
    
    timezone = pytz.timezone("Etc/UTC")
    today = dt.datetime.now()#dia de hoy
    date_from = today - dt.timedelta(days=35)#esto es lo que hay que camabiar en cada estrategia
    date_from = timezone.localize(date_from)

    # print(today)
    # print(date_from) --> lo hace bien
    
    loaded_ticks = mt5.copy_ticks_range(market, date_from, today, mt5.COPY_TICKS_ALL)
    
    if loaded_ticks is None:
        print("Error loading the ticks")
        return -1

    print(loaded_ticks)

   #limpio ticks por si viene llena
    ticks.clear()

    # Inicializamos 'second_to_include' con el primer elemento de 'loaded_ticks'
    second_to_include = loaded_ticks[-1][0]#con el timepo

    

    # Agregamos el primer elemento al comienzo de la lista 'ticks'
    ticks.append([pd.to_datetime(loaded_ticks[-1][0], unit='s'), loaded_ticks[-1][2]])
    print("primer tick")
    print(ticks[0])

    # Iteramos sobre los elementos de 'loaded_ticks' en orden inverso
    for tick in reversed(loaded_ticks):
        # Si el tiempo del tick actual es menor que el tiempo de 'second_to_include - time_period'
        if len(ticks) < 35 and tick[0] < second_to_include - time_period:
            # Agregamos el tick a la lista 'ticks'
            ticks.insert(0, [pd.to_datetime(tick[0], unit='s'), tick[2]])#agregamos en forma inversa, quiere decir que el primero que inserto sera el ultimo
            # Actualizamos 'second_to_include' al tiempo del tick actual
            second_to_include = tick[0]
        elif len(ticks) >= 35:
            break

    
    print("\nDisplay TICKS DIRECTO RSI")
    prices_frame = pd.DataFrame(ticks, columns=['time', 'price'])
    print(prices_frame)
    


def thread_rsi_macd(pill2kill, ticks: list, trading_data: dict):
    """Function executed by a thread that calculates
    the  RSI and MACD and the SIGNAL.

    Args:
        pill2kill (Threading.Event): Event for stopping the thread's execution.
        ticks (list): List with prices.
        trading_data (dict): Dictionary where the data about our bot is stored.
    """
    global CUR_SIGNAL, CUR_MACD, CUR_RSI



    print("[THREAD - tick_direto] - Working")
    
    load_ticks_directo(ticks, trading_data['market'], trading_data['time_period'])


#CAMBIAR ESTO 
    
    prices_frame = pd.DataFrame(ticks, columns=['time', 'price'])#refresco el prices_frame

    rsi= RSIIndicator(prices_frame["price"], window=14, fillna=False)
    CUR_RSI=rsi.rsi()

    macd = MACD(prices_frame["price"], window_slow=26, window_fast=12, window_sign=9)
    CUR_MACD=macd.macd()
    CUR_SIGNAL=macd.macd_signal()
    
    print("[THREAD - tick_reader] - Taking ticks")
    
    while not pill2kill.wait(trading_data['time_period']):
        # Every trading_data['time_period'] seconds we add a tick to the list
        tick = mt5.symbol_info_tick(trading_data['market'])#esta funcion tenemos los precios
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
              



def check_buy() -> bool:
    """Function to check if the MACD indicator
    allows a buy operation"""

    #Poner variable global el rsi y el macd, hacer comprobacion como en backtesting, y luego la 
    #operacion abierta se comprueba en ordenes.

    if CUR_SIGNAL.iloc[-1] >= CUR_MACD.iloc[-1] and CUR_RSI.iloc[-1] < 35 :
        return True
    return False


def check_sell() -> bool:
    """Function to check if the MACD indicator
    allows a buy operation"""

    if CUR_SIGNAL.iloc[-1] <= CUR_MACD.iloc[-1] and CUR_RSI.iloc[-1] > 65:
        return True
    return False


