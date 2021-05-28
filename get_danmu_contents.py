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
    count = 1
    faild_list = []

    for SN in df['網址SN']:
        danmu_path = r'./danmu/' + str(SN)
        if not os.path.isdir(danmu_path):
            os.mkdir(danmu_path)
        
        try:
            f = df['網址SN'] == SN
            sn = df.loc[f]['各集SN'].values
            pattern = r'([\d]+)'
            r = re.findall(pattern, sn[0])
            get_contents(danmu_path, r, SN)
            print("Now: {} %".format(count//len(df)*100), end = '\r')
        except:
            faild_list.append(SN)
        
        time.sleep(random.uniform(1,2))

    end = time.time()

    print("執行時間: {} seconds".format(end - strat))
    print("共{}部動畫失敗, 代碼:{}".format(len(faild_list), faild_list))