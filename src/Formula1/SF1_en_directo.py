#En directo de la url

import pandas as pd
from bs4 import BeautifulSoup

import requests

url = "https://www.f1-fansite.com/f1-results/f1-standings-2024-championship/"


response = requests.get(url)


# Lista para almacenar los datos de todos los archivos
data = []

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


    # Agregar las columnas adicionales para el encabezado de la tabla y las fechas asociadas
    tabla_fechas = soup_tabla_fechas.find('table', class_="motor-sport-results msr_season_summary tablesorter")
    if tabla_fechas:
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

    df = pd.concat([df, nuevo_df], ignore_index=True)


    df['Fecha'] = pd.to_datetime(df['Fecha'])
    # Initialize a new column 'precio' in piloto_frame with NaN values
    df['Precio'] = np.nan
                    
else:
    print("Error al obtener la URL. Código de estado:", response.status_code) 


 