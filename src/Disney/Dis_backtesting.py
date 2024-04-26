import threading
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import numpy as np

data = []
compras = []

html_movies_files = [
    'Disney_2010_2019.html',
    'Disney_Animation_2010_2019.html',
    'Disney_2020_2029.html',
    'Disney_Animation_2020_2029.html'
]

def get_movie_ratings(movie_titles):
    api_key = 'c8a6e89190cb7be8e6b92a4c8d032df3'
    ratings = []

    for title in movie_titles:
        if title is not None:  # Verificar si el título no es None
            formatted_title = '+'.join(title.split())
            print(formatted_title)
            url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={formatted_title}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['total_results'] > 0:
                    movie_id = data['results'][0]['id']
                    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
                    response = requests.get(url)
                    if response.status_code == 200:
                        movie_data = response.json()
                        rating = movie_data['vote_average']
                        ratings.append(rating)
                    else:
                        ratings.append(None)
                else:
                    ratings.append(None)
            else:
                ratings.append(None)
        else:
            ratings.append(None)
    
    return ratings

def backtesting():
    base_dir = os.path.abspath('src\Disney\html')
    html_films_files = [os.path.join(base_dir, file) for file in html_movies_files]

    date_pattern = r"^(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}$"

    for movies_file_name in html_films_files:
        if os.path.exists(movies_file_name):
            print(movies_file_name)
            with open(movies_file_name, 'r', encoding='utf-8') as file_results:
                html_content_movies = file_results.read()

            soup = BeautifulSoup(html_content_movies, 'html.parser')
            rows = soup.find_all('tr')

            titles = []
            release_dates = []

            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                release_date = cells[0].get_text(strip=True)
                if not re.match(date_pattern, release_date):
                    release_date = last_release_date
                else:
                    release_date_parsed = pd.to_datetime(release_date, errors='coerce')
                    if not pd.isnull(release_date_parsed):
                        last_release_date = release_date_parsed
                if len(cells) > 1:
                    title = cells[1].get_text(strip=True)
                    titles.append(title)
                else:
                    titles.append(None)
                release_dates.append(release_date)
                last_release_date = release_date

            ratings = get_movie_ratings(titles)

            df = pd.DataFrame({'Title': titles, 'Release Date': release_dates, 'Rating': ratings})
            df.to_excel(movies_file_name + '.xlsx', index=False)
            print(df)
