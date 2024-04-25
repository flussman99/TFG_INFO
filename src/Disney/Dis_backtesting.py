from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import numpy as np
import tick_reader as tr


data = []
compras = []

meses = {
    'enero': '01',
    'febrero': '02',
    'marzo': '03',
    'abril': '04',
    'mayo': '05',
    'junio': '06',
    'julio': '07',
    'agosto': '08',
    'septiembre': '09',
    'octubre': '10',
    'noviembre': '11',
    'diciembre': '12'
}

acciones_api = {
    'RNO.PAR': 'RENA.PAR',#france
    'AML.LSE': 'ASTO.LSE',#uk
    'RACE.NYSE': 'RACE.MIL'#italy
}

acciones_escuderias = {
    'Mercedes-AMG Petronas Formula One Team': 'HPQ.NYSE',
    'Mercedes AMG Petronas Motorsport': 'QCOM.NYSE',
    'Mercedes AMG Petronas F1 Team': 'QCOM.NYSE',
    'Scuderia Ferrari': 'RACE.NYSE', 
    'Scuderia Ferrari Mission Winnow': 'RACE.NYSE',
    'Oracle Red Bull Racing': 'HMC.NYSE', #Honda es su motorista exclusivo, ellos no cotizan
    'Red Bull Racing Honda': 'RNO.PAR',
    'Red Bull Racing': 'RNO.PAR',
    'Infiniti Red Bull Racing': 'RNO.PAR',
    'McLaren Formula 1 Team': 'GOOG.NAS', #Google es su patrocinador principal, ellos no cotizan
    'McLaren F1 Team': 'GOOG.NAS',
    'McLaren Honda': 'HMC.NYSE',
    'Aston Martin Aramco Cognizant Formula One Team': 'AML.LSE',
    'Aston Martin Cognizant Formula One Team': 'AML.LSE',
    'BWT Racing Point F1 Team': 'AML.LSE',
    'SportPesa Racing Point F1 Team': 'AML.LSE',
    'Racing Point Force India F1 Team': 'AML.LSE',
    'Sahara Force India F1 Team': 'AML.LSE',
    'BWT Alpine F1 Team': 'RNO.PAR',
    'Alpine F1 Team': 'RNO.PAR',
    'Renault DP World F1 Team': 'RNO.PAR',
    'Renault F1 Team': 'RNO.PAR',
    'Renault Sport Formula One Team': 'RNO.PAR',
    'Renault Sport F1 Team': 'RNO.PAR',
    'Lotus F1 Team': 'RNO.PAR',
    'Scuderia AlphaTauri': 'HMC.NYSE',
    'Scuderia AlphaTauri Honda': 'HMC.NYSE',
    'Aston Martin Red Bull Racing': 'HMC.NYSE',
    'Red Bull Toro Rosso Honda': 'HMC.NYSE',
    'Scuderia Toro Rosso': 'RNO.PAR',
    'Alfa Romeo F1 Team Stake': 'RACE.NYSE', #Motorista Ferrari
    'Alfa Romeo F1 Team ORLEN': 'RACE.NYSE', 
    'Alfa Romeo Racing ORLEN': 'RACE.NYSE', 
    'Alfa Romeo Racing': 'RACE.NYSE', 
    'Alfa Romeo Sauber F1 Team': 'RACE.NYSE', 
    'Sauber F1 Team': 'AMX.NYSE', #Claro era su patrocinador, siendo parte de la matriz América Móvil
    'Caterham F1 Team': 'AIR.MAD', #Airbus era su patrocinador principal
    'MoneyGram Haas F1 Team': 'RACE.NYSE', #Haas usa motores de Ferrari
    'Haas F1 Team': 'RACE.NYSE', #NO ESTAAAA
    'Uralkali Haas F1 Team': 'RACE.NYSE',
    'Williams Racing': 'PG.NYSE', #Duracell, uno de los principales patrocinadores, pertenece a Procter & Gamble
    'ROKiT Williams Racing': 'PG.NYSE', #Duracell, uno de los principales patrocinadores, pertenece a Procter & Gamble
    'Williams Martini Racing': 'PG.NYSE' #Duracell, uno de los principales patrocinadores, pertenece a Procter & Gamble
    # Agrega más escuderías y sus acciones asociadas según sea necesario
}

pais_Accion = {
    'NYSE': 'united states',
    'PAR': 'france',
    'NAS': 'united states',
    'LSE': 'united kingdom', 
    'MAD': 'spain',
    'MIL': 'italy'
}

