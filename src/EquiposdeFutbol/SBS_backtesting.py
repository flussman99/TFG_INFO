                                                                    #SOLO LOS PARTIDOS DE LIGA


from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
import numpy as np
import tick_reader as tr
import MetaTrader5 as mt5
from typing import Tuple
from config import API_KEY 

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
    'La Liga': ['Real Madrid', 'Barcelona', 'Atletico de Madrid','Valencia'],
    'Premier League': [ 'Arsenal','Manchester United','Manchester City','Chelsea','Liverpool'],
    'Bundesliga': ['Bayern Munich','Borussia Dortmund','RB Leipzig','Bayer Leverkusen'],
    'Serie A': ['Juventus','Roma','Napoles','AC Milan','Inter de Milan'],
    'Ligue 1':['PSG','Olympique Lyon','Olympique Marsella']
}


pais = {
        'ACS': 'spain',
        'ADS': 'united states',
        'NKE': 'united states',
        # 'SPOT': 'united states',
        'DTEGn': 'germany',
        'ALVG': 'germany',
        'KO' : 'united states',
        'DXC': 'united states',
        'EA': 'united states',
        'TRVG':'united states',
        'EVKn': 'germany',
        'VOWG':'germany',
        'BAYGn':'germany',
        'TM': 'united states',
        'EBAY':'united states',
        'BMWG': 'germany',
        'MCD': 'united states',
        'ORAN':'france',
        'STAN': 'united kingdom'

} 

acronimo_acciones_api = {
    'Grupo ACS(ACS)': 'ACS',
    'Adidas(ADS)': 'ADS',
    'Nike(NKE)': 'NKE',
    'Deutsche Bank(DTE)': 'DTEGn',#este es DTE en metatrader
    'Allianz(ALV)': 'ALVG',#ALV en metatrader
    'Coca cola(KO)': 'KO',
    'DXC Technology(DXC)': 'DXC',
    'Standar Chartered(STAN)': 'STAN',
    'Electronic Arts(EA)': 'EA',
    'Trivago(TRVG)': 'TRVG',
    'Evonik Industries(EVK)': 'EVKn',#EVK en metatrader
    'Volkswagen(VOW3)': 'VOWG',#VOW3 en metatrader
    'Bayer AG(BAYN)': 'BAYGn',#BAYN en metatrader
    'Toyota(TM)': 'TM',
    'Ebay Inc(EBAY)': 'EBAY',
    'Bayerische Motoren Werke(BMW)': 'BMWG',#BMW en metatrader
    'McDonalds(MCD)': 'MCD',
    'Orange(ORA)': 'ORAN',
}

acronimo_acciones_mt5 = {
    'Grupo ACS(ACS)': 'ACS.MAD',
    'Adidas(ADS)': 'ADS.ETR',
    'Nike(NKE)': 'NKE.NYSE',
    'Deutsche Bank(DTE)': 'DTE.ETR',#este es DTE en metatrader
    'Allianz(ALV)': 'ALV.ETR',#ALV en metatrader
    'Coca cola(KO)': 'KO.NYSE',
    'DXC Technology(DXC)': 'DXC.NYSE',
    'Standar Chartered(STAN)': 'STAN.LSE',
    'Electronic Arts(EA)': 'EA.NAS',
    'Trivago(TRVG)': 'TRVG.NAS',
    'Evonik Industries(EVK)': 'EVK.ETR',#EVK en metatrader
    'Volkswagen(VOW3)': 'VOW3.ETR',#VOW3 en metatrader
    'Bayer AG(BAYN)': 'BAYN.ETR',#BAYN en metatrader
    'Toyota(TM)': 'TM.NYSE',
    'Ebay Inc(EBAY)': 'EBAY.NAS',
    'Bayerische Motoren Werke(BMW)': 'BMW.ETR',#BMW en metatrader
    'McDonalds(MCD)': 'MCD.NYSE',
    'Orange(ORAN)': 'ORA.PAR',
}


