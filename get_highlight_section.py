import csv
import pandas as pd
import os
import numpy as np

def slope(data, x1, x2):
        y1 = data.loc[x1][0]
        y2 = data.loc[x2][0]

        return (y2-y1) / (x2-x1)

  
def read_all_episode(sn):
    """return target anime all episode danmu count"""
    
    global path
    path = './danmu/{}/'.format(sn)
    global episode_count
    episode_count = len(os.listdir(path))

    all_episode = []
    for episode in range(1, episode_count+1):
        df = pd.read_csv(path + '{}_{}.csv'.format(sn, episode))

        sec_10_interval = []
        for i in range(1, 150):
            f = ((i-1) * 100 <= df['time']) & (df['time'] < i * 100) # 以每10秒間隔做區分
            sec_10_interval.append(len(df[f])) # 第n個10秒內有幾筆彈幕
        all_episode.append(sec_10_interval)

    return all_episode


def get_Highlight(data ,T):
    
    i = 0
    j = 149

    if T > 1:
        left_baseline = slope(data, T-1, T)
        for i in range(T-1, 0, -1):
            if abs(left_baseline - slope(data, T, i)) >= 10:
                break

    if T < 149:
        right_baseline = slope(data, T, T+1)
        for j in range(T+1, 149):
            if abs(right_baseline - slope(data, j, T)) >= 10:
                break
    
    return i,j

def get_Highlight_section(sn):

    all_episode = read_all_episode(sn)

    all_highlight_section = {}
    for i in range(0, len(all_episode)):
        df_count = pd.DataFrame(
            {
                'count':all_episode[i]
            }
        )
    
        f = df_count['count'] > (np.mean(all_episode[i]) - 1) + (2 * np.std(all_episode[i]) - 1)
        section = []
        for peak in df_count[f].index:
            start, end = get_Highlight(df_count, peak)
            section.append((start, end))

        all_highlight_section['第{}集'.format(i+1)] = section
    
    return all_highlight_section


def get_Highlight_danmu(all_highlight_section, sn):
    for episode in range(episode_count):
        danmu_dict = {}
        for i in all_highlight_section['第{}集'.format(episode+1)]:
            df = pd.read_csv(path + '{}_{}.csv'.format(sn, episode+1))
            df['time'] = df['time']/100
            f = (df['time'] >= i[0]) & (df['time'] < i[1] )
            danmu = df[f]['text'].values.tolist()
            danmu_dict['section{}'.format(i)] = danmu
        
        df2 = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in danmu_dict.items()]))
        df2.to_csv('./extract_danmu/{}/episode{}.csv'.format(sn, episode+1), encoding='utf-8-sig', index=False)

if __name__ == '__main__':

    sn = 109573
    save_path = './extract_danmu/{}/'.format(sn)
    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    all_highlight_section = get_Highlight_section(sn)
    get_Highlight_danmu(all_highlight_section, sn)

    df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in all_highlight_section.items()]))
    df.to_csv(save_path + '/{}_sections.csv'.format(sn), encoding='utf-8-sig', index=False)
