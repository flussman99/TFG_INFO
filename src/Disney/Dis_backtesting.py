import threading
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import numpy as np
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

    peliculas_frame=datosPeliculas('src\Disney\html\Disney_Pelis_2010_2024.csv', studio)
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
            decisiones.append("1")#COMPRO
            rentabilidad.append(None)
            compras.append(precioCompra)
            posicion_abierta=True
        elif rating < combo_rating and posicion_abierta == True:
            decisiones.append("-1")#VENDO
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

def datosPeliculas_antiguo():
    base_dir = os.path.abspath('src\Disney\html')
    html_films_files = [os.path.join(base_dir, file) for file in html_movies_files]

    date_pattern = r"^(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}$"

    for movies_file_name in html_films_files:
        if os.path.exists(movies_file_name):
            print(movies_file_name)
            with open(movies_file_name, 'r', encoding='utf-8') as file_results:
                html_content_movies = file_results.read()

            soup = BeautifulSoup(html_content_movies, 'html.parser')
            rows = soup.find_all('tr')

            titles = []
            release_dates = []

            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                release_date = cells[0].get_text(strip=True)
                if not re.match(date_pattern, release_date):
                    release_date = last_release_date
                else:
                    release_date_parsed = pd.to_datetime(release_date, errors='coerce')
                    if not pd.isnull(release_date_parsed):
                        last_release_date = release_date_parsed
                if len(cells) > 1:
                    title = cells[1].get_text(strip=True)
                    titles.append(title)
                else:
                    titles.append(None)
                release_dates.append(release_date)
                last_release_date = release_date

            ratings = get_movie_ratings(titles)

            df = pd.DataFrame({'Title': titles, 'Release Date': release_dates, 'Rating': ratings})
            df.to_excel(movies_file_name + '.xlsx', index=False)
            print(df)
    return df
