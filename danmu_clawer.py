import requests
import json

def get_Danmu(sn):
    '''
    >>>get_Danmu(sn)
    'received danmu'
    '''
    headers = {
        'authority':'ani.gamer.com.tw',
        'accept':'application/json, text/javascript, */*; q=0.01',
        'accept-endcoding':'gzip, deflate, br',
        'content-length':'8',
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        'origin':'https://ani.gamer.com.tw',
        'referer':'https://ani.gamer.com.tw/animeVideo.php?sn='+str(sn),
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'x-requested-with':'XMLHttpRequest'
    }
    url = 'https://ani.gamer.com.tw//ajax/danmuGet.php'
    FormData = {'sn':str(sn)}

    response = requests.post(url, data=FormData, headers=headers)
    return response.json()
