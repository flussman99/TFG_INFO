from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import requests
import numpy as np
from typing import Tuple
import tick_reader as tr
from datetime import datetime


data = []
compras = []

meses = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}

acciones_api = {
    'RNO.PAR': 'RENA.PAR',#france
    'AML.LSE': 'ASTO.LSE',#uk
    'RACE.NYSE': 'RACE.MIL'#italy
}

acciones_escuderias = {
    'Mercedes-AMG Petronas Motorsport' : 'HPQ.NYSE',
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
    'Aston Martin Aramco Formula One Team': 'AML.LSE',
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
    'Visa Cash App RB F1 Team': 'HMC.NYSE',
    'Scuderia AlphaTauri': 'HMC.NYSE',
    'Scuderia AlphaTauri Honda': 'HMC.NYSE',
    'Aston Martin Red Bull Racing': 'HMC.NYSE',
    'Red Bull Toro Rosso Honda': 'HMC.NYSE',
    'Scuderia Toro Rosso': 'RNO.PAR',
    'Manor Racing MRT': 'RNO.PAR',
    'Stake F1 Team Kick Sauber': 'RACE.NYSE', #Motorista Ferrari
    'Alfa Romeo F1 Team Stake': 'RACE.NYSE', 
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

imagenes_escuderias = {
    'Mercedes-AMG Petronas Formula One Team': 'src/imagenes/escuderias/Mercedes.png',
    'Mercedes AMG Petronas Motorsport': 'src/imagenes/escuderias/Mercedes.png',
    'Mercedes AMG Petronas F1 Team': 'src/imagenes/escuderias/Mercedes.png',
    'Scuderia Ferrari': 'src/imagenes/escuderias/Ferrari.png',
    'Scuderia Ferrari Mission Winnow': 'src/imagenes/escuderias/Ferrari.png',
    'Oracle Red Bull Racing': 'src/imagenes/escuderias/RedBull.png',
    'Red Bull Racing Honda': 'src/imagenes/escuderias/RedBull.png',
    'Red Bull Racing': 'src/imagenes/escuderias/RedBull.png',
    'Infiniti Red Bull Racing': 'src/imagenes/escuderias/RedBull.png',
    'McLaren Formula 1 Team': 'src/imagenes/escuderias/McLaren.png',
    'McLaren F1 Team': 'src/imagenes/escuderias/McLaren.png',
    'McLaren Honda': 'src/imagenes/escuderias/McLaren.png',
    'Aston Martin Aramco Formula One Team': 'src/imagenes/escuderias/AstonMartin.png',
    'Aston Martin Aramco Cognizant Formula One Team': 'src/imagenes/escuderias/AstonMartin.png',
    'Aston Martin Cognizant Formula One Team': 'src/imagenes/escuderias/AstonMartin.png',
    'BWT Racing Point F1 Team': 'src/imagenes/escuderias/BWTRacing.png',
    'SportPesa Racing Point F1 Team': 'src/imagenes/escuderias/BWTRacing.png',
    'Racing Point Force India F1 Team': 'src/imagenes/escuderias/BWTRacing.png',
    'Sahara Force India F1 Team': 'src/imagenes/escuderias/SaharaForce.png',
    'BWT Alpine F1 Team': 'src/imagenes/escuderias/Alpine.png',
    'Alpine F1 Team': 'src/imagenes/escuderias/Alpine.png',
    'Renault DP World F1 Team': 'src/imagenes/escuderias/Renault.png',
    'Renault F1 Team': 'src/imagenes/escuderias/Renault.png',
    'Renault Sport Formula One Team': 'src/imagenes/escuderias/Renault.png',
    'Renault Sport F1 Team': 'src/imagenes/escuderias/Renault.png',
    'Lotus F1 Team': 'src/imagenes/escuderias/Renault.png',
    'Visa Cash App RB F1 Team': 'src/imagenes/escuderias/RedBull.png',
    'Scuderia AlphaTauri': 'src/imagenes/escuderias/AlphaTauri.png',
    'Scuderia AlphaTauri Honda': 'src/imagenes/escuderias/AlphaTauri.png',
    'Aston Martin Red Bull Racing': 'src/imagenes/escuderias/AstonMartinRedBullRacing.png',
    'Red Bull Toro Rosso Honda': 'src/imagenes/escuderias/AstonMartinRedBullRacing.png',
    'Scuderia Toro Rosso': 'src/imagenes/escuderias/ScuderiaToroRosso.png',
    'Stake F1 Team Kick Sauber': 'src/imagenes/escuderias/Stake.png',
    'Alfa Romeo F1 Team Stake': 'src/imagenes/escuderias/Stake.png',
    'Alfa Romeo F1 Team ORLEN': 'src/imagenes/escuderias/AlfaRomeo.png',
    'Alfa Romeo F1 Team ORLEN': 'src/imagenes/escuderias/AlfaRomeo.png',
    'Alfa Romeo Racing ORLEN': 'src/imagenes/escuderias/AlfaRomeo.png',
    'Alfa Romeo Racing': 'src/imagenes/escuderias/AlfaRomeo.png',
    'Alfa Romeo Sauber F1 Team': 'src/imagenes/escuderias/AlfaRomeo.png',
    'Sauber F1 Team': 'src/imagenes/escuderias/AlfaRomeo.png',
    'Caterham F1 Team': 'src/imagenes/escuderias/Caterham.png',
    'MoneyGram Haas F1 Team': 'src/imagenes/escuderias/Haas.png',
    'Haas F1 Team': 'src/imagenes/escuderias/Haas.png',
    'Uralkali Haas F1 Team': 'src/imagenes/escuderias/Haas.png',
    'Williams Racing': 'src/imagenes/escuderias/Williams.png',
    'ROKiT Williams Racing': 'src/imagenes/escuderias/Williams.png',
    'Williams Martini Racing': 'src/imagenes/escuderias/Williams.png'
}

imagenes_pilotos = {
    'Fernando Alonso': 'src/imagenes/F1/Alonso.png',
    'Alexander Albon': 'src/imagenes/F1/Albon.png',
    'Valtteri Bottas': 'src/imagenes/F1/Bottas.png',
    'Jenson Button': 'src/imagenes/F1/Button.png',
    'Nick De Vries': 'src/imagenes/F1/DeVries.png',
    'Marcus Ericsson': 'src/imagenes/F1/Ericsson.png',
    'Pierre Gasly': 'src/imagenes/F1/Gasly.png',
    'Antonio Giovinazzi': 'src/imagenes/F1/Giovinazzi.png',
    'Roman Grosjean': 'src/imagenes/F1/Grosjean.png',
    'Esteban Gutiérrez': 'src/imagenes/F1/Gutiérrez.png',
    'Lewis Hamilton': 'src/imagenes/F1/Hamilton.png',
    'Nico Hülkenberg': 'src/imagenes/F1/Hulkenberg.png',
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
    'Ayumu Iwasa': 'src/imagenes/F1/Iwasa.png',
    'Ollie Bearman': 'src/imagenes/F1/Bearman.png',
    'Zhou Guanyu': 'src/imagenes/F1/Zhou.png'
}

# List of HTML files to process from https://www.f1-fansite.com/f1-results/f1-standings-2023-championship/
html_standings_files = [
    '2014.html',
    '2015.html',
    '2016.html',
    '2017.html', 
    '2018.html',
    '2019.html',
    '2020.html',
    '2021.html',
    '2022.html',
    '2023.html'
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
    '2023_teams.html',
    '2024_teams.html'
]


def backtesting(prices: list, inicio: str, fin: str, url, combo_resultado: int, combo_venta: int, piloto: str):
    # Crear un DataFrame de la lista prices
    ticks_frame = pd.DataFrame(prices, columns=['time', 'price'])
    
    decisiones = []
    rentabilidad = []
    posicion_abierta=False

    piloto_frame=datosPiloto(prices, inicio, fin, url, piloto)
    
    print(ticks_frame)

    # Iterate over the rows in piloto_frame
    for i, row in piloto_frame.iterrows(): 
        resultado = row['Resultado']


        # Find the corresponding price in ticks_frame
        price = ticks_frame.loc[ticks_frame['time'] >= row['Fecha'], 'price'].first_valid_index()

        if price is not None:
            # If a price was found, update the 'precio' column in piloto_frame
            piloto_frame.at[i, 'Precio'] = float(ticks_frame.loc[price, 'price'])
        if 'DNF' in resultado[0] or 'DNS'  in resultado[0] or 'No participo' in resultado[0] or ' ' in resultado[0] or 'N' in resultado[0] or 'DSQ' in resultado[0] or 'WD' in resultado[0]:
            resultado = 30
        elif '*' in resultado[0]:
            # Eliminar el asterisco si está presente
            resultado = int(resultado[0].replace('*', ''))
        else:
            resultado = int(resultado[0])

        precioCompra = piloto_frame.at[i, 'Precio']
            
        if comprobar(resultado, combo_resultado) and len(compras) < 10:
            decisiones.append("Compra")#COMPRO
            rentabilidad.append(None)
            compras.append(precioCompra)
            posicion_abierta=True
        elif not comprobar(resultado, combo_resultado) and posicion_abierta == True:
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
    piloto_frame['Decision'] = decisiones
    piloto_frame['Rentabilidad']= rentabilidad
    print("frame f1",piloto_frame)
    return piloto_frame    

def comprobar(resultado, combo_resultado):
    
    if combo_resultado == "Top 1":
        resultado_combo = 1
    elif combo_resultado == "Top 3":
        resultado_combo = 3
    elif combo_resultado == "Top 5":
        resultado_combo = 5
    elif combo_resultado == "Top 10":
        resultado_combo = 10
    else:
        resultado_combo = 30
    
    if resultado <= resultado_combo:
        return True
    else:
        return False

def obtener_accion_escuderia(piloto, año):
    base_dir = os.path.abspath('src\Formula1\html')
    dir = año + '_teams.html'
    file_name = os.path.join(base_dir, dir)

    if os.path.exists(file_name):

        with open(file_name, 'r', encoding='utf-8') as file:
            html = file.read()

        escuderia = obtener_escuderia_piloto(html, piloto)

    return acciones_escuderias[escuderia]


        

def obtener_listado_años():
    years = []
    for file in html_standings_files:
        # Utilizar una expresión regular para encontrar el año en el nombre del archivo
        match = re.search(r'(\d{4})\.html', file)
        if match:
            year = match.group(1)
            years.append(year)
    years.append(2024)

    return years
    

def obtener_listado_pilotos(año):
    base_dir = os.path.abspath('src\Formula1\html')
    dir = año + '_teams.html'
    file_name = os.path.join(base_dir, dir)
    nombres_pilotos = []

    if os.path.exists(file_name):

        with open(file_name, 'r', encoding='utf-8') as file:
            html = file.read()

        soup = BeautifulSoup(html, 'html.parser')

        filas = soup.find_all('tr')

        for fila in filas:
            celdas = fila.find_all('td')
            if len(celdas) == 3:  # Si hay tres celdas, la primera contiene la escudería y la tercera el piloto
                nombres_pilotos.append(celdas[2].text.strip())

            if len(celdas) == 2:
                nombres_pilotos.append(celdas[1].text.strip())


    # Devuelve el listado de nombres de pilotos
    return nombres_pilotos


def obtener_resultados_piloto(soup, nombre):
    # Parsea el HTML
    tabla_resultados = soup.find('table', class_="motor-sport-results msr_season_driver_results")
    
    if tabla_resultados:
        # Encuentra las filas que contienen el texto específico
        datos_piloto = []
        for fila in tabla_resultados.find_all('tr'):
            if nombre in fila.get_text():
                datos = [td.get_text() for td in fila.find_all('td')]
                datos_piloto.append(datos)
        
        # Transponerlo para que sea una columna
        datos_piloto = list(zip(*datos_piloto))
        encabezado_tabla = [th.get_text(strip=True) for th in tabla_resultados.find('tr').find_all('th')]

    return datos_piloto, encabezado_tabla

#Cambiar que si no compite coge la ultima escuderia por orden alfabetico
def obtener_escuderia_piloto(html, nombre):

    soup = BeautifulSoup(html, 'html.parser')
    escuderia_piloto = ''

    # Extraer las filas de la tabla
    filas = soup.find_all('tr')


    for fila in filas:
        celdas = fila.find_all('td')
        if len(celdas) == 3:  # Si hay tres celdas, la primera contiene la escudería y la tercera el piloto
            piloto = celdas[2].text.strip()
            if(celdas[0].text.strip() != ''):
                escuderia_piloto = celdas[0].text.strip()
            if piloto == nombre:
                break  # Salir del bucle una vez que se haya encontrado el piloto

    return escuderia_piloto

def obtener_periodo_valido(piloto, año_base):
    años = obtener_listado_años()
    accion_base = obtener_accion_escuderia(piloto, str(año_base))
    año_min = int(año_base)
    año_max = int(año_base)
    print('Accion base', accion_base)
    for año in años:
        accion_año = obtener_accion_escuderia(piloto, str(año))
        año = int(año)
        if accion_año == accion_base:
            if año_max < año:
                año_max = año
            elif año_min > año:
                año_min = año

    return año_min, año_max

def datosPiloto(ticks:list,inicio: str, fin: str, url:str,piloto:str):

    df_HTML = leerHTML(piloto, inicio, fin)
    df_URL = leerURL(url, piloto)
    df_URL = df_URL[df_URL['Fecha'].between(inicio, fin)]
    if list(df_HTML.columns) != list(df_URL.columns):
        print("Los DataFrames no tienen las mismas columnas.")
        return None
    
    df_HTML = pd.concat([df_HTML, df_URL], ignore_index=True)

    return df_HTML


def leerHTML(piloto, inicio, fin):
    base_dir = os.path.abspath('src\Formula1\html')

    # Convert the HTML files list to full file paths
    html_results_files = [os.path.join(base_dir, file) for file in html_standings_files]
    html_dates_files = [os.path.join(base_dir, file) for file in html_calendars_files]
    año = 2014
    cabeceras = ['Circuito', 'Fecha', 'Resultado']
    df = pd.DataFrame(columns=cabeceras)

    for result_file_name, date_file_name in zip(html_results_files, html_dates_files):
        if os.path.exists(result_file_name) and os.path.exists(date_file_name):
            
            
            with open(result_file_name, 'r', encoding='utf-8') as file_results:
                html_content_results = file_results.read()
            
            with open(date_file_name, 'r', encoding='utf-8') as file_dates:
                html_content_dates = file_dates.read()


            soup_tabla_principal = BeautifulSoup(html_content_results, 'html.parser')
            soup_tabla_fechas = BeautifulSoup(html_content_dates, 'html.parser')

            # Buscar las filas de la tabla principal que contengan el texto específico
            # Extraer los datos de las filas y transponerlos en una columna
            filas_con_texto, encabezado_tabla = obtener_resultados_piloto(soup_tabla_principal, piloto)
            filas_con_texto = filas_con_texto[3:]
            encabezado_tabla = encabezado_tabla[3:]
            # Agregar las columnas adicionales para las fechas asociadas
            fechas_asociadas = [fecha.get_text(strip=True) for fecha in soup_tabla_fechas.find_all('td', class_='msr_col2')]


            fechas_formateadas = []

            # Formatear las fechas en el formato deseado
            for fecha_texto in fechas_asociadas:
                if fecha_texto:
                    fechas_formateadas.append(convert_date(fecha_texto, año))
                else:
                    fechas_formateadas.append('')  # Mantener un espacio en blanco si no hay fecha


            nuevo_df = pd.DataFrame(encabezado_tabla, columns=['Circuito'])
            nuevo_df['Fecha'] = fechas_formateadas
            if filas_con_texto == []:
                filas_con_texto = ['No participo'] * len(fechas_formateadas)

            nuevo_df['Resultado'] = filas_con_texto

            año = año + 1

        df = pd.concat([df, nuevo_df], ignore_index=True)


    df['Fecha'] = pd.to_datetime(df['Fecha'])
    # Initialize a new column 'precio' in piloto_frame with NaN values
    df = df[df['Fecha'].between(inicio, fin)]
    df['Precio'] = np.nan

    return df

def leerURL(url, piloto):

    print(url)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

    # Define the headers for your request with the User-Agent string
    headers = {"User-Agent": user_agent}

    # Make the request with the custom headers
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        respuesta = response.text
        soup_tabla_principal = BeautifulSoup(respuesta, 'html.parser')
        soup_tabla_fechas = BeautifulSoup(respuesta, 'html.parser')

        año = 2024

        cabeceras = ['Circuito', 'Fecha', 'Resultado']
        df = pd.DataFrame(columns=cabeceras)

        # Buscar las filas de la tabla principal que contengan el texto específico
        # Extraer los datos de las filas y transponerlos en una columna
        filas_con_texto, encabezado_tabla = obtener_resultados_piloto(soup_tabla_principal, piloto)
        filas_con_texto = filas_con_texto[3:]
        encabezado_tabla = encabezado_tabla[3:]


        # Agregar las columnas adicionales para el encabezado de la tabla y las fechas asociadas
        tabla_fechas = soup_tabla_fechas.find('table', class_="motor-sport-results msr_season_summary tablesorter")
        if tabla_fechas:
            fechas_asociadas = [fecha.get_text(strip=True) for fecha in tabla_fechas.find_all('td', class_='msr_col2')]

            fechas_formateadas = []
            # Formatear las fechas en el formato deseado
            for fecha_texto in fechas_asociadas:
                if fecha_texto:
                    fechas_formateadas.append(convert_date(fecha_texto, año))
                else:
                    fechas_formateadas.append('')  # Mantener un espacio en blanco si no hay fecha


        nuevo_df = pd.DataFrame(encabezado_tabla, columns=['Circuito'])
        nuevo_df['Fecha'] = fechas_formateadas
        if filas_con_texto == []:
            filas_con_texto = ['No participo'] * len(fechas_formateadas)
        
        print(filas_con_texto)
        print(nuevo_df)

        nuevo_df['Resultado'] = filas_con_texto

        df = pd.concat([df, nuevo_df], ignore_index=True)


        df['Fecha'] = pd.to_datetime(df['Fecha'])
        # Initialize a new column 'precio' in piloto_frame with NaN values
        df['Precio'] = np.nan

        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Filtrar las filas cuya fecha es posterior al día de hoy
        df = df[df['Fecha'] <= fecha_actual]
                        
    else:
        print("Error al obtener la URL. Código de estado:", response.status_code) 

    return df


def convert_date(fecha_texto, año):           

    mes, dia = fecha_texto.split()
    mes_numero = meses.get(mes)
    fecha_formateada = f"{año}-{mes_numero}-{dia.zfill(2)}"

    return fecha_formateada

def thread_F1(pill2kill,trading_data: dict, piloto_txt,url,combo_comprar,comobo_vender,cola):

    inicializar_variables(combo_comprar,comobo_vender)
    ultimaCarrera(piloto_txt,url,cola)

    while not pill2kill.wait(trading_data['time_period']):
        ultimaCarrera(piloto_txt,url,cola)
        print("Checking races...")
        print(FRAMEDIRECTO)

def inicializar_variables(combo_comprar,comobo_vender):
    global COMBO_COMPRAR,COMBO_VENDER,FECHA_ULTIMA_CARRERA,RESULTADO_ULTIMA_CARRERA,NUEVA_CARRERA,FRAMEDIRECTO
    #van a ser lo que haya establecido el usuario de orgne
    COMBO_COMPRAR=combo_comprar
    COMBO_VENDER=comobo_vender
    #inicializao las variables cada vez que le pulso el boton de ticks en directo para que se reinicie todo y no se qued con los valores anteriores
    FECHA_ULTIMA_CARRERA=None
    RESULTADO_ULTIMA_CARRERA=None
    NUEVA_CARRERA=False
    FRAMEDIRECTO=pd.DataFrame()

def ultimaCarrera(piloto_txt:str,url,cola):
    global FECHA_ULTIMA_CARRERA,RESULTADO_ULTIMA_CARRERA,NUEVA_CARRERA,FRAMEDIRECTO

    
    piloto_frame = leerURL(url, piloto_txt)#cojo las carreras
    # # piloto_frame['Fecha'] = pd.to_datetime(piloto_frame['Fecha'])
    # data.clear()#ya lo tengo que limpiar
    last_row = piloto_frame.iloc[-1]
    if(FECHA_ULTIMA_CARRERA is None or last_row['Fecha']!=FECHA_ULTIMA_CARRERA):
        FECHA_ULTIMA_CARRERA = last_row['Fecha']
        print(FECHA_ULTIMA_CARRERA)
        # Asignar el Resultado a cada carrera
        RESULTADO_ULTIMA_CARRERA = piloto_frame.at[piloto_frame.index[-1], 'Resultado']
        print(RESULTADO_ULTIMA_CARRERA)
        filaAdd=piloto_frame.iloc[[-1]].drop(['Precio'], axis=1)
        FRAMEDIRECTO = pd.concat([FRAMEDIRECTO,  filaAdd], ignore_index=True)#GUARDO EL ULTIMO sin las columnas que no me interesan
        # FRAMEDIRECTO = pd.concat([FRAMEDIRECTO, piloto_frame.iloc[[-1]]], ignore_index=True)#GUARDO EL ULTIMO
        # FRAMEDIRECTO = pd.concat([FRAMEDIRECTO, piloto_frame.iloc[[-1]].drop(['Resultado'], axis=1)], ignore_index=True)#GUARDO EL ULTIMO sin las columnas que no me interesan
        print(last_row)
        cola.put(FRAMEDIRECTO)
        NUEVA_CARRERA = True
    else:
        print("No hay carrera nueva")

def parar_carreras(self):
    global FRAMEDIRECTO
    frame=FRAMEDIRECTO
    FRAMEDIRECTO = pd.DataFrame(columns=['Circuito', 'Fecha', 'Resultado'])
    return frame

def check_buy() -> Tuple[bool, bool]:
    global RESULTADO_ULTIMA_CARRERA,NUEVA_CARRERA,COMBO_COMPRAR
    print(NUEVA_CARRERA)

    if(NUEVA_CARRERA):
        if RESULTADO_ULTIMA_CARRERA <= COMBO_COMPRAR:#lo que ha elegido el usuario es lo mismo que el resultado de la carrera y es una carrera nueva
            NUEVA_CARRERA=False#si he invertido una vez por la carrera no invierto mas
            return True, True
        else:
            NUEVA_CARRERA=False
            return True, False
    else:
        return False, False
    
    # if CUR_SIGNAL.iloc[-1] >= CUR_MACD.iloc[-1] and CUR_RSI.iloc[-1] < 35 :
    #     return True
    # return False

def check_sell() -> bool:#ñle tendre que pasar el valor al que la he comprado cada una de las buy
    global RESULTADO_ULTIMA_CARRERA,NUEVA_CARRERA,COMBO_COMPRAR   
    if(NUEVA_CARRERA and RESULTADO_ULTIMA_CARRERA > COMBO_VENDER):#lo que ha elegido el usuario es lo mismo que el resultado del partido y es un partdo nuevo
        NUEVA_CARRERA=False
        return True
    else:
        NUEVA_CARRERA=False
        return False
