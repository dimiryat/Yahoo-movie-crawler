# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
import re
import json

target_url = 'https://movies.yahoo.com.tw/movie_thisweek.html'

def get_movie_id(url):
    try:
        movie_id = url.split('-')[-1]
    except:
        movie_id = url
    return movie_id

def get_date(date_str):
    pattern = '\d+-\d+-\d+'
    match = re.search(pattern, date_str)
    if match is None:
        return date_str
    else:
        return match.group(0)
    
def get_movies(dom):
    soup = BeautifulSoup(dom, 'html5lib')
    movies = []
    rows = soup.find_all('div', 'release_info_text')
    for row in rows:
        movie = dict()
        movie['expectation'] = row.find('div', 'leveltext').span.text.strip()
        movie['ch_name'] = row.find('div', 'release_movie_name').a.text.strip()
        movie['eng_name'] = row.find('div', 'release_movie_name').find('div', 'en').a.text.strip()
        movie['movie_id'] = get_movie_id(row.find('div', 'release_movie_name').a['href'])
        movie['poster_url'] = row.parent.find_previous_sibling('div','release_foto').a.img['data-src']
        movie['release_date'] = get_date(row.find('div', 'release_movie_time').text)
        movie['intro'] = row.find('div', 'release_text').text.replace(u' 詳全文 ', '').strip()
        trailer_a = row.find_next_sibling('div', 'release_btn color_btnbox').find_all('a')[1]
        movie['trailer_url'] = trailer_a['href'] if 'href' in trailer_a.attrs else ''
        movies.append(movie)
    return movies

def get_web_page(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print("Invalid url : ", resp.url)
        return None
    else:
        return resp.text

if __name__=="__main__":
    page = get_web_page(target_url)
    if page:
        movies = get_movies(page)
        for movie in movies:
            print(movie)
        with open('movie.json', 'w', encoding='utf-8') as f:
            json.dump(movies, f, indent=2 , sort_keys=True, ensure_ascii=False)