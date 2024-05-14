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
import time
from config import API_KEY 
# import investpy
import requests
from EquiposdeFutbol import SBS_backtesting as SBS
from Formula1 import SF1_backtesting as SF1
from Disney import Dis_backtesting as DIS

# Global variables
MAX_TICKS_LEN = 200
MAX_LEN_SPREAD = 20

spread_list = []
TIMEZONE=pytz.timezone("Etc/UTC")


                            #Funciones de ticks EN BACKTESTING

def thread_tick_reader(ticks: list, trading_data: dict, inicio_txt, fin_txt,estrategia_txt,cola):
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
    
    load_ticks(ticks, trading_data['market'], trading_data['time_period'], inicio_txt, fin_txt)

    frame=estrategias(ticks,estrategia_txt)

    rentabilidad=rentabilidad_total(frame['Rentabilidad'])#genero mi rentabilidad total

    cola.put((frame, rentabilidad))

    print("[THREAD - tick_reader] - Ticks loaded")
    


def estrategias(ticks: list, nombre:str):
    #Escoger estrategia a aplicar
    
    if nombre == 'RSI':
        frame=Rsi_Macd.backtesting(nombre,ticks)
        
    elif nombre == 'Media Movil':
        frame=MediaMovil.backtesting(nombre,ticks)
        
    elif nombre == 'Bandas':
        frame=Bandas_Bollinger.backtesting(nombre,ticks)
        
    elif nombre == 'Estocastico':
        frame=Estocastico.backtesting(nombre,ticks)
    
    frameToExcel(frame, f'{nombre}.xlsx')
    ticks.clear()       
    return frame


def thread_creativas(ticks: list, trading_data: dict, inicio_txt, fin_txt,pais_txt,url_txt,estrategia_txt,cuando_comprar_actuar,cuando_vender_vacio,equipos_pilotos_txt,cola):
    """Function executed by a thread. It fills the list of ticks and
    it also computes the average spread.

    Args:
        pill2kill (Threading.Event): Event to stop the execution of the thread.
        ticks (list): List of ticks to fill.
        trading_data (dict): Trading data needed for loading ticks.
    """
   
    print("[THREAD - tick_futbol] - Working")

    load_ticks_invest(ticks,trading_data['market'], trading_data['time_period'], inicio_txt, fin_txt, pais_txt)
    # Filling the list with previos ticks
    frame = estrategias_Creativas(ticks,estrategia_txt,inicio_txt, fin_txt,url_txt,cuando_comprar_actuar,cuando_vender_vacio,equipos_pilotos_txt)
    rentabilidad=rentabilidad_total(frame['Rentabilidad'])#genero mi rentabilidad total
    cola.put((frame, rentabilidad))
    print("[THREAD - tick_reader] - Ticks loaded")

def rentabilidadIndicador(time_period,inicio,fin,indicador):
    if(indicador == 'IBEX35'):
        return load_IBEX35(time_period, inicio, fin)
    elif(indicador == 'SP500'):
        return load_SP500(time_period, inicio, fin)
    elif(indicador == 'Plazo Fijo'):
        return calcular_rentabilidad_plazo_fijo(inicio,fin)

def estrategias_Creativas(ticks: list,nombre:str,inicio_txt, fin_txt,url,cuando_comprar_actuar,cuando_vender_vacio,equipos_pilotos_txt):
    if nombre == 'Futbol':
        frame=SBS.backtesting(ticks, inicio_txt, fin_txt,url,cuando_comprar_actuar,cuando_vender_vacio,equipos_pilotos_txt)
    elif nombre == 'Formula1':
        frame=SF1.backtesting(ticks, inicio_txt, fin_txt, url, cuando_comprar_actuar, cuando_vender_vacio, equipos_pilotos_txt)
    elif nombre == 'Disney':
        frame=DIS.backtesting(nombre,ticks, inicio_txt, fin_txt, url, cuando_comprar_actuar, equipos_pilotos_txt)

    frameToExcel(frame, f'{nombre}.xlsx')
    ticks.clear()       
    return frame