acciones = {
    'Real Madrid': ['Adidas(ADS)','Grupo ACS(ACS)'],
    'Barcelona': [ 'Nike(NKE)'],
    'Arsenal': ['Adidas(ADS)'],
    'Bayern Munich': ['Deutsche Bank(DTE)', 'Allianz(ALV)'],
    'Atletico de Madrid':['Nike(NKE)'],
    'Valencia': ['Coca cola(KO)'],
    'Manchester United':['DXC Technology(DXC)'],
    'Liverpool': ['Standar Chartered(STAN)'],
    'Manchester City': ['Electronic Arts(EA)'],
    'Chelsea': ['Trivago(TRVG)'],
    'Borussia Dortmund':['Evonik Industries(EVK)'],
    'RB Leipzig': ['Volkswagen(VOW3)'],
    'Bayer Leverkusen':['Bayer AG(BAYN)'],
    'Juventus':['Adidas(ADS)'],
    'Roma': ['Toyota(TM)'],
    'Napoles': ['Ebay Inc(EBAY)'],
    'AC Milan': ['Bayerische Motoren Werke(BMW)'],
    'Inter de Milan': ['Ebay Inc(EBAY)','Nike(NKE)'],
    'PSG':['Nike(NKE)','McDonalds(MCD)'],
    'Olympique Lyon': ['Adidas(ADS)'],
    'Olympique Marsella': ['Orange(ORAN)'],
}

urls_equipos = {
    'Real Madrid': 'https://es.besoccer.com/equipo/partidos/real-madrid',
    'Barcelona': 'https://es.besoccer.com/equipo/partidos/barcelona',
    'Arsenal': 'https://es.besoccer.com/equipo/partidos/arsenal',
    'Bayern Munich': 'https://es.besoccer.com/equipo/partidos/bayern-munchen',
    'Atletico de Madrid': 'https://es.besoccer.com/equipo/partidos/atletico-madrid',
    'Valencia': 'https://es.besoccer.com/equipo/partidos/valencia-cf',
    'Manchester United': 'https://es.besoccer.com/equipo/partidos/manchester-united-fc',
    'Manchester City': 'https://es.besoccer.com/equipo/partidos/manchester-city-fc',
    'Liverpool': 'https://es.besoccer.com/equipo/partidos/liverpool',
    'Chelsea': 'https://es.besoccer.com/equipo/partidos/chelsea-fc',
    'Borussia Dortmund': 'https://es.besoccer.com/equipo/partidos/borussia-dortmund',
    'RB Leipzig': 'https://es.besoccer.com/equipo/partidos/rb-leipzig',
    'Bayer Leverkusen': 'https://es.besoccer.com/equipo/partidos/bayer-leverkusen',
    'Juventus': 'https://es.besoccer.com/equipo/partidos/juventus-fc',
    'Roma': 'https://es.besoccer.com/equipo/partidos/roma',
    'Napoles': 'https://es.besoccer.com/equipo/partidos/napoli',
    'AC Milan': 'https://es.besoccer.com/equipo/partidos/milan',
    'Inter de Milan': 'https://es.besoccer.com/equipo/partidos/internazionale',
    'PSG': 'https://es.besoccer.com/equipo/partidos/paris-saint-germain-fc',
    'Olympique Lyon': 'https://es.besoccer.com/equipo/partidos/olympique-lyonnais',
    'Olympique Marsella': 'https://es.besoccer.com/equipo/partidos/olympique-marsella'
}

