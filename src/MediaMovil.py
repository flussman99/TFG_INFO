

from ta.momentum import RSIIndicator
from ta.trend import MACD
import tick_reader as tr
import pandas as pd
import ordenes as ord
import MetaTrader5 as mt5
import datetime as dt
import pytz
import time
TIMEZONE=pytz.timezone("Etc/UTC")





# Global variables
CUR_MED_LP= None
CUR_MED_CP= None


def backtesting(market: str, prices: list):

    # Crear un DataFrame de la lista prices
    prices_frame = pd.DataFrame(prices, columns=['time', 'price'])
    # Puedes ajustar el tamaño de la ventana según tus necesidades
    prices_frame['mediaMovil_CP'] = prices_frame['price'].rolling(window=30).mean()
    prices_frame['mediaMovil_LP'] = prices_frame['price'].rolling(window=60).mean()
     # Lista para almacenar las decisiones
    decisiones = []
    rentabilidad=[]
    posicion_abierta=False

    # Iterar sobre las filas del DataFrame
    for index, row in prices_frame.iterrows():
        media_movil_cp = row['mediaMovil_CP']
        media_movil_lp = row['mediaMovil_LP']
        precioCompra= row['price']
        # Comparar las medias móviles
        if media_movil_cp > media_movil_lp and posicion_abierta == True:
            decisiones.append("-1")#VENDO
            posicion_abierta=False
            rentabilidad.append(tr.calcular_rentabilidad(guardar,row['price']))
        elif media_movil_cp > media_movil_lp and  posicion_abierta == False:
            decisiones.append("NO PA")#VENDO
            rentabilidad.append(None)
        elif media_movil_cp < media_movil_lp and posicion_abierta == False:
            decisiones.append("1")#COMPRO
            rentabilidad.append(None)
            posicion_abierta=True
            guardar=precioCompra
        elif media_movil_cp < media_movil_lp and posicion_abierta == True:
            decisiones.append("POSICION ABIERTA")#COMPRO
            rentabilidad.append(None)
        else:
            decisiones.append("NO HAY MEDIA MOVILES")#COMPRO
            rentabilidad.append(None)

    # Agregar la lista de decisiones como una nueva columna al DataFrame
    prices_frame['Decision'] = decisiones
    prices_frame['Rentabilidad']= rentabilidad

    print(prices_frame)
    
    tr.rentabilidad_total( prices_frame['Rentabilidad'])
    tr.frameToExcel(prices_frame,'MediaMovil.xlsx')



   
def load_ticks_directo(ticks: list, market: str, time_period: int):
    
    # Loading data
    
    timezone = pytz.timezone("Etc/UTC")
    today = dt.datetime.now()#dia de hoy
    date_from = today - dt.timedelta(days=60)#esto es lo que hay que camabiar en cada estrategia
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
        if len(ticks) < 60 and tick[0] < second_to_include - time_period:
            # Agregamos el tick a la lista 'ticks'
            ticks.insert(0, [pd.to_datetime(tick[0], unit='s'), tick[2]])#agregamos en forma inversa, quiere decir que el primero que inserto sera el ultimo
            # Actualizamos 'second_to_include' al tiempo del tick actual
            second_to_include = tick[0]
        elif len(ticks) >= 60:
            break

    
    print("\nDisplay TICKS DIRECTO MediaMovil")
    prices_frame = pd.DataFrame(ticks, columns=['time', 'price'])
    print(prices_frame)
    


def thread_MediaMovil(pill2kill, ticks: list, trading_data: dict):
    """Function executed by a thread that calculates
    the MACD and the SIGNAL.

    Args:
        pill2kill (Threading.Event): Event for stopping the thread's execution.
        ticks (list): List with prices.
        indicators (dict): Dictionary where the data is going to be stored.
        trading_data (dict): Dictionary where the data about our bot is stored.
    """
    global CUR_MED_LP,CUR_MED_CP
    

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

            prices_frame['mediaMovil_CP'] = prices_frame['price'].rolling(window=30).mean()
            prices_frame['mediaMovil_LP'] = prices_frame['price'].rolling(window=60).mean()

            CUR_MED_CP = prices_frame['mediaMovil_CP']
            CUR_MED_LP = prices_frame['mediaMovil_LP']

            print(prices_frame)

def check_buy() -> bool:
    if CUR_MED_LP >= CUR_MED_CP :
        return True
    return False
   
def check_sell() -> bool:
     if CUR_MED_LP <= CUR_MED_CP :
        return True
     return False
