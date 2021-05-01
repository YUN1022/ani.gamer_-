import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

def crawler(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        bsobj = BeautifulSoup(response.text, 'lxml')
        pattern = r'(.+)\[.*'
        anime_name = re.search(pattern, bsobj.title.text).group(1)

        season_section = bsobj.find('section', {'class':'season'})
        anime_url = season_section.find_all('a')

        sn_list = []
        for i in anime_url:
            i.get('href')
            pattern = "[0-9]+"
            sn = re.search(pattern, anime_url[0].get('href')).group(0)
            sn_list.append(sn)

        dict = {anime_name: sn_list}
        return dict

    except:
        return {url: 'faild'}

if __name__ == '__main__':
    print(crawler('https://ani.gamer.com.tw/animeRef.php?sn=112522'))
