from src.core import Core
from src.utils import *
from bs4 import BeautifulSoup as bs

class Plugin():
    def __init__(self):
        
        self.name = 'ev01'
        self.about = 'Plugin for ev01.net'
        self.author = 'Symbolic'
        self.home = 'https://ev01.net'
        self.rows = ['Title', 'Link', 'Quality', 'Release date', 'Duration', 'Season', 'Episode', 'Type']
    
    def format_string(self, raw):
        return raw.replace(' ', '-')
    
    def format_data(self, raw: dict):
        return list(raw.values())
    
    def search(self, query:str) -> list[dict]:

        if len(query) <= 0:
            return [{'Error': 'no query provided!'}]

        query = self.format_string(query)
        with Core.session as s:
            resp = s.get(f'https://ev01.net/search/{query}')
        
        s = bs(resp.text, 'html.parser')

        data = []
        for i in s.findAll('div', {'class': 'flw-item'}):
            s = bs(str(i), 'html.parser')

            info = s.find('h2', {'class': 'film-name'}).find('a', href=True)

            url = info.attrs['href']
            name = info.attrs['title']

            if not url.startswith('http'):
                url = f'{self.home}{url}'

            quality = s.find('span', {'class': 'fi-ql'}).text

            s = bs(str(s.find(
                'div', 
                {'class': 'film-infor'}
                )
            ), 'html.parser')

            info = s.find_all('span')

            # everything is None by default
            release = duration = season = episode = None
            if is_valid_year(info[1].text):
                release = info[1].text
                duration = info[2].text
            else:
                season = info[1].text
                episode = info[2].text

            data.append({
                'name': name,
                'link': url,
                'quality': quality,
                'release': release,
                'duration': duration,
                'season': season,
                'episode': episode,
                'type': 'movie' if release else 'show'
            })
        
        return data

Core.plugins.update({
    'ev01': Plugin()
})