imagenes_equipos={
    'Real Madrid': 'src/imagenes/Futbol/real-madrid-icono.png',
    'Barcelona': 'src/imagenes/Futbol/barcelona-icono.png',
    'Arsenal': 'src/imagenes/Futbol/arsenal-icono.png',
    'Bayern Munich': 'src/imagenes/Futbol/munich-icono.png',
    'Atletico de Madrid': 'src/imagenes/Futbol/atletico-de-madrid-icono.png',
    'Valencia': 'src/imagenes/Futbol/valencia-icono.png',
    'Manchester United': 'src/imagenes/Futbol/united-icono.png',
    'Manchester City': 'src/imagenes/Futbol/city-icono.png',
    'Liverpool': 'src/imagenes/Futbol/liverpool-icono.png',
    'Chelsea': 'src/imagenes/Futbol/chelsea-icono.png',
    'Borussia Dortmund': 'src/imagenes/Futbol/borussia-icono.png',
    'RB Leipzig': 'src/imagenes/Futbol/leipzig-icono.png',
    'Bayer Leverkusen': 'src/imagenes/Futbol/leverkusen-icono.png',
    'Juventus': 'src/imagenes/Futbol/juventus-icono.png',
    'Roma': 'src/imagenes/Futbol/roma-icono.png',
    'Napoles': 'src/imagenes/Futbol/napoles-icono.png',
    'AC Milan': 'src/imagenes/Futbol/milan-icono.png',
    'Inter de Milan': 'src/imagenes/Futbol/inter-icono.png',
    'PSG': 'src/imagenes/Futbol/psg-icono.png',
    'Olympique Lyon': 'src/imagenes/Futbol/lyon-icono.png',
    'Olympique Marsella': 'src/imagenes/Futbol/marsella-icono.png'
}

imagenes_ligas={
    'La Liga': "src/imagenes/Futbol/la-liga-icono.png",
    'Premier League': 'src/imagenes/Futbol/premier-icono.png',
    'Ligue 1': 'src/imagenes/Futbol/ligue1-icono.png',
    'Serie A': 'src/imagenes/Futbol/serieA-icono.png',
    'Bundesliga': 'src/imagenes/Futbol/bundesliga-icono.png'
}

data=[]#guardo los partidos
compras=[]

FECHA_ULTIMO_PARTIDO=None
COMBO_COMPRAR=None
COMBO_VENDER=None
RESULTADO_ULTIMO_PARTIDO=None
NUEVO_PARTIDO=False
FRAMEDIRECTO = pd.DataFrame(columns=['Fecha', 'Competición', 'Equipo Local', 'Equipo Visitante','Marcador'])


def backtesting(ticks: list,inicio: str, fin: str,url,combo_comprar:str,combo_vender:str,equipos_txt:str):
    
    
    equipos_frame=datosEquipos(ticks,inicio, fin,url,equipos_txt) 
    # Initialize a new column 'precio' in equipos_frame with NaN values
    
    # equipos_frame['Fecha'] = ticks_frame['Fecha'].dt.date#solo la fecha no la hora
    posicion_abierta=False #comprobar si hay alguna posicion abierta para poder realziar ventas 
    decisiones = []
    rentabilidad=[]


    for index, row in equipos_frame.iterrows():
        resultado = row['Resultado']
        precioCompra= row['Precio']

        # Comparar las medias móviles
        if comprobar(resultado,combo_vender) and posicion_abierta == True:
            decisiones.append("Venta")#VENDO
            posicion_abierta=False
            rentabilidad.append(tr.calcular_rentabilidad(compras,row['Precio']))
            compras.clear()
        elif len(compras) < 10 and comprobar(resultado,combo_comprar) :  
            decisiones.append("Compra")#COMPRO
            rentabilidad.append(None)
            compras.append(precioCompra)
            posicion_abierta=True
        else:
            decisiones.append("NO SE REALIZA OPERACION")#COMPRO
            rentabilidad.append(None)
    compras.clear()
    # Agregar la lista de decisiones como una nueva columna al DataFrame
    equipos_frame['Decision'] = decisiones
    equipos_frame['Rentabilidad']= rentabilidad
    print("frame futbol",equipos_frame)
    return equipos_frame
    
