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
        # anime_name = re.search(pattern, bsobj.title.text).group(1)

        season_section = bsobj.find('section', {'class':'season'})
        anime_url = season_section.find_all('a')

        sn_list = []
        for i in anime_url:
            i.get('href')
            pattern = "[0-9]+"
            sn = re.search(pattern, i.get('href')).group(0)
            sn_list.append(sn)

        return sn_list

    except:
        return 'faild'

if __name__ == '__main__':
    df = pd.read_csv('gamer_video_list_ver_2.csv', index_col='SN_Number', encoding='utf-8-sig')
    sn = []

    for i in df.index:
        sn_list = crawler('https://ani.gamer.com.tw/animeRef.php?sn='+str(i))
        sn.append(sn_list)
    df.insert(0, column = '各集SN', value = sn)
    df.to_csv('gamer_video_list_ver_2.csv', index=False, encoding='utf-8-sig')