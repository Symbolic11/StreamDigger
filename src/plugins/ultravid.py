from src.core import Core
from src.utils import *

from bs4 import BeautifulSoup as bs

class Plugin():
    def __init__(self):
        
        self.name = 'ultravid'
        self.about = 'Plugin for ultravid.ca'
        self.author = 'Symbolic'
        self.home = 'https://ultravid.ca'
        self.rows = ['Title', 'IMDB rating', 'Release date', 'Location', 'Link']
    
    def format_string(self, raw):
        return raw.replace(' ', '+')
    
    def format_data(self, raw: dict):
        return list(raw.values())
    
    def search(self, query:str) -> list[dict]:

        if len(query) <= 0:
            return [{'Error': 'no query provided!'}]

        query = self.format_string(query)
        with Core.session as s:
            resp = s.get(f'https://www.ultravid.ca/?s={query}')
        
        s = bs(resp.text, 'html.parser')

        data = []
        for i in s.find_all('div', {'class': 'movies-list movies-list-full'}):
            s = bs(str(i), 'html.parser')

            for z in s.find_all('div', {'class': 'ml-item'}):
                s = bs(str(z), 'html.parser')

                link = clean(s.find('a', href=True).attrs['href'])

                if not link.startswith('http'):
                    link = f'https{link}'

                info = bs(str(s.find(
                    'div', 
                    {'id': 'hidden_tip'
                })), 'html.parser')

                title = clean(info.find(
                    'div', 
                    {'class': 'qtip-title'
                }).text)

                imdb_rating = clean(info.find(
                    'div', 
                    {'class': 'jt-info jt-imdb'
                }).text)

                release = clean(info.find('a', href=True).text)
                release = release if is_valid_year(release) else None

                s = bs(str(
                    info.find(
                        'div', 
                        {'class': 'block'}
                    )
                ), 'html.parser')

                loc = clean(s.find('a', href=True).text)

                data.append({
                    'title': title,
                    'imdb': imdb_rating,
                    'release': release,
                    'location': loc,
                    'link': link
                })

        return data

Core.plugins.update({
    'ultravid': Plugin()
})