def comprobar(resultado,operar):
    
    if "/" in operar:
        operar_values = operar.split("/")
        if resultado == operar_values[0] or resultado == operar_values[1]:
            return True
    else:
        if resultado == operar:
            return True

    return False



def datosEquipos(ticks:list,inicio: str, fin: str, url:str,equipos_txt:str):

    leerHtml(equipos_txt)
    leerUrl(url)
    print(data)
    dataframe=crearDf(ticks,inicio, fin,equipos_txt)

    return dataframe


def crearDf(ticks:list,inicio: str, fin: str,equipos_txt:str):

    # Crear un DataFrame de la lista prices
    ticks_frame = pd.DataFrame(ticks, columns=['time', 'price'])
    # Convert 'time' from Unix timestamp to datetime
    print(ticks_frame)
    
    ticks_frame.to_excel('tick.xlsx', index=False)
    # Convert data to a DataFrame
    equipos_frame = pd.DataFrame(data, columns=['Fecha', 'Competición', 'Equipo Local', 'Equipo Visitante','Marcador', 'ResultadoLocal', 'ResultadoVisitante'])
    data.clear()#ya lo tengo que limpiar
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
    equipos_frame = equipos_frame.drop(columns=['ResultadoLocal', 'ResultadoVisitante'])

    return equipos_frame
    

def ultimoPartido(equipos_txt:str,url,cola):
    global FECHA_ULTIMO_PARTIDO,RESULTADO_ULTIMO_PARTIDO,NUEVO_PARTIDO,FRAMEDIRECTO

    leerUrl(url)#cojo los partidos
    equipos_frame = pd.DataFrame(data, columns=['Fecha', 'Competición', 'Equipo Local', 'Equipo Visitante','Marcador', 'ResultadoLocal', 'ResultadoVisitante'])
    # equipos_frame['Fecha'] = pd.to_datetime(equipos_frame['Fecha'])
    data.clear()#ya lo tengo que limpiar
    last_row = equipos_frame.iloc[-1]
    if(FECHA_ULTIMO_PARTIDO is None or last_row['Fecha']!=FECHA_ULTIMO_PARTIDO):
        FECHA_ULTIMO_PARTIDO = last_row['Fecha']
        print(FECHA_ULTIMO_PARTIDO)
        # Asignar el Resultado a cada partido
        if last_row['Equipo Local'] == equipos_txt:
            if int(last_row['ResultadoLocal']) > int(last_row['ResultadoVisitante']):
                equipos_frame.loc[equipos_frame.tail(1).index, 'Resultado'] = 'Ganado'
            elif int(last_row['ResultadoLocal']) < int(last_row['ResultadoVisitante']):
                equipos_frame.loc[equipos_frame.tail(1).index, 'Resultado'] = 'Perdido'
            else:
                equipos_frame.loc[equipos_frame.tail(1).index, 'Resultado'] = 'Empatado'
        else:
            if int(last_row['ResultadoVisitante']) > int(last_row['ResultadoLocal']):
                equipos_frame.loc[equipos_frame.tail(1).index, 'Resultado'] = 'Ganado'
            elif int(last_row['ResultadoLocal']) > int(last_row['ResultadoVisitante']):
                equipos_frame.loc[equipos_frame.tail(1).index, 'Resultado'] = 'Perdido'
            else:
                equipos_frame.loc[equipos_frame.tail(1).index, 'Resultado'] = 'Empatado'
        
        RESULTADO_ULTIMO_PARTIDO = equipos_frame.at[equipos_frame.index[-1], 'Resultado']
        print(RESULTADO_ULTIMO_PARTIDO)
        filaAdd=equipos_frame.iloc[[-1]].drop(['ResultadoLocal', 'ResultadoVisitante'], axis=1)
        FRAMEDIRECTO = pd.concat([FRAMEDIRECTO,  filaAdd], ignore_index=True)#GUARDO EL ULTIMO sin las columnas que no me interesan
        print(FRAMEDIRECTO)
        cola.put(FRAMEDIRECTO)
        NUEVO_PARTIDO = True
    else:
        print("No hay partido nuevo")
    
