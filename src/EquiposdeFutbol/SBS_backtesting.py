                                                                    #SOLO LOS PARTIDOS DE LIGA


from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
import numpy as np


# Spanish month names
month_names = {
    'ENE': '01',
    'FEB': '02',
    'MAR': '03',
    'ABR': '04',
    'MAY': '05',
    'JUN': '06',
    'JUL': '07',
    'AGO': '08',
    'SEP': '09',
    'OCT': '10',
    'NOV': '11',
    'DIC': '12'
}


# Lista para almacenar los datos de todos los partidos
data = []


def backtesting(nombre:str, prices: list):
    # Crear un DataFrame de la lista prices
    ticks_frame = pd.DataFrame(prices, columns=['time', 'price'])
    # Convert 'time' from Unix timestamp to datetime
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
    # Extract the date
    ticks_frame['time'] = ticks_frame['time'].dt.date.astype(str)#conventirlo a string para poder comparar con el dataframe de los partidos
    print(ticks_frame)
    ticks_frame.to_excel('tick.xlsx', index=False)
    equipos_frame=datosEquipos()
    # Initialize a new column 'precio' in equipos_frame with NaN values
    equipos_frame['precio'] = np.nan
    # Iterate over the rows in equipos_frame
    for i, row in equipos_frame.iterrows(): 
        # Find the corresponding price in ticks_frame
        price = ticks_frame.loc[ticks_frame['time'] >= row['Fecha'], 'price'].first_valid_index()
        if price is not None:
            # If a price was found, update the 'precio' column in equipos_frame
            equipos_frame.at[i, 'precio'] = ticks_frame.loc[price, 'price']
    
    print(equipos_frame)
    equipos_frame.to_excel('precios.xlsx', index=False)

    # tr.rentabilidad_total( prices_frame['Rentabilidad']




def datosEquipos():
    #leerHtml()
    leerUrl()
    dataframe=crearDf()
    return dataframe
    

def leerHtml():#AQUI LE DEBERIA PASAR EL EQUIPO PARA ELEGIR LOS HTML QUE VOY A LEER ACTUALMENTE SOLO ESTAN LOS DEL MADRID

    # Define the base directory for the HTML files
    base_dir = os.path.abspath('src\EquiposdeFutbol\html')

    # List of HTML files to process
    html_files = [
        '2014-2015.html',
        '2015-2016.html',
        '2016-2017.html',
        '2017-2018.html',
        '2018-2019.html',
        '2019-2020.html',
        '2020-2021.html',
        '2021-2022.html'
    ]

    # Convert the HTML files list to full file paths
    html_files = [os.path.join(base_dir, file) for file in html_files]

    for file_name in html_files:
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                matches = soup.find_all('a', class_='match-link', attrs={'data-cy': 'match'})
                
                for match in matches:
                        competition_elem = match.find('div', class_='middle-info')
                    # if competition_elem and 'Primera División' in competition_elem.get_text(strip=True):
                        date_elem = match.find('div', class_='date-transform')
                        fecha_convertida=convert_date(date_elem.text.strip())
                        home_team_elem = match.find('div', class_='team-name', itemprop='name')
                        away_team_elems = match.find_all('div', class_='team-name', itemprop='name')
                        result_elem = match.find('div', class_='marker')
                        
                        if date_elem and home_team_elem and len(away_team_elems) > 1 and result_elem:
                            result_spans = result_elem.find_all('span')
                            if len(result_spans) == 3:  # Ensure there are two result spans and one dash
                                result_local = result_spans[1].text.strip()
                                result_visitante = result_spans[2].text.strip()
                                data.append([
                                    fecha_convertida.strip(),
                                    competition_elem.text.strip(),
                                    home_team_elem.text.strip(),
                                    away_team_elems[1].text.strip(),
                                    result_elem.text.strip(),
                                    result_local,
                                    result_visitante
                                ])
        else:
            print(f"File {file_name} does not exist.")


def leerUrl():
   
    url = "https://es.besoccer.com/equipo/partidos/real-madrid"
    response = requests.get(url)

    if response.status_code == 200:
        respuesta = response.text
        soup = BeautifulSoup(respuesta, 'html.parser')
        matches = soup.find_all('a', class_='match-link', attrs={'data-cy': 'match'})

            
        for match in matches:
                    competition_elem = match.find('div', class_='middle-info')
                # if competition_elem and 'Primera División' in competition_elem.get_text(strip=True):
                    date_elem = match.find('div', class_='date-transform')
                    fecha_convertida=convert_date(date_elem.text.strip())
                    home_team_elem = match.find('div', class_='team-name', itemprop='name')
                    away_team_elems = match.find_all('div', class_='team-name', itemprop='name')
                    result_elem = match.find('div', class_='marker')
                    
                    if date_elem and home_team_elem and len(away_team_elems) > 1 and result_elem:
                        result_spans = result_elem.find_all('span')
                        small_elem = result_elem.find('span', class_='small')
                        if small_elem is not None:#Para partidos con penaltis me quedo con el resultado de la tanda de penaltis
                            p1_elem = small_elem.find('span', class_='p1')
                            p2_elem = small_elem.find('span', class_='p2')
                            p1 = p1_elem.text.strip()
                            p2 = p2_elem.text.strip()
                            data.append([
                                fecha_convertida.strip(),
                                competition_elem.text.strip(),
                                home_team_elem.text.strip(),
                                away_team_elems[1].text.strip(),
                                result_elem.text.strip(),
                                p1,
                                p2
                            ])    
                        elif len(result_spans) == 3:  # Ensure there are two result spans and one dash
                            result_local = result_spans[1].text.strip()
                            result_visitante = result_spans[2].text.strip()
                            data.append([
                                fecha_convertida.strip(),
                                competition_elem.text.strip(),
                                home_team_elem.text.strip(),
                                away_team_elems[1].text.strip(),
                                result_elem.text.strip(),
                                result_local,
                                result_visitante
                            ])
                        else:
                            break  # Paro aqui porque el primera partido que no tenga 3 elementos sera el primero que se vaya a jugar despues porque tiene dentro de marker la hora del partido
                        

    else:
            print("Error al obtener la URL. Código de estado:", response.status_code)


