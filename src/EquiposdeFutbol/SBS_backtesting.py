                                                                    #SOLO LOS PARTIDOS DE LIGA


from bs4 import BeautifulSoup
import pandas as pd

# Lista de archivos HTML a procesar
html_files = [
    'html/2014-2015.html',
    'html/2015-2016.html',
    'html/2016-2017.html',
    'html/2017-2018.html',
    'html/2018-2019.html',
    'html/2019-2020.html',
    'html/2020-2021.html',
    'html/2021-2022.html',
    'html/2022-2023.html'
]

# Lista para almacenar los datos de todos los archivos
data = []

for file_name in html_files:
    with open(file_name, 'r', encoding='utf-8') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
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
df.to_excel('real_madrid_primera_division_matches_combined.xlsx', index=False)


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