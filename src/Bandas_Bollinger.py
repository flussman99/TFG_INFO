
from ta.volatility import BollingerBands
import tick_reader as tr
import pandas as pd
import MetaTrader5 as mt5
import datetime as dt
import pytz
import time
TIMEZONE=pytz.timezone("Etc/UTC")



# Global variables

BB_LOWER=None
BB_UPPER=None
PRECIO_ACTUAL=None




def backtesting(market: str, prices: list):
    # Crear un DataFrame de la lista prices
    prices_frame = pd.DataFrame(prices, columns=['time', 'price'])
    bb = BollingerBands(prices_frame['price'], window=20, window_dev=2)
    prices_frame['bb_upper'] = bb.bollinger_hband()
    prices_frame['bb_lower'] = bb.bollinger_lband()

    decisiones = []
    rentabilidad=[]
    posicion_abierta=False

    for index, row in prices_frame.iterrows():
        upper = row['bb_upper']
        lower=row['bb_lower']
        precioCompra= row['price']
        # Comparar las medias móviles
        if  upper < precioCompra and posicion_abierta == True:
            decisiones.append("-1")#VENDO
            posicion_abierta=False
            rentabilidad.append(tr.calcular_rentabilidad(guardar,row['price']))
        elif lower > precioCompra and posicion_abierta == False:
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
    tr.frameToExcel(prices_frame,'Bandas.xlsx')


      
   
def load_ticks_directo(ticks: list, market: str, time_period: int):
    
    # Loading data
    
     # Loading data
    tick = mt5.symbol_info_tick(market)
    today=pd.to_datetime(tick[0], unit='s')#coje el horario del tick de la accion que haya elegido asi me adapto el horario en funcion del tick y la accion seleccionada
    date_from = today - dt.timedelta(days=21)#esto es lo que hay que camabiar en cada estrategia
    loaded_ticks = mt5.copy_ticks_range(market, date_from, today, mt5.COPY_TICKS_ALL)
    
    if loaded_ticks is None:
        print("Error loading the ticks")
        return -1

    print(loaded_ticks)

   #limpio ticks por si viene llena
    ticks.clear()
    # Agregamos el primer elemento al comienzo de la lista 'ticks'
    ticks.append([today,tick[2]])
   # Inicializamos 'second_to_include' con el primer elemento de 'loaded_ticks'
    second_to_include = tick[0]#con el timepo

    # Iteramos sobre los elementos de 'loaded_ticks' en orden inverso
    for tick in reversed(loaded_ticks):
        # Si el tiempo del tick actual es menor que el tiempo de 'second_to_include - time_period'
        if len(ticks) < 20 and tick[0] < second_to_include - time_period:
            # Agregamos el tick a la lista 'ticks'
            ticks.insert(0, [pd.to_datetime(tick[0], unit='s'), tick[2]])#agregamos en forma inversa, quiere decir que el primero que inserto sera el ultimo
            # Actualizamos 'second_to_include' al tiempo del tick actual
            second_to_include = tick[0]
        elif len(ticks) >= 20:
            break

    
    print("\nDisplay TICKS DIRECTO Bandas Bollinger")
    prices_frame = pd.DataFrame(ticks, columns=['time', 'price'])
    print(prices_frame)
    



def thread_bandas(pill2kill, ticks: list,trading_data: dict):
    """Function executed by a thread that calculates
    the  RSI and MACD and the SIGNAL.

    Args:
        pill2kill (Threading.Event): Event for stopping the thread's execution.
        ticks (list): List with prices.
        indicators (dict): Dictionary where the data is going to be stored.
        trading_data (dict): Dictionary where the data about our bot is stored.
    """
    global BB_LOWER,BB_UPPER,PRECIO_ACTUAL
    
    

    print("[THREAD - tick_direto] - Working")
    
    load_ticks_directo(ticks, trading_data['market'], trading_data['time_period'])

    print("[THREAD - tick_reader] - Taking ticks")
    
    while not pill2kill.wait(trading_data['time_period']):
        # Every trading_data['time_period'] seconds we add a tick to the list
        tick = mt5.symbol_info_tick(trading_data['market'])#esta funcion tenemos los precios
        # print(tick)
        if tick is not None:
            ticks.append([pd.to_datetime(tick[0], unit='s'),tick[2]])
            print("Nuevo tick añadido:", ticks[-1])
            prices_frame = pd.DataFrame(ticks, columns=['time', 'price'])#refresco el prices_frame
            # print(prices_frame)

            bb = BollingerBands(prices_frame['price'], window=20, window_dev=2)
            prices_frame['bb_upper'] = bb.bollinger_hband()
            prices_frame['bb_lower'] = bb.bollinger_lband()

            PRECIO_ACTUAL= tick[2]
            BB_UPPER = bb.bollinger_hband()
            BB_LOWER =  bb.bollinger_lband()

            print(prices_frame)


def check_buy() -> bool:
   if PRECIO_ACTUAL <  BB_LOWER:
        return True
   return False



def check_sell() -> bool:
    if PRECIO_ACTUAL < BB_UPPER:
        return True
    return False