def parar_partidos(self):
    global FRAMEDIRECTO
    frame=FRAMEDIRECTO
    return frame

def inicializar_variables(combo_comprar,comobo_vender):
    global COMBO_COMPRAR,COMBO_VENDER,FECHA_ULTIMO_PARTIDO,RESULTADO_ULTIMO_PARTIDO,NUEVO_PARTIDO,FRAMEDIRECTO
    #van a ser lo que haya establecido el usuario de orgne
    COMBO_COMPRAR=combo_comprar
    COMBO_VENDER=comobo_vender
    #inicializao las variables cada vez que le pulso el boton de ticks en directo para que se reinicie todo y no se qued con los valores anteriores
    FECHA_ULTIMO_PARTIDO=None
    RESULTADO_ULTIMO_PARTIDO=None
    NUEVO_PARTIDO=False
    FRAMEDIRECTO = pd.DataFrame(columns=['Fecha', 'Competición', 'Equipo Local', 'Equipo Visitante','Marcador'])


def thread_futbol(pill2kill,trading_data: dict, equipos_txt,url,combo_comprar,comobo_vender,cola):

    inicializar_variables(combo_comprar,comobo_vender)
    ultimoPartido(equipos_txt,url,cola)

    while not pill2kill.wait(20):
        ultimoPartido(equipos_txt,url,cola)
        print("Checking matches...")
        print(FRAMEDIRECTO)


def check_buy() -> Tuple[bool, bool]:
    global RESULTADO_ULTIMO_PARTIDO,NUEVO_PARTIDO,COMBO_COMPRAR
    print(NUEVO_PARTIDO)
    if(NUEVO_PARTIDO):#Hay nuevo partido
        if(comprobar(RESULTADO_ULTIMO_PARTIDO,COMBO_COMPRAR)):#El resultado del partido coincide con la eleccion del usuario
            NUEVO_PARTIDO=False #Ya he comprobado ese resultado con el mercado y he realizado una inversion con ese partido
            return True, True
        else:#El resultado del partido no coincide con la eleccion del usuario
            NUEVO_PARTIDO=False#Ya he comprobado ese resultado con el mercado y he realizado una inversion con ese partido
            return True, False
    else:
        return False, False#no hay partido nuevo y no tengo que comprobar nada

def check_sell() -> bool:#en el check buy returneo si coincide con valor de venta el nuevo partido lo trato con check buy
    global RESULTADO_ULTIMO_PARTIDO,COMBO_COMPRAR
    if(comprobar(RESULTADO_ULTIMO_PARTIDO,COMBO_VENDER)):#El resultado del partido coincide con la eleccion del usuario
        return True
    else:#El resultado del partido no coincide con la eleccion del usuario
        return False
   
