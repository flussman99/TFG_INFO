#En directo de la url

import pandas as pd
from bs4 import BeautifulSoup

import requests

urlResultados = "https://www.f1-fansite.com/f1-results/f1-standings-2024-championship/"
urlFechas = "https://www.f1-fansite.com/f1-results/f1-standings-2024-championship/" #hay que cambiarla

responseResultados = requests.get(urlResultados)
responseFechas = requests.get(urlFechas)


# Lista para almacenar los datos de todos los archivos
data = []

if responseResultados.status_code == 200 and responseFechas.status_code == 200:
    
    respuestaResultados = responseResultados.text
    respuestaFechas = responseFechas.text

    soup_tabla_principal = BeautifulSoup(respuestaResultados, 'html.parser')
    soup_tabla_fechas = BeautifulSoup(respuestaFechas, 'html.parser')

    datos_piloto = []
    for fila in soup_tabla_principal.find_all('tr'):
        if piloto in fila.get_text():
            datos = [td.get_text() for td in fila.find_all('td')]
            datos_piloto.append(datos)
    
    # Transponerlo para que sea una columna
    datos_piloto = list(zip(*datos_piloto))


 