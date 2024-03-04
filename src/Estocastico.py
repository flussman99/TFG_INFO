
from ta.momentum import StochasticOscillator
import tick_reader as tr
import pandas as pd
import MetaTrader5 as mt5
from ta.momentum import RSIIndicator





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
   if CUR_K > CUR_D  and CUR_RSI < 35:
        return True
   return False




def check_sell() -> bool:
   if CUR_K < CUR_D  and CUR_RSI > 65:
        return True
   return False