def leerUrl(url):

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
                    fecha_convertida=convert_date(date_elem.text.strip())
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
        
    elif equipo == 'Atletico de Madrid':
        # List of HTML files to process
        html_files = [
            '2014-2015_Atletico.html',
            '2015-2016_Atletico.html',
            '2016-2017_Atletico.html',
            '2017-2018_Atletico.html',
            '2018-2019_Atletico.html',
            '2019-2020_Atletico.html',
            '2020-2021_Atletico.html',
            '2021-2022_Atletico.html'
        ]

    elif equipo == 'Valencia':
        # List of HTML files to process
        html_files = [
            '2014-2015_Valencia.html',
            '2015-2016_Valencia.html',
            '2016-2017_Valencia.html',
            '2017-2018_Valencia.html',
            '2018-2019_Valencia.html',
            '2019-2020_Valencia.html',
            '2020-2021_Valencia.html',
            '2021-2022_Valencia.html'
        ]
    elif equipo == 'Arsenal':
        # List of HTML files to process
        html_files = [
            '2014-2015_Arsenal.html',
            '2015-2016_Arsenal.html',
            '2016-2017_Arsenal.html',
            '2017-2018_Arsenal.html',
            '2018-2019_Arsenal.html',
            '2019-2020_Arsenal.html',
            '2020-2021_Arsenal.html',
            '2021-2022_Arsenal.html'
        ]   

    elif equipo == 'Manchester United':
        # List of HTML files to process
        html_files = [
            '2014-2015_United.html',
            '2015-2016_United.html',
            '2016-2017_United.html',
            '2017-2018_United.html',
            '2018-2019_United.html',
            '2019-2020_United.html',
            '2020-2021_United.html',
            '2021-2022_United.html'
        ]    

    elif equipo == 'Manchester City':
        # List of HTML files to process
        html_files = [
            '2014-2015_City.html',
            '2015-2016_City.html',
            '2016-2017_City.html',
            '2017-2018_City.html',
            '2018-2019_City.html',
            '2019-2020_City.html',
            '2020-2021_City.html',
            '2021-2022_City.html'
        ]

    elif equipo == 'Chelsea':
        # List of HTML files to process
        html_files = [
            '2014-2015_Chelsea.html',
            '2015-2016_Chelsea.html',
            '2016-2017_Chelsea.html',
            '2017-2018_Chelsea.html',
            '2018-2019_Chelsea.html',
            '2019-2020_Chelsea.html',
            '2020-2021_Chelsea.html',
            '2021-2022_Chelsea.html'
        ]  

    elif equipo == 'Liverpool':
        # List of HTML files to process
        html_files = [
            '2014-2015_Liverpool.html',
            '2015-2016_Liverpool.html',
            '2016-2017_Liverpool.html',
            '2017-2018_Liverpool.html',
            '2018-2019_Liverpool.html',
            '2019-2020_Liverpool.html',
            '2020-2021_Liverpool.html',
            '2021-2022_Liverpool.html'
        ]             
    elif equipo == 'Bayern Munich':
        # List of HTML files to process
        html_files = [
            '2014-2015_Bayern.html',
            '2015-2016_Bayern.html',
            '2016-2017_Bayern.html',
            '2017-2018_Bayern.html',
            '2018-2019_Bayern.html',
            '2019-2020_Bayern.html',
            '2020-2021_Bayern.html',
            '2021-2022_Bayern.html'
        ] 

    elif equipo == 'Borussia Dortmund':
        # List of HTML files to process
        html_files = [
            '2014-2015_Borussia.html',
            '2015-2016_Borussia.html',
            '2016-2017_Borussia.html',
            '2017-2018_Borussia.html',
            '2018-2019_Borussia.html',
            '2019-2020_Borussia.html',
            '2020-2021_Borussia.html',
            '2021-2022_Borussia.html'
        ] 

    elif equipo == 'RB Leipzig':
        # List of HTML files to process
        html_files = [
            '2014-2015_RB.html',
            '2015-2016_RB.html',
            '2016-2017_RB.html',
            '2017-2018_RB.html',
            '2018-2019_RB.html',
            '2019-2020_RB.html',
            '2020-2021_RB.html',
            '2021-2022_RB.html'
        ] 

    elif equipo == 'Bayern Leverkusen':
        # List of HTML files to process
        html_files = [
            '2014-2015_Leverkusen.html',
            '2015-2016_Leverkusen.html',
            '2016-2017_Leverkusen.html',
            '2017-2018_Leverkusen.html',
            '2018-2019_Leverkusen.html',
            '2019-2020_Leverkusen.html',
            '2020-2021_Leverkusen.html',
            '2021-2022_Leverkusen.html'
        ] 
    elif equipo == 'PSG':
        # List of HTML files to process
        html_files = [
            '2014-2015_PSG.html',
            '2015-2016_PSG.html',
            '2016-2017_PSG.html',
            '2017-2018_PSG.html',
            '2018-2019_PSG.html',
            '2019-2020_PSG.html',
            '2020-2021_PSG.html',
            '2021-2022_PSG.html'
        ]

    elif equipo == 'Olympique Lyon':
        # List of HTML files to process
        html_files = [
            '2014-2015_OL.html',
            '2015-2016_OL.html',
            '2016-2017_OL.html',
            '2017-2018_OL.html',
            '2018-2019_OL.html',
            '2019-2020_OL.html',
            '2020-2021_OL.html',
            '2021-2022_OL.html'
        ]

    elif equipo == 'Olympique Marsella':
        # List of HTML files to process
        html_files = [
            '2014-2015_OM.html',
            '2015-2016_OM.html',
            '2016-2017_OM.html',
            '2017-2018_OM.html',
            '2018-2019_OM.html',
            '2019-2020_OM.html',
            '2020-2021_OM.html',
            '2021-2022_OM.html'
        ]    

    elif equipo == 'Juventus':
        # List of HTML files to process
        html_files = [
            '2014-2015_Juventus.html',
            '2015-2016_Juventus.html',
            '2016-2017_Juventus.html',
            '2017-2018_Juventus.html',
            '2018-2019_Juventus.html',
            '2019-2020_Juventus.html',
            '2020-2021_Juventus.html',
            '2021-2022_Juventus.html'
        ]  

    elif equipo == 'Roma':
        # List of HTML files to process
        html_files = [
            '2014-2015_Roma.html',
            '2015-2016_Roma.html',
            '2016-2017_Roma.html',
            '2017-2018_Roma.html',
            '2018-2019_Roma.html',
            '2019-2020_Roma.html',
            '2020-2021_Roma.html',
            '2021-2022_Roma.html'
        ] 

    elif equipo == 'Napoles':
        # List of HTML files to process
        html_files = [
            '2014-2015_Napoles.html',
            '2015-2016_Napoles.html',
            '2016-2017_Napoles.html',
            '2017-2018_Napoles.html',
            '2018-2019_Napoles.html',
            '2019-2020_Napoles.html',
            '2020-2021_Napoles.html',
            '2021-2022_Napoles.html'
        ]            
        
    elif equipo == 'AC Milan':
        # List of HTML files to process
        html_files = [
            '2014-2015_Milan.html',
            '2015-2016_Milan.html',
            '2016-2017_Milan.html',
            '2017-2018_Milan.html',
            '2018-2019_Milan.html',
            '2019-2020_Milan.html',
            '2020-2021_Milan.html',
            '2021-2022_Milan.html'
        ]  
    elif equipo == 'Inter de Milan':
        # List of HTML files to process
        html_files = [
            '2014-2015_Inter.html',
            '2015-2016_Inter.html',
            '2016-2017_Inter.html',
            '2017-2018_Inter.html',
            '2018-2019_Inter.html',
            '2019-2020_Inter.html',
            '2020-2021_Inter.html',
            '2021-2022_Inter.html'
        ]       

    # Convert the HTML files list to full file paths
    html_files = [os.path.join(base_dir, file) for file in html_files]

    return html_files


def leerHtml(equipo):#AQUI LE DEBERIA PASAR EL EQUIPO PARA ELEGIR LOS HTML QUE VOY A LEER ACTUALMENTE SOLO ESTAN LOS DEL MADRID



    html_files = cargar_html(equipo)

    
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
                    aplazado_elem = result_elem.find('p', class_='match_hour match-apl')
                    
                    
                    if date_elem and home_team_elem and len(away_team_elems) > 1 and result_elem and aplazado_elem is None:
                        
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
            print(f"File {file_name} does not exist.")




def convert_date(date_str):
    # print(date_str)
    day, month, year = date_str.split()
    month = month_names[month.upper()]
    return f"{year}-{month}-{day.zfill(2)}"



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