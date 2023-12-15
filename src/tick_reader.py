import MetaTrader5 as mt5
import datetime as dt
import pytz
import openpyxl
import pandas as pd
import numpy as np

# Global variables
MAX_TICKS_LEN = 200
MAX_LEN_SPREAD = 20
spread_list = []
TIMEZONE=pytz.timezone("Etc/UTC")

def calcular_rentabilidad(symbol: str,precio_apertura: int,precio_cierre: int):
    """
    Calculate the profitability of a symbol between two dates.

    Args:
        symbol (str): Accion que vamos a observar
        start_date (datetime.datetime): Fecha inicio 
        end_date (datetime.datetime): Fecha cierre 
    Returns:
        float: Profitability percentage.
    """

    if precio_apertura != 0 :

        rentabilidad = ((precio_cierre - precio_apertura) / precio_apertura) * 100
        print(rentabilidad)
        return rentabilidad
    
    

def thread_tick_reader(pill2kill, ticks: list, trading_data: dict, inicio_txt, fin_txt):
    """Function executed by a thread. It fills the list of ticks and
    it also computes the average spread.

    Args:
        pill2kill (Threading.Event): Event to stop the execution of the thread.
        ticks (list): List of ticks to fill.
        trading_data (dict): Trading data needed for loading ticks.
    """
    global spread_list

    print("[THREAD - tick_reader] - Working")

    # Filling the list with previos ticks
    load_ticks(ticks, trading_data['market'], trading_data['time_period'], inicio_txt, fin_txt)
    
    print("[THREAD - tick_reader] - Ticks loaded")
   
    # Filling the list with actual ticks
    print("[THREAD - tick_reader] - Taking ticks")
    i = 1
    while not pill2kill.wait(1):
        
        # Every trading_data['time_period'] seconds we add a tick to the list
        if i % trading_data['time_period'] == 0:
            store_tick(ticks, trading_data['market'])
            i = 0
        
        # Computing the average spread
        spread_list.append(mt5.symbol_info(trading_data['market']).spread)
        if len(spread_list) >= MAX_LEN_SPREAD:
            trading_data['avg_spread'] = sum(spread_list) / len(spread_list)
            del spread_list[0]
                
        # The last tick is going to be changed all the time with the actual one
        ticks[-1] = mt5.symbol_info_tick(trading_data['market']).ask
        i += 1


def load_ticks(ticks: list, market: str, time_period: int, inicio_txt, fin_txt):
    """Function to load into a list, previous ticks.

    Args:
        ticks (list): List where to load ticks.
        market (str): Market from which we have to take ticks.
        time_period (int): Time period in which we want to operate.
        1 minute, 15 minutes... (in seconds)
    """
    # Checking if we are on the weekend (we include the friday),
    # if so, we take ticks from an earlier date.
    today = dt.datetime.utcnow().date()#fecha actual
    if today.weekday() == 0: #lunes
        yesterday = today - dt.timedelta(days=3)
    elif today.weekday() == 6:#domingo
        yesterday = today - dt.timedelta(days=2)
    else:#resto dias dia anterior
        yesterday = today - dt.timedelta(days=1)

    # Loading data
    timezone = pytz.timezone("Etc/UTC")
    fecha_inicio = txt_to_int_fecha(inicio_txt)
    fecha_fin = txt_to_int_fecha(fin_txt)

    utc_from = dt.datetime(fecha_inicio[2], fecha_inicio[1], fecha_inicio[0], tzinfo=timezone)
    utc_to = dt.datetime(fecha_fin[2], fecha_fin[1], fecha_fin[0], tzinfo=timezone)
    #utc_from = datetime.datetime(int(yesterday.year), int(yesterday.month), int(yesterday.day), tzinfo=timezone)
    #loaded_ticks = mt5.copy_ticks_from(market, utc_from, 100000, mt5.COPY_TICKS_ALL)
    loaded_ticks = mt5.copy_ticks_range(market, utc_from, utc_to, mt5.COPY_TICKS_ALL)
    if loaded_ticks is None:
        print("Error loading the ticks")
        return -1

    # create DataFrame out of the obtained data
    ticks_frame = pd.DataFrame(loaded_ticks)
    # convert time in seconds into the datetime format
    ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
        # Nombre del archivo Excel de salida
    excel_filename = 'ticks_data.xlsx'

    # Exportar el DataFrame a Excel
    ticks_frame.to_excel(excel_filename, index=False)

    # display data
    print("\nDisplay dataframe with ticks")
    print(ticks_frame)

    # Filling the list
    second_to_include = 0
    for tick in loaded_ticks:
        # Every X seconds we add a value to the list
        if tick[0] > second_to_include + time_period:
            ticks.append([pd.to_datetime(tick[0], unit='s'),tick[2]])
            second_to_include = tick[0]


    calcular_mediamovil(market,ticks)

    ticks.clear()

    # Removing the ticks that we do not need
    not_needed_ticks = len(ticks) - MAX_TICKS_LEN
    if not_needed_ticks > 0:
        for i in range(not_needed_ticks):
            del ticks[0]




def calcular_mediamovil(market: str, prices: list):

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
            rentabilidad.append(calcular_rentabilidad(market,guardar,row['price']))
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
    excel_filename = 'media.xlsx'
    # Exportar el DataFrame a Excel
    prices_frame.to_excel(excel_filename, index=False)
   # rest of your code


def moving_average_crossover_strategy(prices, short_window, long_window):

    signals = pd.DataFrame(index=prices.index)
    signals['signal'] = 0.0

    # Crear media móvil simple corta
    signals['short_mavg'] = prices.rolling(window=short_window, min_periods=5, center=False).mean()

    # Crear media móvil simple larga
    signals['long_mavg'] = prices.rolling(window=long_window, min_periods=1, center=False).mean()
    # Crear señales de trading
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

    # Generar órdenes de trading
    signals['positions'] = signals['signal'].diff()

    return signals

def store_tick(ticks: list, market: str):#primera forma
    """Function that stores a tick into the given list,
    and also it checks if the list is full to remove a value.

    Args:
        ticks (list): List to be filled
        market (str): Market to be taken
    """
    tick = mt5.symbol_info_tick(market)#esta funcion tenemos los precios
    ticks.append(tick.ask)
    
    # If the list is full (MAX_TICKS_LEN), 
    # we delete the first value
    if len(ticks) >= MAX_TICKS_LEN:
        del ticks[0]

def txt_to_int_fecha(fecha):
    """Function that converts a string date to a int date.

    Args:
        fecha (str): String date to be converted.

    Returns:
        int: Int date.
    """
    fecha = fecha.split("/")
    return int(fecha[2]), int(fecha[1]), int(fecha[0])
