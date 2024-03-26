#En directo de la url

import pandas as pd
from bs4 import BeautifulSoup

import requests

url = "https://es.besoccer.com/equipo/partidos/real-madrid"
response = requests.get(url)

# Lista para almacenar los datos de todos los archivos
data = []

if response.status_code == 200:
    respuesta = response.text
    soup = BeautifulSoup(respuesta, 'html.parser')
    matches = soup.find_all('a', class_='match-link', attrs={'data-cy': 'match'})

        
    for match in matches:
            competition_elem = match.find('div', class_='middle-info')
            if competition_elem and 'Primera División' in competition_elem.get_text(strip=True):
                date_elem = match.find('div', class_='date-transform')
                home_team_elem = match.find('div', class_='team-name', itemprop='name')
                away_team_elems = match.find_all('div', class_='team-name', itemprop='name')
                result_elem = match.find('div', class_='marker')
                
                if date_elem and home_team_elem and len(away_team_elems) > 1 and result_elem:
                    result_spans = result_elem.find_all('span')
                    if len(result_spans) == 3:  # Ensure there are two result spans and one dash
                        result_local = result_spans[1].text.strip()
                        result_visitante = result_spans[2].text.strip()
                        data.append([
                            date_elem.text.strip(),
                            competition_elem.text.strip(),
                            home_team_elem.text.strip(),
                            away_team_elems[1].text.strip(),
                            result_elem.text.strip(),
                            result_local,
                            result_visitante
                        ])

# Crear un DataFrame con los datos combinados
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
    df.to_excel('de la url.xlsx', index=False)
    # Aquí puedes procesar los datos obtenidos de la URL
else:
    print("Error al obtener la URL. Código de estado:", response.status_code)
