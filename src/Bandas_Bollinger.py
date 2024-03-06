
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

MAX_LEN = 9


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

            bb = BollingerBands(prices_frame['price'], window=20, window_dev=2)
            prices_frame['bb_upper'] = bb.bollinger_hband()
            prices_frame['bb_lower'] = bb.bollinger_lband()

            PRECIO_ACTUAL= tick
            BB_UPPER = bb.bollinger_hband()
            BB_LOWER =  bb.bollinger_lband()

            print(prices_frame)

        time.sleep(trading_data['time_period'])

def check_buy() -> bool:
   if PRECIO_ACTUAL <  BB_LOWER:
        return True
   return False



def check_sell() -> bool:
    if PRECIO_ACTUAL < BB_UPPER:
        return True
    return False


