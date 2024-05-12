import threading
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import numpy as np
from typing import Tuple
import tick_reader as tr

data = []
compras = []

estudios_Disney = [
    'Star Distribution',
    'Star Studios',
    'Buena Vista International',
    '20th Century Studios',
    '20th Century Fox',
    'Fox Star Studios',
    'Touchstone Pictures',
    'Stone Circle Pictures',
    'Walt Disney Pictures',
    'Pixar Animation Studios',
    'Jerry Bruckheimer Films',
    'Miramax Films',
    'Disneynature',
    'Walt Disney Animation Studios',
    'DreamWorks Pictures',
    'Marvel Studios',
    'Tim Burton Productions',
    'Disneytoon Studios',
    'Ruby Films',
    'Roth Films',
    'Lucamar Productions and Marc Platt Productions',
    'Mayhem Pictures',
    'Kinberg Genre',
    'Lucasfilm',
    'Fairview Entertainment',
    'Amblin Entertainment',
    'Whitaker Entertainment',
    'The Mark Gordon Company',
    'Silverback Films',
    'Fox Searchlight Pictures',
    'Regency Enterprises',
    'Others'
]

html_movies_files = [
    'Disney_2010_2019.html',
    'Disney_Animation_2010_2019.html',
    'Disney_2020_2029.html',
    'Disney_Animation_2020_2029.html'
]

def get_movie_ratings(movie_titles):
    api_key = 'c8a6e89190cb7be8e6b92a4c8d032df3'
    ratings = []

    for title in movie_titles:
        if title is not None:  # Verificar si el título no es None
            formatted_title = '+'.join(title.split())
            print(formatted_title)
            url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={formatted_title}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['total_results'] > 0:
                    movie_id = data['results'][0]['id']
                    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
                    response = requests.get(url)
                    if response.status_code == 200:
                        movie_data = response.json()
                        rating = movie_data['vote_average']
                        ratings.append(rating)
                    else:
                        ratings.append(None)
                else:
                    ratings.append(None)
            else:
                ratings.append(None)
        else:
            ratings.append(None)
    
    return ratings
 
def backtesting(nombre:str, prices: list, inicio: str, fin: str, url, combo_rating: float, studio: str):
    # Crear un DataFrame de la lista prices
    ticks_frame = pd.DataFrame(prices, columns=['time', 'price'])

    ticks_frame.to_excel('tick.xlsx', index=False)
    
    decisiones = []
    rentabilidad = []
    posicion_abierta=False

    peliculas_frame=datosPeliculas(url, studio)
    #peliculas_frame['Release Date'] = pd.to_datetime(peliculas_frame['Release Date'])

    # Initialize a new column 'precio' in peliculas_frame with NaN values
    peliculas_frame = peliculas_frame[peliculas_frame['Release Date'].between(inicio, fin)]
    peliculas_frame['Precio'] = np.nan
    # Iterate over the rows in peliculas_frame
    
    for i, row in peliculas_frame.iterrows(): 
        rating = row['Rating']


        # Find the corresponding price in ticks_frame
        price = ticks_frame.loc[ticks_frame['time'] >= row['Release Date'], 'price'].first_valid_index()

        if price is not None:
            # If a price was found, update the 'precio' column in peliculas_frame
            peliculas_frame.at[i, 'Precio'] = float(ticks_frame.loc[price, 'price'])
        # if rating[0] == 'DNF' or rating[0] == 'DNS' or rating[0] == 'No participo' or rating[0] == ' ' or rating[0] == 'N':
        #     rating = 30
        # elif '*' in rating[0]:
        #     # Eliminar el asterisco si está presente
        #     rating = int(rating[0].replace('*', ''))
        # else:
        #     rating = int(rating[0])

        precioCompra = peliculas_frame.at[i, 'Precio']
            
        if rating >= combo_rating and len(compras) < 10:
            decisiones.append("Compra")#COMPRO
            rentabilidad.append(None)
            compras.append(precioCompra)
            posicion_abierta=True
        elif rating < combo_rating and posicion_abierta == True:
            decisiones.append("Venta")#VENDO
            posicion_abierta=False
            print(compras)
            rentabilidad.append(tr.calcular_rentabilidad(compras,precioCompra))
            compras.clear()
        else:
            decisiones.append("NO SE REALIZA OPERACION")
            rentabilidad.append(None)
    compras.clear()

    # Agregar la lista de decisiones como una nueva columna al DataFrame
    peliculas_frame['Decision'] = decisiones
    peliculas_frame['Rentabilidad']= rentabilidad
    print("frame Disney",peliculas_frame)
    return peliculas_frame


def datosPeliculas(filename, studio):
    try:
        df = pd.read_csv(filename)  # Leer el archivo CSV
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {filename}")
        return None
    
    # Convertir la columna 'Release Date' a formato datetime si es necesario
    if 'Release Date' in df.columns:
        df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
    
    # Filtrar el Studio que hemos seleccionado
    df = df.loc[df['Studio'] == studio]

    return df

