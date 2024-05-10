
from ta.momentum import StochasticOscillator
import tick_reader as tr
import pandas as pd
import MetaTrader5 as mt5
from ta.momentum import RSIIndicator
import datetime as dt
import pytz
import time
from datetime import timedelta

TIMEZONE=pytz.timezone("Etc/UTC")

# Global variables
CUR_RSI=None
CUR_K =None
CUR_D =None

TIMEBTWOPERATIONS = timedelta(minutes=15)
compras=[]
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
    tiempo=0


    for index, row in prices_frame.iterrows():
        K = row['%K']
        D=row['%D']
        rsi = row['RSI']

        precioCompra= row['price']
        # Comparar las medias móviles
        if K < D and  rsi > 60 and posicion_abierta == True:
            decisiones.append("Venta")#VENDO
            posicion_abierta=False
            rentabilidad.append(tr.calcular_rentabilidad(compras,row['price']))
            compras.clear()

        elif len(compras) < 10 and K > D and rsi < 35 :
            if tiempo==0 or diftime(row['time'],tiempo):
                decisiones.append("Compra")#COMPRO
                rentabilidad.append(None)
                compras.append(precioCompra)
                posicion_abierta=True
                tiempo=row['time']#tiempo ultima operacion
                print(tiempo)
            else:
                decisiones.append("NO SE REALIZA OPERACION")
                rentabilidad.append(None)    
        else:
            decisiones.append("NO SE REALIZA OPERACION")
            rentabilidad.append(None)

    # Agregar la lista de decisiones como una nueva columna al DataFrame
    prices_frame['Decision'] = decisiones
    prices_frame['Rentabilidad'] = rentabilidad

    print(prices_frame)

    tr.rentabilidad_total( prices_frame['Rentabilidad'])
    tr.frameToExcel(prices_frame,'Estocastico.xlsx')

    return prices_frame



def diftime(t1,t2):
    if t1-t2>TIMEBTWOPERATIONS:
        print("Diferencia de tiempo mayor a 15 minutos")
        print(t1-t2)
        return True
    else:
        return False       
   
def load_ticks_directo(ticks: list, market: str, time_period: int):
    
    # Loading data
     # Loading data
    tick = mt5.symbol_info_tick(market)
    today=pd.to_datetime(tick[0], unit='s')#coje el horario del tick de la accion que haya elegido asi me adapto el horario en funcion del tick y la accion seleccionada
    date_from = today - dt.timedelta(days=17)#esto es lo que hay que camabiar en cada estrategia
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
        if len(ticks) < 16 and tick[0] < second_to_include - time_period:
            # Agregamos el tick a la lista 'ticks'
            ticks.insert(0, [pd.to_datetime(tick[0], unit='s'), tick[2]])#agregamos en forma inversa, quiere decir que el primero que inserto sera el ultimo
            # Actualizamos 'second_to_include' al tiempo del tick actual
            second_to_include = tick[0]
        elif len(ticks) >= 16:
            break

    
    print("\nDisplay TICKS DIRECTO Estocastico")
    prices_frame = pd.DataFrame(ticks, columns=['time', 'price'])
    print(prices_frame)
    



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

           

def check_buy() -> bool:
   if CUR_K > CUR_D  and CUR_RSI < 35:
        return True
   return False




def check_sell() -> bool:
   if CUR_K < CUR_D  and CUR_RSI > 65:
        return True
   return False


