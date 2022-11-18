from src.core import Core
from src.utils import *
from bs4 import BeautifulSoup as bs

class Plugin():
    def __init__(self):
        
        self.name = '0123movies'
        self.about = 'Plugin for 0123movies.com'
        self.author = 'Symbolic'
        self.home = 'https://0123movies.com'
        self.rows = ['Title', 'Link', 'Quality', 'Release date', 'Duration']
    
    def format_string(self, raw):
        return raw.replace(' ', '-')
    
    def format_data(self, raw: dict):
        return list(raw.values())
    
    def search(self, query:str) -> list[dict]:

        if len(query) <= 0:
            return [{'Error': 'no query provided!'}]

        query = self.format_string(query)
        with Core.session as s:
            resp = s.get(f'https://0123movies.com/search/?q={query}')
        
        s = bs(resp.text, 'html.parser')

        data = []
        for i in s.find_all('div', {'class': 'ml-item movie-item'}):
            s = bs(str(i), 'html.parser')

            info = s.find('a', {'class': 'ml-mask jtip'})
            
            title = info.attrs['title']
            link = info.attrs['href']

            quality = clean(s.find(
                'span', 
                {'class': 'mli-quality'}
            ).text)

            release = clean(s.find(
                'span', {'class': 'year'}
            ).text)

            duration = s.find('span', {'class': 'duration'})
            if duration: duration = clean(duration.text)
            else: duration = 'N/A'
            
            data.append({
                'titl': title,
                'link': link,
                'quality': quality,
                'release': release,
                'duration': duration
            })
            
        return data

Core.plugins.update({
    '0123movies': Plugin()
})