def leerURL(url, studio_txt):

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

    # Define the headers for your request with the User-Agent string
    headers = {"User-Agent": user_agent}

    # Make the request with the custom headers
    response = requests.get(url, headers=headers)

    date_pattern = r"^(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}$"

    if response.status_code == 200:

        respuesta = response.text
        soup = BeautifulSoup(respuesta, 'html.parser')

        titulos = []
        fechas_lanzamiento = []
        estudios = []

        tabla_peliculas = soup.find('table')

        if tabla_peliculas:
            
            filas = tabla_peliculas.find_all('tr')
            # Si hay al menos una fila (cabecera), obtener la última fila
            for fila in filas:                
                # Obtener los datos de la última fila
                datos = fila.find_all('td')
                titulo = fila.find_all('th')

                # Extraer el título de la película, el estudio y la fecha de lanzamiento
                if len(datos) >= 2:
                    fechas_lanzamiento.append(datos[0].get_text(strip=True))
                    titulos.append(titulo[0].get_text(strip=True))
                    estudios.append(datos[1].get_text(strip=True))
                    ult_fecha = datos[0].get_text(strip=True)
                    ult_estudio = datos[1].get_text(strip=True)
                elif len(datos) > 0:
                    fechas_lanzamiento.append(ult_fecha)
                    titulos.append(titulo[0].get_text(strip=True))
                    estudios.append(ult_estudio)
                

            ratings = get_movie_ratings(titulos)

            df = pd.DataFrame({'Title': titulos, 'Release Date': fechas_lanzamiento, 'Rating': ratings, 'Studio': estudios})
            # df = pd.DataFrame({'Title': titulos, 'Release Date': fechas_lanzamiento, 'Studio': estudios})
            print(df)
    else:
        print("NO ENTRA")
    return df

def thread_Disney(pill2kill,trading_data: dict, studio_txt,url,combo_comprar,comobo_vender,cola):

    inicializar_variables(combo_comprar,comobo_vender)
    ultimaPelicula(studio_txt,url,cola)

    while not pill2kill.wait(trading_data['time_period']):
        ultimaPelicula(studio_txt,url,cola)
        print("Checking films...")
        print(FRAMEDIRECTO)

def inicializar_variables(combo_comprar,comobo_vender):
    global COMBO_COMPRAR,COMBO_VENDER,FECHA_ULTIMA_PELICULA,RESULTADO_ULTIMA_PELICULA,NUEVA_PELICULA,FRAMEDIRECTO
    #van a ser lo que haya establecido el usuario de orgne
    COMBO_COMPRAR=combo_comprar
    COMBO_VENDER=comobo_vender
    #inicializao las variables cada vez que le pulso el boton de ticks en directo para que se reinicie todo y no se qued con los valores anteriores
    FECHA_ULTIMA_PELICULA=None
    RESULTADO_ULTIMA_PELICULA=None
    NUEVA_PELICULA=False
    FRAMEDIRECTO=pd.DataFrame()

def ultimaPelicula(studio_txt:str,url,cola):
    global FECHA_ULTIMA_PELICULA,RESULTADO_ULTIMA_PELICULA,NUEVA_PELICULA,FRAMEDIRECTO

    
    studio_frame = leerURL(url, studio_txt)#cojo las peliculas

    last_row = studio_frame.iloc[-1]
    
    if(FECHA_ULTIMA_PELICULA is None or last_row['Release Date']!=FECHA_ULTIMA_PELICULA):
        FECHA_ULTIMA_PELICULA = last_row['Release Date']
        print(FECHA_ULTIMA_PELICULA)
        # Asignar el Resultado a cada carrera
        RESULTADO_ULTIMA_PELICULA = studio_frame.at[studio_frame.index[-1], 'Rating']
        print(RESULTADO_ULTIMA_PELICULA)
        # FRAMEDIRECTO = pd.concat([FRAMEDIRECTO, piloto_frame.iloc[[-1]]], ignore_index=True)#GUARDO EL ULTIMO
        # FRAMEDIRECTO = pd.concat([FRAMEDIRECTO, piloto_frame.iloc[[-1]].drop(['Resultado'], axis=1)], ignore_index=True)#GUARDO EL ULTIMO sin las columnas que no me interesan
        print(last_row)
        cola.put(FRAMEDIRECTO)
        NUEVA_PELICULA = True
    else:
        print("No hay pelicula nueva")

def check_buy() -> Tuple[bool, bool]:
    global RESULTADO_ULTIMA_PELICULA,NUEVA_PELICULA,COMBO_COMPRAR
    print(NUEVA_PELICULA)

    if(NUEVA_PELICULA):
        if RESULTADO_ULTIMA_PELICULA >= COMBO_COMPRAR:#lo que ha elegido el usuario es lo mismo que el resultado de la carrera y es una carrera nueva
            NUEVA_PELICULA = False#si he invertido una vez por la carrera no invierto mas
            return True, True
        else:
            NUEVA_PELICULA = False
            return True, False
    else:
        return False, False
    
    # if CUR_SIGNAL.iloc[-1] >= CUR_MACD.iloc[-1] and CUR_RSI.iloc[-1] < 35 :
    #     return True
    # return False

def check_sell() -> bool:#ñle tendre que pasar el valor al que la he comprado cada una de las buy
    global RESULTADO_ULTIMA_PELICULA,NUEVA_PELICULA,COMBO_COMPRAR
    if(NUEVA_PELICULA and RESULTADO_ULTIMA_PELICULA < COMBO_VENDER):#lo que ha elegido el usuario es lo mismo que el resultado del partido y es un partdo nuevo
        NUEVA_PELICULA=False
        return True
    else:
        NUEVA_PELICULA=False
        return False
