from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import numpy as np
import tick_reader as tr


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
    '2023_teams.html'
]


def backtesting(prices: list, inicio: str, fin: str, url, combo_resultado: int, piloto: str):
    # Crear un DataFrame de la lista prices
    ticks_frame = pd.DataFrame(prices, columns=['time', 'price'])

    ticks_frame.to_excel('tick.xlsx', index=False)
    
    decisiones = []
    rentabilidad = []
    posicion_abierta=False

    piloto_frame=datosPiloto(piloto)
    piloto_frame['Fecha'] = pd.to_datetime(piloto_frame['Fecha'])

    # Initialize a new column 'precio' in piloto_frame with NaN values
    piloto_frame = piloto_frame[piloto_frame['Fecha'].between(inicio, fin)]
    piloto_frame['Precio'] = np.nan
    # Iterate over the rows in piloto_frame


    for i, row in piloto_frame.iterrows(): 
        resultado = row['Resultado']


        # Find the corresponding price in ticks_frame
        price = ticks_frame.loc[ticks_frame['time'] >= row['Fecha'], 'price'].first_valid_index()

        if price is not None:
            # If a price was found, update the 'precio' column in piloto_frame
            piloto_frame.at[i, 'Precio'] = float(ticks_frame.loc[price, 'price'])
        if resultado[0] == 'DNF' or resultado[0] == 'DNS' or resultado[0] == 'No participo' or resultado[0] == ' ' or resultado[0] == 'N':
            resultado = 30
        elif '*' in resultado[0]:
            # Eliminar el asterisco si está presente
            resultado = int(resultado[0].replace('*', ''))
        else:
            resultado = int(resultado[0])

        precioCompra = piloto_frame.at[i, 'Precio']
            
        if resultado <= combo_resultado and len(compras) < 10:
            decisiones.append("1")#COMPRO
            rentabilidad.append(None)
            compras.append(precioCompra)
            posicion_abierta=True
        elif resultado > combo_resultado and posicion_abierta == True:
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
    piloto_frame['Decision'] = decisiones
    piloto_frame['Rentabilidad']= rentabilidad
    print("frame f1",piloto_frame)
    return piloto_frame    


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


def obtener_resultados_piloto(html, nombre):
    # Parsea el HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Encuentra las filas que contienen el texto específico
    datos_piloto = []
    for fila in soup.find_all('tr'):
        if nombre in fila.get_text():
            datos = [td.get_text() for td in fila.find_all('td')]
            datos_piloto.append(datos)
    
    # Transponerlo para que sea una columna
    datos_piloto = list(zip(*datos_piloto))

    return datos_piloto

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




def datosPiloto(piloto):
    base_dir = os.path.abspath('src\Formula1\html')

    # Convert the HTML files list to full file paths
    html_results_files = [os.path.join(base_dir, file) for file in html_standings_files]
    html_dates_files = [os.path.join(base_dir, file) for file in html_calendars_files]
    html_teams_files = [os.path.join(base_dir, file) for file in html_pilotTeams_files]
    año = 2014
    cabeceras = ['Circuito', 'Fecha', 'Resultado']
    df = pd.DataFrame(columns=cabeceras)

    for result_file_name, date_file_name, teams_file_name in zip(html_results_files, html_dates_files, html_teams_files):
        if os.path.exists(result_file_name) and os.path.exists(date_file_name) and os.path.exists(teams_file_name):
            
            
            with open(result_file_name, 'r', encoding='utf-8') as file_results:
                html_content_results = file_results.read()
            
            with open(date_file_name, 'r', encoding='utf-8') as file_dates:
                html_content_dates = file_dates.read()

            with open(teams_file_name, 'r', encoding='utf-8') as file_teams:
                html_content_teams = file_teams.read()


            soup_tabla_principal = BeautifulSoup(html_content_results, 'html.parser')
            soup_tabla_fechas = BeautifulSoup(html_content_dates, 'html.parser')

            # Buscar las filas de la tabla principal que contengan el texto específico
            # Extraer los datos de las filas y transponerlos en una columna
            filas_con_texto = obtener_resultados_piloto(html_content_results, piloto)
            filas_con_texto = filas_con_texto[3:]


            # Agregar las columnas adicionales para el encabezado de la tabla y las fechas asociadas
            encabezado_tabla = [th.get_text(strip=True) for th in soup_tabla_principal.find('tr').find_all('th')]
            encabezado_tabla = encabezado_tabla[3:]
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

    return df


def convert_date(fecha_texto, año):           

    mes, dia = fecha_texto.split()
    mes_numero = meses.get(mes)
    fecha_formateada = f"{año}-{mes_numero}-{dia.zfill(2)}"

    return fecha_formateada


