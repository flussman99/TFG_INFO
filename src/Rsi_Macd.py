

from ta.momentum import RSIIndicator
from ta.trend import MACD
import tick_reader as tr
import pandas as pd
import MetaTrader5 as mt5




# Global variables
MACDs = []
PREV_MACD = None
PREV_SIGNAL = None
CUR_MACD = None
CUR_SIGNAL = None

PREV_EMA9 = None
PREV_EMA12 = None
PREV_EMA26 = None

MAX_LEN = 9


def backtesting(market: str, prices: list):
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
            rentabilidad.append(tr.calcular_rentabilidad(market,guardar,row['price']))
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
    prices_frame['Rentabilidad Estrategia']= rentabilidad

    print(prices_frame)
    excel_filename = 'media.xlsx'
    # Exportar el DataFrame a Excel
    prices_frame.to_excel(excel_filename, index=False)
    

def thread_rsi_macd(pill2kill, ticks: list, time_period: int,indicators: dict, trading_data: dict):
    """Function executed by a thread that calculates
    the  RSI and MACD and the SIGNAL.

    Args:
        pill2kill (Threading.Event): Event for stopping the thread's execution.
        ticks (list): List with prices.
        indicators (dict): Dictionary where the data is going to be stored.
        trading_data (dict): Dictionary where the data about our bot is stored.
    """
    global MACDs, CUR_SIGNAL, CUR_MACD, PREV_SIGNAL, PREV_MACD
    
    # Wait if there are not enough elements
    #while len(ticks) < 14 and not pill2kill.wait(1.5):
     #   print("[THREAD - MACD] - Waiting for ticks")
    loaded_ticks=mt5.copy_ticks_from(trading_data['market'])
     # Filling the list
    second_to_include = 0
    for tick in loaded_ticks:
        # Every X seconds we add a value to the list
        if tick[0] > second_to_include + time_period:
            ticks.append([pd.to_datetime(tick[0], unit='s'),tick[2]])
            second_to_include = tick[0]
#hay que usar javascript para coger los ticks en directo uando queramos revisar las compras
            
            #elegirel periodo que quiere comprobar mi inversor en los ticks lo toco en funcion de lo que elija

    print("[THREAD - MACD] - Loading values")
    # First we need to calculate the previous MACDs and SIGNALs
    i = 26
    while i < len(ticks):
        # Computing the MACD
        PREV_MACD = CUR_MACD
        CUR_MACD = MACD(ticks[:i])
        MACDs.append(CUR_MACD)
        
        i+=1
        
        # Computing the SIGNAL
        if len(MACDs) < 9:
            continue
        else:
            PREV_SIGNAL = CUR_SIGNAL
            CUR_SIGNAL = SIGNAL(MACDs)
        
        if len(MACDs) > 9:
            del MACDs[0]

    # Main thread loop
    print("[THREAD - MACD] - Computing values")
    i = 0
    while not pill2kill.wait(1):
        # Computing the MACD
        PREV_MACD = CUR_MACD
        CUR_MACD = MACD(ticks[-26:])
        
        # Only append a MACD value every time period
        if i >= trading_data['time_period']:
            MACDs.append(CUR_MACD)
            i = 0
        else:
            MACDs[-1] = CUR_MACD
        i+=1
        
        # Computing the SIGNAL
        PREV_SIGNAL = CUR_SIGNAL
        CUR_SIGNAL = SIGNAL(MACDs)
        
        # Updating the dictionary
        indicators['MACD']['MACD'] = CUR_MACD
        indicators['MACD']['SIGNAL'] = CUR_SIGNAL

        if len(MACDs) > 9:
            del MACDs[0]

def check_buy() -> bool:
    """Function to check if the MACD indicator
    allows a buy operation.

    Returns:
        bool: True if it is a buy oportunity, false if not
    """

    
    if CUR_SIGNAL == None or CUR_MACD == None \
        or PREV_SIGNAL == None or PREV_MACD == None:
        return False
    if PREV_SIGNAL >= PREV_MACD:
        if CUR_SIGNAL <= CUR_MACD:
            return True
    return False




def check_sell() -> bool:
    """Function to check if the MACD indicator
    allows a buy operation.

    Returns:
        bool: True if it is a buy oportunity, false if not
    """
    if CUR_SIGNAL == None or CUR_MACD == None \
        or PREV_SIGNAL == None or PREV_MACD == None:
        return False
    if PREV_SIGNAL <= PREV_MACD:
        if CUR_SIGNAL >= CUR_MACD:
            return True
    return False


def K(n):
    """Function for calculating k

    Args:
        n (int): Lenght
    
    Returns:
        float: valor
    """
    return 2/(n+1)


def SMA(ticks):
    """Function that computes the Simple Moving Average.

    Args:
        ticks (list): List with prices.

    Returns:
        float: valor
    """
    return sum(ticks)/len(ticks)


def EMA(ticks: list, n: int):
    """Function that computes the Exponential Moving Average.   

    Args:
        ticks (list): List of prices.
        n (int): Number of values to take into account.
        n can only be 12, 9 or 26.

    Returns:
        float: Value of the EMA
    """
    global PREV_EMA12, PREV_EMA26, PREV_EMA9
    
    if n != 12 and n != 26 and n != 9:
        print("EMA function: N must be 12 or 26 or 9")
    
    # Not enough ticks in the list
    if n > len(ticks): return None
    
    k = K(n)
    
    # Checking if the previous EMA has been calculated
    prev_ema = 0
    if n == 12:
        if PREV_EMA12 is None: 
            prev_ema = SMA(ticks)
        else:
            prev_ema = PREV_EMA12
        ema = (ticks[-1] - prev_ema)*k + prev_ema
        PREV_EMA12 = ema 
    elif n == 26:
        if PREV_EMA26 is None: 
            prev_ema = SMA(ticks)
        else:
            prev_ema = PREV_EMA26
        ema = (ticks[-1] - prev_ema)*k + prev_ema
        PREV_EMA26 = ema 
    else:
        if PREV_EMA9 is None: 
            prev_ema = SMA(ticks)
        else:
            prev_ema = PREV_EMA9
        ema = (ticks[-1] - prev_ema)*k + prev_ema
        PREV_EMA9 = ema 
    
    return ema


# def MACD(ticks):
#     """Function that computes the MACD.

#     Args:
#         ticks (list): List with prices of the ticks

#     Returns:
#         float: Value of the MACD.
#     """
#     return EMA(ticks[-12:], 12) - EMA(ticks[-26:], 26)


def SIGNAL(values_list):
    """Function that computes the SIGNAL.

    Args:
        values_list (list): List with which we have to compute the values.

    Returns:
        float: Value of the SIGNAL.
    """
    return EMA(values_list[-9:], 9)