def load_IBEX35(time_period, inicio_txt, fin_txt):
    print(time_period, inicio_txt, fin_txt)

    url = "https://api.scraperlink.com/investpy/"
    params = {
        "email": "tfginfotrading@gmail.com",
        "type": "historical_data",
        "product": "indices",
        "symbol": "IBEX",
        "from_date": inicio_txt,
        "to_date": fin_txt,
        "time_frame": time_period        
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['data'] is None:
            print("The 'data' field is null.")
            # Handle the null case here, e.g., return a default value or perform any other desired action
            return 0
        loaded_ticks = pd.DataFrame(data['data'])
        loaded_ticks = loaded_ticks.rename(columns={'last_close': 'price', 'rowDateRaw': 'time'})
        loaded_ticks['time'] = pd.to_datetime(loaded_ticks['time'], unit='s')
        prices_frame = loaded_ticks[['price', 'time']]
        precio_cierre = prices_frame.iloc[0] 
        precio_apertura = prices_frame.iloc[-1]
        print(precio_apertura['price'])
        print(precio_cierre['price'])

        precio_cierre = float(precio_cierre['price'].replace(',', ''))
        precio_apertura = float(precio_apertura['price'].replace(',', ''))
        
        rentabilidad_IBEX = calcularIBEX35(precio_cierre, precio_apertura)
        # Convertir el DataFrame a una lista de diccionarios y añadirlo a la lista 'ticks'

    return rentabilidad_IBEX

        
def calcularIBEX35(precio_cierre,precio_apertura):
    rentabilidad=((precio_cierre-precio_apertura)/precio_apertura)*100              
    return round(rentabilidad,2)


def load_SP500(time_period, inicio_txt, fin_txt):
    print(time_period, inicio_txt, fin_txt)

    url = "https://api.scraperlink.com/investpy/"
    params = {
        "email": "tfginfotrading@gmail.com",
        "type": "historical_data",
        "product": "indices",
        "symbol": "SPX",
        "from_date": inicio_txt,
        "to_date": fin_txt,
        "time_frame": time_period        
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, params=params, headers=headers)
    print(response)
    if response.status_code == 200:
        data = response.json()
        if data['data'] is None:
            print("The 'data' field is null.")
            # Handle the null case here, e.g., return a default value or perform any other desired action
            return 0
        loaded_ticks = pd.DataFrame(data['data'])
        loaded_ticks = loaded_ticks.rename(columns={'last_close': 'price', 'rowDateRaw': 'time'})
        loaded_ticks['time'] = pd.to_datetime(loaded_ticks['time'], unit='s')
        prices_frame = loaded_ticks[['price', 'time']]
        precio_cierre = prices_frame.iloc[0] 
        precio_apertura = prices_frame.iloc[-1]
        print(precio_apertura['price'])
        print(precio_cierre['price'])

        precio_cierre = float(precio_cierre['price'].replace(',', ''))
        precio_apertura = float(precio_apertura['price'].replace(',', ''))
        
        rentabilidad_SP = calcularSP(precio_cierre, precio_apertura)
        # Convertir el DataFrame a una lista de diccionarios y añadirlo a la lista 'ticks'

    return rentabilidad_SP

def calcularSP(precio_cierre,precio_apertura):
    rentabilidad=((precio_cierre-precio_apertura)/precio_apertura)*100              
    return round(rentabilidad,2)

def calcular_rentabilidad_plazo_fijo(fecha_inicio, fecha_final):
   
    print(fecha_final,fecha_inicio)
    # Calcular la cantidad de días entre las dos fechas

    fecha_inicio = dt.datetime.strptime(fecha_inicio, '%Y/%m/%d')
    fecha_final = dt.datetime.strptime(fecha_final, '%Y/%m/%d')
    dias = (fecha_final - fecha_inicio).days
    
    # Calcular la rentabilidad utilizando la misma fórmula
    rentabilidad = (3 / 100 / 365) * dias
    return round(rentabilidad,2)*100



def load_ticks_invest(ticks: list, market: str, time_period ,inicio_txt, fin_txt, pais_txt):

    print(market, time_period, inicio_txt, fin_txt, pais_txt)

    url = "https://api.scraperlink.com/investpy/"
    params = {
    "email": "tfginfotrading@gmail.com",
    "type": "historical_data",
    "product": "stocks",
    "country": pais_txt,
    "symbol": market,
    "from_date": inicio_txt,
    "to_date": fin_txt,
    "time_frame": time_period        
    }
    headers = {
    "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        loaded_ticks = pd.DataFrame(data['data'])
        loaded_ticks = loaded_ticks.iloc[::-1]
        loaded_ticks = loaded_ticks.reset_index(drop=True)
        loaded_ticks = loaded_ticks.rename(columns={'last_close': 'price', 'rowDateRaw': 'time'})
        loaded_ticks['time'] = pd.to_datetime(loaded_ticks['time'], unit='s')
        prices_frame = loaded_ticks[['price', 'time']]
        print(prices_frame)
        # Convertir el DataFrame a una lista de diccionarios y añadirlo a la lista 'ticks'
        ticks.extend(prices_frame.to_dict('records'))


def load_ticks(ticks: list, market: str, time_period: int, inicio_txt, fin_txt):
# Loading data
    timezone = pytz.timezone("Etc/UTC")
    fecha_inicio = txt_to_int_fecha(inicio_txt)
    fecha_fin = txt_to_int_fecha(fin_txt)

    utc_from = dt.datetime(fecha_inicio[2], fecha_inicio[1], fecha_inicio[0], tzinfo=timezone)
    print(utc_from)
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
    # print("\nDisplay dataframe with ticks")
    # print(ticks_frame)

    # Añadiendo a la lista que muestro en el excell solo time y price--> tick[2] -->ask 
    second_to_include = 0
    for tick in loaded_ticks:
        # Every X seconds we add a value to the list
        if tick[0] > second_to_include + time_period:
            ticks.append([pd.to_datetime(tick[0], unit='s'),tick[2]])
            second_to_include = tick[0] 
    print("\nDisplay dataframe with ticks tratados")
    final_frame=pd.DataFrame(ticks)

    print(final_frame)
    # # Removing the ticks that we do not need
    # not_needed_ticks = len(ticks) - MAX_TICKS_LEN
    # if not_needed_ticks > 0:
    #     for i in range(not_needed_ticks):
    #         del ticks[0]
   

def calcular_rentabilidad(precios_apertura: list, precio_cierre: int):
    """
    Calcular rentabilidad total
    """
    rentabilidad_total = 0
    
    for precio_apertura in precios_apertura:
        if precio_apertura != 0:
            rentabilidad = ((precio_cierre - precio_apertura) / precio_apertura) * 100
            # print("Rentabilidad obtenida")
            # print(rentabilidad)
            rentabilidad_total += rentabilidad
            
    rentabilidad_total = rentabilidad_total/len(precios_apertura)
    print("Rentabilidad total obtenida")
    print(rentabilidad_total)
    return rentabilidad_total


def rentabilidad_total(rentabilidades):
     # Mostrar la rentabilidad total
    suma_rentabilidades = rentabilidades.sum()
    print("La suma de rentabilidades es:", suma_rentabilidades)
    return round(suma_rentabilidades,2)

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




