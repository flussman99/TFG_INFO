from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np


data = []

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


def backtesting(nombre:str, prices: list):
    # Crear un DataFrame de la lista prices
    ticks_frame = pd.DataFrame(prices, columns=['time', 'price'])
    # Convert 'time' from Unix timestamp to datetime
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
    # Extract the date
    ticks_frame['time'] = ticks_frame['time'].dt.date.astype(str)#conventirlo a string para poder comparar con el dataframe de las carreras
    print(ticks_frame)
    ticks_frame.to_excel('tick.xlsx', index=False)
    piloto_frame=datosPiloto(nombre)
    # Initialize a new column 'precio' in piloto_frame with NaN values
    piloto_frame['precio'] = np.nan
    # Iterate over the rows in equipos_frame
    for i, row in piloto_frame.iterrows(): 
        # Find the corresponding price in ticks_frame
        price = ticks_frame.loc[ticks_frame['time'] >= row['Fecha'], 'price'].first_valid_index()
        if price is not None:
            # If a price was found, update the 'precio' column in piloto_frame
            piloto_frame.at[i, 'precio'] = ticks_frame.loc[price, 'price']
    
    print(piloto_frame)
    piloto_frame.to_excel('precios.xlsx', index=False)

    # tr.rentabilidad_total( prices_frame['Rentabilidad']


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


def datosPiloto(piloto):
    base_dir = os.path.abspath('src\Formula1\html')

    # List of HTML files to process from https://www.f1-fansite.com/f1-results/f1-standings-2023-championship/
    html_results_files = [
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

    # Convert the HTML files list to full file paths
    html_results_files = [os.path.join(base_dir, file) for file in html_results_files]
    html_dates_files = [os.path.join(base_dir, file) for file in html_calendars_files]
    año = 2014
    for result_file_name, date_file_name in zip(html_results_files, html_dates_files):
        if os.path.exists(result_file_name):
            
            
            with open(result_file_name, 'r', encoding='utf-8') as file_results:
                html_content_results = file_results.read()
            
            with open(date_file_name, 'r', encoding='utf-8') as file_dates:
                html_content_dates = file_dates.read()



            soup_tabla_principal = BeautifulSoup(html_content_results, 'html.parser')
            soup_tabla_fechas = BeautifulSoup(html_content_dates, 'html.parser')

            # Buscar las filas de la tabla principal que contengan el texto específico
            # Extraer los datos de las filas y transponerlos en una columna
            texto_especifico = piloto # Por ejemplo, estamos buscando el nombre 'Jane'
            filas_con_texto = obtener_resultados_piloto(html_content_results, piloto)
            df = pd.DataFrame(filas_con_texto, columns=[texto_especifico])


            # Agregar las columnas adicionales para el encabezado de la tabla y las fechas asociadas
            encabezado_tabla = [th.get_text(strip=True) for th in soup_tabla_principal.find('tr').find_all('th')]
            fechas_asociadas = [''] * 3 + [fecha.get_text(strip=True) for fecha in soup_tabla_fechas.find_all('td', class_='msr_col2')]

            fechas_formateadas = []

            # Formatear las fechas en el formato deseado
            for fecha_texto in fechas_asociadas:
                if fecha_texto:
                    fechas_formateadas.append(convert_date(fecha_texto, año))
                else:
                    fechas_formateadas.append('')  # Mantener un espacio en blanco si no hay fecha

            df['Encabezado Tabla'] = encabezado_tabla
            df['Fecha Asociada'] = fechas_formateadas

            print(df)
            año = año + 1

def convert_date(fecha_texto, año):           

    mes, dia = fecha_texto.split()
    mes_numero = meses.get(mes)
    fecha_formateada = f"{año}-{mes_numero}-{dia.zfill(2)}"
    print(fecha_formateada)

    return fecha_formateada