imagenes_pilotos = {
    'Fernando Alonso': 'src/imagenes/F1/Alonso.png',
    'Alexander Albon': 'src/imagenes/F1/Albon.png',
    'Valteri Bottas': 'src/imagenes/F1/Bottas.png',
    'Jenson Button': 'src/imagenes/F1/Button.png',
    'Nick De Vries': 'src/imagenes/F1/DeVries.png',
    'Marcus Ericsson': 'src/imagenes/F1/Ericsson.png',
    'Pierre Gasly': 'src/imagenes/F1/Gasly.png',
    'Antonio Giovinazzi': 'src/imagenes/F1/Giovinazzi.png',
    'Roman Grosjean': 'src/imagenes/F1/Grosjean.png',
    'Esteban Gutiérrez': 'src/imagenes/F1/Gutiérrez.png',
    'Lewis Hamilton': 'src/imagenes/F1/Hamilton.png',
    'Nico Hulkenberg': 'src/imagenes/F1/Hulkenberg.png',
    'Kamui Kobayashi': 'src/imagenes/F1/Kobayashi.png',
    'Robert Kubica': 'src/imagenes/F1/Kubica.png',
    'Daniil Kvyat': 'src/imagenes/F1/Kvyat.png',
    'Nicholas Latifi': 'src/imagenes/F1/Latifi.png',
    'Charles Leclerc': 'src/imagenes/F1/Leclerc.png',
    'Kevin Magnussen': 'src/imagenes/F1/Magnussen.png',
    'Pastor Maldonado': 'src/imagenes/F1/Maldonado.png',
    'Felipe Massa': 'src/imagenes/F1/Massa.png',
    'Lando Norris': 'src/imagenes/F1/Norris.png',
    'Esteban Ocon': 'src/imagenes/F1/Ocon.png',
    'Jolyon Palmer': 'src/imagenes/F1/Palmer.png',
    'Sergio Pérez': 'src/imagenes/F1/Pérez.png',
    'Oscar Piastri': 'src/imagenes/F1/Piastri.png',
    'Kimi Raikkonen': 'src/imagenes/F1/Raikkonen.png',
    'Daniel Ricciardo': 'src/imagenes/F1/Ricciardo.png',
    'Nico Rosberg': 'src/imagenes/F1/Rosberg.png',
    'George Russell': 'src/imagenes/F1/Russell.png',
    'Carlos Sainz': 'src/imagenes/F1/Sainz.png',
    'Logan Sargeant': 'src/imagenes/F1/Sargeant.png',
    'Mick Schumacher': 'src/imagenes/F1/Schumacher.png',
    'Lance Stroll': 'src/imagenes/F1/Stroll.png',
    'Yuki Tsunoda': 'src/imagenes/F1/Tsunoda.png',
    'Stoffel Vandoorne': 'src/imagenes/F1/Vandoorne.png',
    'Max Verstappen': 'src/imagenes/F1/Verstappen.png',
    'Sebastian Vettel': 'src/imagenes/F1/Vettel.png',
    'Guanyu Zhou': 'src/imagenes/F1/Zhou.png'
}

# List of HTML files to process from https://www.f1-fansite.com/f1-results/f1-standings-2023-championship/
html_movies_files = [
    'Disney_2010_2019.html',
    'Disney_Animation_2010_2019.html',
    'Disney_2020_2029.html',
    'Disney_Animation_2020_2029.html'
]

html_calendars_files = [
    '2014_calendar.html',
    '2015_calendar.html',
    '2016_calendar.html',
    '2017_calendar.html',
    '2018_calendar.html',
    '2019_calendar.html',
    '2020_calendar.html',
    '2021_calendar.html',
    '2022_calendar.html',
    '2023_calendar.html'
]

# https://fiaresultsandstatistics.motorsportstats.com/series/fia-formula-one-world-championship/season/2023
html_pilotTeams_files = [
    '2014_teams.html',
    '2015_teams.html',
    '2016_teams.html',
    '2017_teams.html',
    '2018_teams.html',
    '2019_teams.html',
    '2020_teams.html',
    '2021_teams.html',
    '2022_teams.html',
    '2023_teams.html'
]

def backtesting():
    base_dir = os.path.abspath('src\Disney\html')
    # Parsear el HTML
    html_films_files = [os.path.join(base_dir, file) for file in html_movies_files]

    date_pattern = r"^(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}$"


    for movies_file_name in html_films_files:
        if os.path.exists(movies_file_name):
            
            print(movies_file_name)
            with open(movies_file_name, 'r', encoding='utf-8') as file_results:
                html_content_movies = file_results.read()

            soup = BeautifulSoup(html_content_movies, 'html.parser')
            # Encontrar todas las filas de la tabla
            # Encontrar todas las filas de la tabla
            rows = soup.find_all('tr')

            # Crear listas para almacenar los datos
            titles = []
            release_dates = []
            last_release_date = None
            # Iterar sobre cada fila (empezando desde la segunda fila para evitar los encabezados)
            for row in rows[1:]:
                # Encontrar las celdas de fecha de lanzamiento y título
                cells = row.find_all(['td', 'th'])
                # Obtener la fecha de lanzamiento
                release_date = cells[0].get_text(strip=True)
                # Si la fecha de lanzamiento no es una fecha válida, utiliza la última fecha guardada
                if not re.match(date_pattern, release_date):
                    release_date = last_release_date
                else:
                    # Intenta convertir la fecha a formato datetime
                    release_date_parsed = pd.to_datetime(release_date, errors='coerce')
                    # Si la conversión fue exitosa, actualiza la última fecha válida
                    if not pd.isnull(release_date_parsed):
                        last_release_date = release_date_parsed
                if len(cells) > 1:
                    title = cells[1].get_text(strip=True)
                # Agregar los datos a las listas
                titles.append(title)
                release_dates.append(release_date)
                last_release_date = release_date

            # Crear el DataFrame
            df = pd.DataFrame({'Title': titles, 'Release Date': release_dates})
            df.to_excel(movies_file_name + '.xlsx', index=False)
            # Mostrar el DataFrame
            print(df)