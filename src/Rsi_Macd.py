

from ta.momentum import RSIIndicator
from ta.trend import MACD
import tick_reader as tr
import pandas as pd
import MetaTrader5 as mt5
import datetime as dt
import pytz
from datetime import timedelta



TIMEZONE=pytz.timezone("Etc/UTC")



# Global variables
MACDs = []
CUR_MACD = None
CUR_SIGNAL = None
CUR_RSI = None
# Definir 'TIMEBTWOPERATIONS' como un timedelta que representa 15 minutos
TIMEBTWOPERATIONS = timedelta(minutes=15)
compras=[]
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
    posicion_abierta=False#comprobar si hay alguna posicion abierta para poder realziar ventas
    tiempo=0#tiempo ultima operacion
    
    for index, row in prices_frame.iterrows():
        rsi = row['RSI']
        macd_fila=row['macd']
        macd_si=row['macd_signal']
        precioCompra= row['price']

        # Comparar las medias móviles
        if rsi > 65 and macd_fila < macd_si and posicion_abierta == True:
            decisiones.append("Venta")#VENDO
            posicion_abierta=False
            rentabilidad.append(tr.calcular_rentabilidad(compras,row['price']))
            compras.clear()
        elif len(compras) < 10 and rsi < 35 and macd_fila > macd_si :
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
            decisiones.append("NO SE REALIZA OPERACION")#COMPRO
            rentabilidad.append(None)
    
    compras.clear()
    # Agregar la lista de decisiones como una nueva columna al DataFrame
    prices_frame['Decision'] = decisiones
    prices_frame['Rentabilidad']= rentabilidad

    print("Frame Rsi ",prices_frame)
    return prices_frame

   
def diftime(t1,t2):
    if t1-t2>TIMEBTWOPERATIONS:
        print("Diferencia de tiempo mayor a 15 minutos")
        print(t1-t2)
        return True
    else:
        return False

def load_ticks_directo(ticks: list, market: str, time_period: int):
    selected=mt5.symbol_select(market,True)
    if not selected:
        print("Failed to select EURCAD, error code =",mt5.last_error())
    else: symbol_info=mt5.symbol_info(market)
    print(symbol_info)
    # Loading data
    tick = mt5.symbol_info_tick(market)
    print(tick)
 
    today=pd.to_datetime(tick[0], unit='s')#coje el horario del tick de la accion que haya elegido asi me adapto el horario en funcion del tick y la accion seleccionada
    date_from = today - dt.timedelta(days=35)#esto es lo que hay que camabiar en cada estrategia
    loaded_ticks = mt5.copy_ticks_range(market, date_from, today, mt5.COPY_TICKS_ALL)
    
    if loaded_ticks is None:
        print("Error loading the ticks")
        return -1

    print(loaded_ticks)

   #limpio ticks por si viene llena
    ticks.clear()
    # Agregamos el primer elemento al comienzo de la lista 'ticks'
    ticks.append([today,tick[2]])
    print(ticks[-1])
   # Inicializamos 'second_to_include' con el primer elemento de 'loaded_ticks'
    second_to_include = tick[0]#con el timepo

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
    
    prices_frame = pd.DataFrame(ticks, columns=['time', 'price'])#refresco el prices_frame
  
    rsi= RSIIndicator(prices_frame["price"], window=14, fillna=False)
    CUR_RSI=rsi.rsi()

    macd = MACD(prices_frame["price"], window_slow=26, window_fast=12, window_sign=9)
    CUR_MACD=macd.macd()
    CUR_SIGNAL=macd.macd_signal()
    
    print("[THREAD - tick_reader] - Taking ticks")
    
    tiempoUltimoTick=ticks[-1][0]#Coger el tiempo del ultimo tick

    while not pill2kill.wait(trading_data['time_period']):
        # Every trading_data['time_period'] seconds we add a tick to the list
        tick = mt5.symbol_info_tick(trading_data['market'])#esta funcion tenemos los precios
        
        if tick is not None:
            tiempoactualTick=pd.to_datetime(tick[0], unit='s')
            print(tick)
            if  tiempoactualTick!=tiempoUltimoTick :#comprobacion para que no me meta el mismo tick cuando el mercado esta cerrado 
                
                tiempoUltimoTick=tiempoactualTick#actualizo el tiempo
                
                ticks.append([pd.to_datetime(tick[0], unit='s'),tick[2]])
                print("Nuevo tick añadido:", ticks[-1])
                prices_frame = pd.DataFrame(ticks, columns=['time', 'price'])#refresco el prices_frame
                

                rsi= RSIIndicator(prices_frame["price"], window=14, fillna=False)
                prices_frame["RSI"] = rsi.rsi()
                CUR_RSI=rsi.rsi()

                macd = MACD(prices_frame['price'], window_slow=26, window_fast=12, window_sign=9)
                prices_frame['macd'] = macd.macd()
                prices_frame['macd_signal'] = macd.macd_signal()
                CUR_MACD=macd.macd()
                CUR_SIGNAL=macd.macd_signal()

                print(prices_frame)
            else:
                print("TICK INVALIDO")
              



def check_buy() -> bool:
    """Function to check if the MACD indicator
    allows a buy operation"""

    #Poner variable global el rsi y el macd, hacer comprobacion como en backtesting, y luego la 
    #operacion abierta se comprueba en ordenes.

    if CUR_SIGNAL.iloc[-1] >= CUR_MACD.iloc[-1] and CUR_RSI.iloc[-1] < 35 :
        return True
    return True


def check_sell() -> bool:#ñle tendre que pasar el valor al que la he comprado cada una de las buy
    """Function to check if the MACD indicator
    allows a buy operation"""

    if CUR_SIGNAL.iloc[-1] <= CUR_MACD.iloc[-1] and CUR_RSI.iloc[-1] > 65:
        return True
    return False


