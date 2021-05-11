import time

tStart = time.time()#計時開始

import os
import requests
import re
import pandas as pd
import json
import csv
from bs4 import BeautifulSoup

def _execute_time_():
    tMiddle = time.time()#計時結束
    #列印結果
    print("目前已執行了 %f 秒" % (tMiddle - tStart))#會自動做近位
    print("目前已執行了 %f 分鐘" % ((tMiddle - tStart)/60))#會自動做近位
    print("目前已執行了 %f 小時" % ((tMiddle - tStart)/60/60))#會自動做近位

def _add_dirs_(new_dirs):
    if not os.path.isdir(new_dirs):
        os.makedirs(new_dirs)

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
            sn = re.search(pattern, i.get('href')).group(0)
            sn_list.append(sn)

        
        return sn_list

    except:
        return 'faild'

def get_Danmu(sn):
    
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




# Read CSV file
df = pd.read_csv('gamer_video_list_Complete.csv')

# Make lists
WSN_list = df['網址SN'].tolist()
Video_list = df['影片名稱'].tolist()
Year_list = df['年份'].tolist()
VN_list = df['觀看人數'].tolist()

#for SN_row in range(20):
#Run for loop
for SN_row in range(len(WSN_list)):
    print(SN_row)
    f = df['網址SN'] == WSN_list[SN_row]
    df.loc[f]
    temp = df.loc[f]['各集SN'].values
    
    pattern = r'([\d]+)'
    r = re.findall(pattern, temp[0])
    #path = './danmu/'+ str(WSN_list[SN_row])+'/'
    #path = './gamer_data2/'+str(WSN_list[SN_row])+'/'
    path = './gamer_data/'
    _add_dirs_(path)
    path_folder = './gamer_data_folder/'+str(WSN_list[SN_row])+'/'
    _add_dirs_(path_folder)
    userid = []
    time = []
    text = []
    danmu_sn = []
    for index, sn in enumerate(r):
        data_json = get_Danmu(sn)
        data_json
        for i in data_json:
            text.append(i['text'])
            time.append(i['time'])
            userid.append(i['userid'])
            danmu_sn.append(i['sn'])
        df2 = pd.DataFrame({
            'time':time,
            'userid':userid,
            'danmu_sn':danmu_sn,
            '彈幕內容':text
        })
        #df2['影片名稱'] = Video_list[SN_row]
        df2.insert(0,'影片名稱',Video_list[SN_row])
        
        #df2['Webpage'] = 'https://ani.gamer.com.tw/animeRef.php?sn='+str(WSN_list[SN_row])
        df2.insert(1,'影片SN',str(WSN_list[SN_row]))
        df2.insert(2,'年份',str(Year_list[SN_row]))
        df2.insert(3,'觀看人數',str(VN_list[SN_row]))
        df2.insert(4,'集數',str(index + 1))
        df2.insert(5,'集數SN',str(sn))
        df2['影片網址'] = 'https://ani.gamer.com.tw/animeRef.php?sn='+str(WSN_list[SN_row])

        df2['集數網址'] = 'https://ani.gamer.com.tw/animeVideo.php?sn='+str(sn)

        df2.to_csv(path+str(WSN_list[SN_row])+'_{}.csv'.format(index + 1), index = False, encoding = 'utf-8-sig')
        df2.to_csv(path_folder+str(WSN_list[SN_row])+'_{}.csv'.format(index + 1), index = False, encoding = 'utf-8-sig')
       
        userid = []
        time = []
        text = []
        danmu_sn = []
'''
tEnd = time.time()#計時結束
#列印結果
print("執行時間 %f 秒" % (tEnd - tStart))#會自動做近位
print("執行時間 %f 分鐘" % ((tEnd - tStart)/60))#會自動做近位
print("執行時間 %f 小時" % ((tEnd - tStart)/60/60))#會自動做近位
'''