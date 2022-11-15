from src.core import Core
from src.utils import *

from bs4 import BeautifulSoup as bs

class Plugin():
    def __init__(self):
        
        self.name = 'pressplay'
        self.about = 'Plugin for pressplay.top'
        self.author = 'Symbolic'
        self.home = 'https://pressplay.top'
        self.rows = ['Title', 'Link', 'Quality', 'Release date', 'Duration']
    
    def format_string(self, raw):
        return raw.replace(' ', '+')
    
    def format_data(self, raw: dict):
        return list(raw.values())
    
    def search(self, query:str) -> list[dict]:

        if len(query) <= 0:
            return [{'Error': 'no query provided!'}]

        query = self.format_string(query)
        with Core.session as s:
            resp = s.get(f'https://www.pressplay.top/?s={query}')
        
        s = bs(resp.text, 'html.parser')

        data = []
        for i in s.find_all('article', {'class': 'post dfx fcl movies'}):
            s = bs(str(i), 'html.parser')

            title = clean(s.find('h2', {'class': 'entry-title'}).text)
            link = clean(s.find('a', {'class': 'lnk-blk'}, href=True).attrs['href'])
            release = clean(s.find('div', {'class': 'entry-meta'}).text)

            duration = s.find('span', {'class': 'duration'})
            if duration:
                duration = clean(duration.text)
            else:
                duration = 'N/A'
            
            quality = s.find('span', {'class': 'quality'})
            if quality:
                quality = clean(quality.text)
            else:
                quality = 'N/A'

            data.append({
                'title': title,
                'link': link,
                'quality': quality,
                'release': release,
                'duration': duration
            })
        
        return data

Core.plugins.update({
    'pressplay': Plugin()
})