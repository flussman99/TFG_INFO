import MetaTrader5 as mt5
import datetime as dt
import ordenes as orden
import Rsi_Macd 
import MediaMovil 
import Bandas_Bollinger
import Estocastico
import pytz
import openpyxl
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.momentum import StochRSIIndicator
from ta.trend import MACD

# Global variables
MAX_TICKS_LEN = 200
MAX_LEN_SPREAD = 20
spread_list = []
TIMEZONE=pytz.timezone("Etc/UTC")


                            #Funciones estaticas de ticks

def thread_tick_reader(ticks: list, trading_data: dict, inicio_txt, fin_txt,estrategia_txt):
    """Function executed by a thread. It fills the list of ticks and
    it also computes the average spread.

    Args:
        pill2kill (Threading.Event): Event to stop the execution of the thread.
        ticks (list): List of ticks to fill.
        trading_data (dict): Trading data needed for loading ticks.
    """
    # global spread_list
    print("Show symbol_info")
    symbol_info_dict = mt5.symbol_info(trading_data['market'])._asdict()
    for prop in symbol_info_dict:
        print("  {}={}".format(prop, symbol_info_dict[prop]))

    print("[THREAD - tick_reader] - Working")

    # Filling the list with previos ticks
    load_ticks(ticks, trading_data['market'], trading_data['time_period'], inicio_txt, fin_txt)
 
    estrategias(ticks,trading_data['market'],estrategia_txt)
    
    print("[THREAD - tick_reader] - Ticks loaded")
   
    
def load_ticks(ticks: list, market: str, time_period: int, inicio_txt, fin_txt):
    
    # Loading data
    timezone = pytz.timezone("Etc/UTC")
    fecha_inicio = txt_to_int_fecha(inicio_txt)
    fecha_fin = txt_to_int_fecha(fin_txt)

    utc_from = dt.datetime(fecha_inicio[2], fecha_inicio[1], fecha_inicio[0], tzinfo=timezone)
    utc_to = dt.datetime(fecha_fin[2], fecha_fin[1], fecha_fin[0], tzinfo=timezone)
    loaded_ticks = mt5.copy_ticks_range(market, utc_from, utc_to, mt5.COPY_TICKS_ALL)
    if loaded_ticks is None:
        print("Error loading the ticks")
        return -1

    # create DataFrame out of the obtained data
    ticks_frame = pd.DataFrame(loaded_ticks)
    # convert time in seconds into the datetime format
    ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')

    # mostrar todos los ticks con todas las columnas
    print("\nDisplay dataframe with ticks")
    print(ticks_frame)

    # Añadiendo a la lista que muestro en el excell solo time y price--> tick[2] -->ask 
    second_to_include = 0
    for tick in loaded_ticks:
        # Every X seconds we add a value to the list
        if tick[0] > second_to_include + time_period:
            ticks.append([pd.to_datetime(tick[0], unit='s'),tick[2]])
            second_to_include = tick[0] 

    # # Removing the ticks that we do not need
    # not_needed_ticks = len(ticks) - MAX_TICKS_LEN
    # if not_needed_ticks > 0:
    #     for i in range(not_needed_ticks):
    #         del ticks[0]



                            #Funciones DINMICAS de ticks


def ticks_directo(pill2kill, ticks: list, trading_data: dict):#primera forma

    # Coger tcks en directo
    print("[THREAD - tick_reader] - Taking ticks")
    i = 1
    tick = mt5.symbol_info_tick(trading_data['market'])#esta funcion tenemos los precios

    while not pill2kill.wait(1):
        # Every trading_data['time_period'] seconds we add a tick to the list
        if i % trading_data['time_period'] == 0:
            ticks.append([pd.to_datetime(tick[0], unit='s'),tick[2]])
            print("Nuevo tick añadido:", ticks[-1])
        
        # # Computing the average spread
        # spread_list.append(mt5.symbol_info(trading_data['market']).spread)
        # if len(spread_list) >= MAX_LEN_SPREAD:
        #     trading_data['avg_spread'] = sum(spread_list) / len(spread_list)
        #     del spread_list[0]
                
        # The last tick is going to be changed all the time with the actual one
        # ticks[-1] = mt5.symbol_info_tick(trading_data['market']).ask
        i += 1
   
    # If the list is full (MAX_TICKS_LEN), 
    # we delete the first value
    # if len(ticks) >= MAX_TICKS_LEN:
    #     del ticks[0]




                                    #FUNCIONES DE APOYO
        

def estrategias(ticks: list, market: str,nombre:str):
    #Escoger estrategia a aplicar
    if nombre == 'RSI':
        Rsi_Macd.backtesting(nombre,ticks)
        ticks.clear()
    elif nombre == 'Media Movil':
        MediaMovil.backtesting(nombre,ticks)
        ticks.clear()
    elif nombre == 'Bandas':
        Bandas_Bollinger.backtesting(nombre,ticks)
        ticks.clear()
    elif nombre == 'Estocastico':
        Estocastico.backtesting(nombre,ticks)
        ticks.clear()
    
    



def calcular_rentabilidad(precio_apertura: int,precio_cierre: int):
    """
    Calcular rentabilidad
    """
    if precio_apertura != 0 :

        rentabilidad = ((precio_cierre - precio_apertura) / precio_apertura) * 100
        print("Rentabilidad obtenida")
        print(rentabilidad)
        return rentabilidad
    
def rentabilidad_total(rentabilidades):
     # Mostrar la rentabilidad total
    suma_rentabilidades = rentabilidades.sum()
    print("La suma de rentabilidades es:", suma_rentabilidades)

def frameToExcel(prices_frame, excel_filename):
    """
    Exporta un DataFrame a un archivo Excel."""

    try:
        # Exportar el DataFrame a Excel
        prices_frame.to_excel(excel_filename, index=False)
        print(f"DataFrame exportado correctamente a '{excel_filename}'.")
    except Exception as e:
        print("Error al exportar el DataFrame a Excel:", str(e))

def txt_to_int_fecha(fecha):
    """Function that converts a string date to a int date.

    Args:
        fecha (str): String date to be converted.

    Returns:
        int: Int date.
    """
    fecha = fecha.split("/")
    return int(fecha[2]), int(fecha[1]), int(fecha[0])







                                    #Funciones que no se usan


# def moving_average_crossover_strategy(prices, short_window, long_window):

#     signals = pd.DataFrame(index=prices.index)
#     signals['signal'] = 0.0

#     # Crear media móvil simple corta
#     signals['short_mavg'] = prices.rolling(window=short_window, min_periods=5, center=False).mean()

#     # Crear media móvil simple larga
#     signals['long_mavg'] = prices.rolling(window=long_window, min_periods=1, center=False).mean()
#     # Crear señales de trading
#     signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

#     # Generar órdenes de trading
#     signals['positions'] = signals['signal'].diff()

#     return signals