def crearDf():
    
    # Convert data to a DataFrame
        df = pd.DataFrame(data, columns=['Fecha', 'Competición', 'Equipo Local', 'Equipo Visitante','Resultado', 'ResultadoLocal', 'ResultadoVisitante'])

    # Después de crear el DataFrame
        for index, row in df.iterrows():
            if row['Equipo Local'] == 'Real Madrid':
                if int(row['ResultadoLocal']) > int(row['ResultadoVisitante']):
                    df.loc[index, 'Decision'] = 'Ganado'
                elif int(row['ResultadoLocal']) < int(row['ResultadoVisitante']):
                    df.loc[index, 'Decision'] = 'Perdido'
                else:
                    df.loc[index, 'Decision'] = 'Empatado'
            else:
                if int(row['ResultadoVisitante']) > int(row['ResultadoLocal']):
                    df.loc[index, 'Decision'] = 'Ganado'
                elif int(row['ResultadoLocal']) > int(row['ResultadoVisitante']):
                    df.loc[index, 'Decision'] = 'Perdido'
                else:
                    df.loc[index, 'Decision'] = 'Empatado'
    # Guardar los datos en un archivo Excel
        # df.to_excel('de la url.xlsx', index=False)
        # Aquí puedes procesar los datos obtenidos de la URL
    
        return df
    




def convert_date(date_str):
    # print(date_str)
    day, month, year = date_str.split()
    month = month_names[month.upper()]
    return f"{year}-{month}-{day.zfill(2)}"


                                                                      # #TODOS LOS PARTIDOS

# import pandas as pd
# from bs4 import BeautifulSoup

# # Lista de archivos HTML a procesar
# html_files = [
#     'html/2014-2015.html',
#     'html/2015-2016.html',
#     'html/2016-2017.html',
#     'html/2017-2018.html',
#     'html/2018-2019.html',
#     'html/2019-2020.html',
#     'html/2020-2021.html',
#     'html/2021-2022.html',
#     'html/2022-2023.html'
# ]

# # Lista para almacenar los datos de todos los archivos
# data = []

# for file_name in html_files:
#     with open(file_name, 'r', encoding='utf-8') as file:
#         html_content = file.read()
#         soup = BeautifulSoup(html_content, 'html.parser')
#         matches = soup.find_all('a', class_='match-link', attrs={'data-cy': 'match'})
        
#         for match in matches:
#                 competition_elem = match.find('div', class_='middle-info')
#                 date_elem = match.find('div', class_='date-transform')
#                 home_team_elem = match.find('div', class_='team-name', itemprop='name')
#                 away_team_elems = match.find_all('div', class_='team-name', itemprop='name')
#                 result_elem = match.find('div', class_='marker')
                
#                 if date_elem and home_team_elem and len(away_team_elems) > 1 and result_elem:
#                     result_spans = result_elem.find_all('span')
#                     if len(result_spans) == 3:  # Ensure there are two result spans and one dash
#                         result_local = result_spans[1].text.strip()
#                         result_visitante = result_spans[2].text.strip()
#                         data.append([
#                             date_elem.text.strip(),
#                             competition_elem.text.strip(),
#                             home_team_elem.text.strip(),
#                             away_team_elems[1].text.strip(),
#                             result_elem.text.strip(),
#                             result_local,
#                             result_visitante
#                         ])

# # Crear un DataFrame con los datos combinados
# df = pd.DataFrame(data, columns=['Fecha', 'Competición', 'Equipo Local', 'Equipo Visitante','Resultado', 'ResultadoLocal', 'ResultadoVisitante'])

# # Después de crear el DataFrame
# for index, row in df.iterrows():
#     if row['Equipo Local'] == 'Real Madrid':
#         if int(row['ResultadoLocal']) > int(row['ResultadoVisitante']):
#             df.loc[index, 'Decision'] = 'Ganado'
#         elif int(row['ResultadoLocal']) < int(row['ResultadoVisitante']):
#             df.loc[index, 'Decision'] = 'Perdido'
#         else:
#             df.loc[index, 'Decision'] = 'Empatado'
#     else:
#         if int(row['ResultadoVisitante']) > int(row['ResultadoLocal']):
#             df.loc[index, 'Decision'] = 'Ganado'
#         elif int(row['ResultadoLocal']) > int(row['ResultadoVisitante']):
#             df.loc[index, 'Decision'] = 'Perdido'
#         else:
#             df.loc[index, 'Decision'] = 'Empatado'



# # Guardar los datos en un archivo Excel
# df.to_excel('real_madrid_matches_combined.xlsx', index=False)