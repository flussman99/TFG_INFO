

from ta.momentum import RSIIndicator
from ta.trend import MACD
import tick_reader as tr
import pandas as pd
import ordenes as ord





# Global variables
CUR_MED_LP= None
CUR_MED_CP= None

MAX_LEN = 9


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


def check_buy() -> bool:
    if CUR_MED_LP >= CUR_MED_CP :
        return True
    return False
   
def check_sell() -> bool:
     if CUR_MED_LP <= CUR_MED_CP :
        return True
     return False

   

def MediaMovil(pill2kill, ticks: list, trading_data: dict):
    """Function executed by a thread that calculates
    the MACD and the SIGNAL.

    Args:
        pill2kill (Threading.Event): Event for stopping the thread's execution.
        ticks (list): List with prices.
        indicators (dict): Dictionary where the data is going to be stored.
        trading_data (dict): Dictionary where the data about our bot is stored.
    """
    global MACDs, CUR_SIGNAL, CUR_MACD, PREV_SIGNAL, PREV_MACD
    #global CUR_MED_LP,CUR_MED_CP
    
    # Wait if there are not enough elements
    while len(ticks) < 35 and not pill2kill.wait(1.5):
        print("[THREAD - MACD] - Waiting for ticks")
    
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