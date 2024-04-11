                                                                    #SOLO LOS PARTIDOS DE LIGA


from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
import numpy as np
import tick_reader as tr

class SBSBacktesting:
        
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

    ligas = {
        'La Liga': ['Real Madrid', 'Barcelona'],
        'Premier League': [ 'Arsenal'],
        'Bundesliga': ['Bayern Munich']
    }

    pais = {
        'ACS': 'spain',
        'ADS': 'united states',
        'NKE': 'united states',
        # 'SPOT': 'united states',
        'DTEGn': 'germany',
        'ALVG': 'germany',

    }

    acciones = {
        'Real Madrid': ['ACS', 'ADS'],
        'Barcelona': [ 'NKE'],
        'Arsenal': ['ADS'],
        'Bayern Munich': ['DTEGn', 'ALVG'],
    }

    urls_equipos = {
        'Real Madrid': 'https://es.besoccer.com/equipo/partidos/real-madrid',
        'Barcelona': 'https://es.besoccer.com/equipo/partidos/barcelona',
        'Arsenal': 'https://es.besoccer.com/equipo/partidos/arsenal',
        'Bayern Munich': 'https://es.besoccer.com/equipo/partidos/bayern-munchen',
    }

    def __init__(self):
        # Inicializa las variables que necesites, como rentabilidad_total
        self.rentabilidad_total = 0
        self.data = []
        self.compras = []


    def backtesting(self,nombre:str, ticks: list,inicio: str, fin: str,url,combo_comprar:str,combo_vender:str,equipos_txt:str):
        
        
        equipos_frame=self.datosEquipos(ticks,inicio, fin,url,equipos_txt) 
        # Initialize a new column 'precio' in equipos_frame with NaN values
        
        # equipos_frame['Fecha'] = ticks_frame['Fecha'].dt.date#solo la fecha no la hora
        posicion_abierta=False #comprobar si hay alguna posicion abierta para poder realziar ventas 
        decisiones = []
        rentabilidad=[]


        for index, row in equipos_frame.iterrows():
            resultado = row['Resultado']
            precioCompra= row['Precio']

            # Comparar las medias móviles
            if resultado == combo_vender and posicion_abierta==True:
                decisiones.append("-1")#VENDO
                posicion_abierta=False
                rentabilidad.append(tr.calcular_rentabilidad(self.compras,row['Precio']))
                self.compras.clear()
            elif len(self.compras) < 10 and resultado == combo_comprar :  
                decisiones.append("1")#COMPRO
                rentabilidad.append(None)
                self.compras.append(precioCompra)
                posicion_abierta=True
            else:
                decisiones.append("NO SE REALIZA OPERACION")#COMPRO
                rentabilidad.append(None)

        # Agregar la lista de decisiones como una nueva columna al DataFrame
        equipos_frame['Decision'] = decisiones
        equipos_frame['Rentabilidad']= rentabilidad
    
        print(equipos_frame)
        
        equipos_frame.to_excel('precios.xlsx', index=False)

        rentabilidad_total=tr.rentabilidad_total(equipos_frame['Rentabilidad'])
        self.data.clear()

    def obtener_rentabilidad_total(self):
        return self.rentabilidad_total


    def datosEquipos(self,ticks:list,inicio: str, fin: str, url:str,equipos_txt:str):
        # leerHtml(equipos_txt)
        self.leerUrl(url)
        print(self.data)
        dataframe=self.crearDf(ticks,inicio, fin,equipos_txt)
        return dataframe



    def crearDf(self,ticks:list,inicio: str, fin: str,equipos_txt:str):

        # Crear un DataFrame de la lista prices
        ticks_frame = pd.DataFrame(ticks, columns=['time', 'price'])
        # Convert 'time' from Unix timestamp to datetime
        print(ticks_frame)
        
        ticks_frame.to_excel('tick.xlsx', index=False)
        # Convert data to a DataFrame
        equipos_frame = pd.DataFrame(self.data, columns=['Fecha', 'Competición', 'Equipo Local', 'Equipo Visitante','Marcador', 'ResultadoLocal', 'ResultadoVisitante'])

        # Convertir la columna 'Fecha' a datetime
        equipos_frame['Fecha'] = pd.to_datetime(equipos_frame['Fecha'])

        # Filtrar el DataFrame basado en las fechas de inicio y fin
        equipos_frame = equipos_frame[equipos_frame['Fecha'].between(inicio, fin)]
        equipos_frame['Precio'] = np.nan

        for i, row in equipos_frame.iterrows(): 
            price = ticks_frame.loc[ticks_frame['time'] >= row['Fecha'], 'price'].first_valid_index()
            if price is not None:
                # If a price was found, update the 'precio' column in equipos_frame
                equipos_frame.at[i, 'Precio'] = float(ticks_frame.loc[price, 'price'])
            #Asignar el Resultado a cada partido
            if row['Equipo Local'] == equipos_txt:
                if int(row['ResultadoLocal']) > int(row['ResultadoVisitante']):
                    equipos_frame.loc[i, 'Resultado'] = 'Ganado'
                elif int(row['ResultadoLocal']) < int(row['ResultadoVisitante']):
                    equipos_frame.loc[i, 'Resultado'] = 'Perdido'
                else:
                    equipos_frame.loc[i, 'Resultado'] = 'Empatado'
            else:
                if int(row['ResultadoVisitante']) > int(row['ResultadoLocal']):
                    equipos_frame.loc[i, 'Resultado'] = 'Ganado'
                elif int(row['ResultadoLocal']) > int(row['ResultadoVisitante']):
                    equipos_frame.loc[i, 'Resultado'] = 'Perdido'
                else:
                    equipos_frame.loc[i, 'Resultado'] = 'Empatado'
            
        # Guardar los datos en un archivo Excel
        # df.to_excel('de la url.xlsx', index=False)
        # Aquí puedes procesar los datos obtenidos de la URL

        return equipos_frame
        




    def leerUrl(self,url):
    
        print(url)
        response = requests.get(url)

        if response.status_code == 200:
            respuesta = response.text
            soup = BeautifulSoup(respuesta, 'html.parser')
            matches = soup.find_all('a', class_='match-link', attrs={'data-cy': 'match'})

                
            for match in matches:
                        competition_elem = match.find('div', class_='middle-info')
                    # if competition_elem and 'Primera División' in competition_elem.get_text(strip=True):
                        date_elem = match.find('div', class_='date-transform')
                        fecha_convertida=self.convert_date(date_elem.text.strip())
                        home_team_elem = match.find('div', class_='team-name', itemprop='name')
                        away_team_elems = match.find_all('div', class_='team-name', itemprop='name')
                        result_elem = match.find('div', class_='marker')
                        aplazado_elem = result_elem.find('p', class_='match_hour match-apl')
                        
                        
                        if date_elem and home_team_elem and len(away_team_elems) > 1 and result_elem and aplazado_elem is None:
                            
                            result_spans = result_elem.find_all('span')
                            small_elem = result_elem.find('span', class_='small')
                            

                            if small_elem is not None:#Para partidos con penaltis me quedo con el resultado de la tanda de penaltis
                                p1_elem = small_elem.find('span', class_='p1')
                                p2_elem = small_elem.find('span', class_='p2')
                                p1 = p1_elem.text.strip()
                                p2 = p2_elem.text.strip()
                                self.data.append([
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
                                self.data.append([
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









    def cargar_html(equipo):
        # Define the base directory for the HTML files
        base_dir = os.path.abspath('src\EquiposdeFutbol\html')

        if equipo == 'Real Madrid':
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
        elif equipo == 'Barcelona':
            # List of HTML files to process
            html_files = [
                '2014-2015_Barcelona.html',
                '2015-2016_Barcelona.html',
                '2016-2017_Barcelona.html',
                '2017-2018_Barcelona.html',
                '2018-2019_Barcelona.html',
                '2019-2020_Barcelona.html',
                '2020-2021_Barcelona.html',
                '2021-2022_Barcelona.html'
            ]

        # Convert the HTML files list to full file paths
        html_files = [os.path.join(base_dir, file) for file in html_files]

        return html_files


    def leerHtml(self,equipo):#AQUI LE DEBERIA PASAR EL EQUIPO PARA ELEGIR LOS HTML QUE VOY A LEER ACTUALMENTE SOLO ESTAN LOS DEL MADRID

    

        html_files = self.cargar_html(equipo)

        
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
                        fecha_convertida=self.convert_date(date_elem.text.strip())
                        home_team_elem = match.find('div', class_='team-name', itemprop='name')
                        away_team_elems = match.find_all('div', class_='team-name', itemprop='name')
                        result_elem = match.find('div', class_='marker')
                        aplazado_elem = result_elem.find('p', class_='match_hour match-apl')
                        
                        
                        if date_elem and home_team_elem and len(away_team_elems) > 1 and result_elem and aplazado_elem is None:
                            
                            result_spans = result_elem.find_all('span')
                            small_elem = result_elem.find('span', class_='small')

                            if small_elem is not None:#Para partidos con penaltis me quedo con el resultado de la tanda de penaltis
                                p1_elem = small_elem.find('span', class_='p1')
                                p2_elem = small_elem.find('span', class_='p2')
                                p1 = p1_elem.text.strip()
                                p2 = p2_elem.text.strip()
                                self.data.append([
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
                                self.data.append([
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
                print(f"File {file_name} does not exist.")




    def convert_date(self,date_str):
        # print(date_str)
        day, month, year = date_str.split()
        month = self.month_names[month.upper()]
        return f"{year}-{month}-{day.zfill(2)}"



    def check_buy() -> bool:
        return False
    
        # if CUR_SIGNAL.iloc[-1] >= CUR_MACD.iloc[-1] and CUR_RSI.iloc[-1] < 35 :
        #     return True
        # return False


    def check_sell() -> bool:#ñle tendre que pasar el valor al que la he comprado cada una de las buy
        
        return False

        # if CUR_SIGNAL.iloc[-1] <= CUR_MACD.iloc[-1] and CUR_RSI.iloc[-1] > 65:
        #     return True
        # return False



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