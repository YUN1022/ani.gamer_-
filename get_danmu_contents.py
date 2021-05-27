from danmu_clawer import get_Danmu
import pandas as pd
import os
import re
import gc
import time
import random

def get_contents(path, r, SN):

    for index, sn in enumerate(r):
        userid = []
        time = []
        text = []
        danmu_sn = []

        data_json = get_Danmu(sn)
        for i in data_json:
            text.append(i['text'])
            time.append(i['time'])
            userid.append(i['userid'])
            danmu_sn.append(i['sn'])
            
        df2 = pd.DataFrame({
            'time':time,
            'text':text,
            'userid':userid,
            'danmu_sn':danmu_sn
        })
        df2.to_csv(path+'/{}_{}.csv'.format(SN, index + 1), index = False, encoding = 'utf-8-sig')
        
        del df2
        gc.collect()

if __name__ == '__main__':
    strat = time.time()
    df = pd.read_csv('gamer_video_list_Complete.csv')
    for SN in df['網址SN'][:10]:
        time.sleep(random.uniform(1, 2))
        danmu_path = r'./danmu/' + str(SN)
        if not os.path.isdir(danmu_path):
            os.mkdir(danmu_path)
        
        try:
            f = df['網址SN'] == SN
            sn = df.loc[f]['各集SN'].values
            pattern = r'([\d]+)'
            r = re.findall(pattern, sn[0])
            get_contents(danmu_path, r, SN)
        except:
            print(SN)

    end = time.time()

    print("執行時間: " + str(end - strat) + " seconds")