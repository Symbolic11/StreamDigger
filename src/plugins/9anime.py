from src.core import Core
from src.utils import *
from bs4 import BeautifulSoup as bs

class Plugin():
    def __init__(self):
        
        self.name = '9Anime'
        self.about = 'Plugin for 9anime.vc'
        self.author = 'Symbolic'
        self.home = 'https://9anime.vc'
        self.rows = ['Title', 'Link']
    
    def format_data(self, raw: dict):
        return list(raw.values())
    
    def search(self, query:str) -> list[dict]:
        if len(query) <= 0:
            return [{'Error': 'no query provided!'}]

        with Core.session as s:
            resp = s.get(f'https://9anime.vc/search?keyword={query}')

        s = bs(resp.text, 'html.parser')

        data = []
        for i in s.find_all('div', {'class': 'flw-item item-qtip'}):
            s = bs(str(i), 'html.parser')
            
            z = bs(str(s.find(
                'h3',
                {'class': 'film-name'}
            )), 'html.parser')
            
            info = z.find('a', href=True)
            title = info.attrs['title']
            link = info.attrs['href']

            if not link.startswith('http'):
                link = f'{self.home}{link}'

            data.append({
                'title': title,
                'link': link
            })
        
        return data

Core.plugins.update({
    '9anime': Plugin()
})