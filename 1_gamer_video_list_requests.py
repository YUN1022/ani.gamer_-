import time

tStart = time.time()#計時開始
import os
import sys
import csv
import re

def _input_file_(file_name,line_Blue_NUM):
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        lines = csv.reader(csvfile)
        columns = [line[line_Blue_NUM] for line in lines]
        return columns

def _output_file_(file_name,file_type,D0,D1,D2,D3,D4,D5):
    with open(file_name, file_type, newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([D0,D1,D2,D3,D4,D5])

def _add_dirs_(new_dirs):
    if not os.path.isdir(new_dirs):
        os.makedirs(new_dirs)

def _execute_time_():
    tMiddle = time.time()#計時結束
    #列印結果
    print("目前已執行了 %f 秒" % (tMiddle - tStart))#會自動做近位
    print("目前已執行了 %f 分鐘" % ((tMiddle - tStart)/60))#會自動做近位
    print("目前已執行了 %f 小時" % ((tMiddle - tStart)/60/60))#會自動做近位

new_dirs = '../Video_List/'
_add_dirs_(new_dirs)
output_file = new_dirs + 'gamer_video_list_ver_2.csv'

_output_file_(output_file, 'w', 'SN_Number', '影片名稱', '年份', '集數', '觀看人數', '網址')



import urllib.request as req
import bs4

#for i in range(1,35+1):
for i in range(1,36+1):

    url = 'https://ani.gamer.com.tw/animeList.php?page='+str(i)+'&c=0&sort=1'
    request = req.Request(url, data=None, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    })


    with req.urlopen(request, data=None) as response:
        data = response.read().decode("utf-8")
    #print(data)


    root = bs4.BeautifulSoup(data, "html.parser")
    theme_names = root.find_all('p', class_='theme-name')
    theme_times = root.find_all('p', class_='theme-time')
    theme_numbers = root.find_all('span', class_='theme-number')
    theme_list_mains = root.find_all('a', class_='theme-list-main')
    view_nums = root.find_all('p', class_='')
    #print(view_nums)
    #print(theme_names)
    theme_names_cnt = len(theme_names)
    for cnt in range(theme_names_cnt):
        #print('X'*30)
        #print(theme_names[cnt].string) # 影片名稱
        #print(theme_times[cnt].string) # 年份
        #print(theme_numbers[cnt].string) # 集數
        #print('='*30)
        link_1 = theme_list_mains[cnt]
        link = []
        link.append(link_1)
        link  = str(link)
        #link = link[link.find('<a class="theme-list-main" href="'):link.find('>"')]
        link_start = 'href="'
        #link_start_cnt = len(link_start)
        link_end = '">'
        link = link[link.find(link_start)+len(link_start):link.find(link_end)]
        #print(link) # 網址
        #print('*'*30)
        #print(view_nums[cnt].string) # 觀看人數

        #############################################

        theme_name = theme_names[cnt].string # 影片名稱
        theme_time = theme_times[cnt].string # 年份
        theme_number = theme_numbers[cnt].string # 集數
        theme_link = 'https://ani.gamer.com.tw/' + link # 網址
        theme_sn_number = link[link.rfind('=')+1:]
        view_num = view_nums[cnt].string # 觀看人數

        #############################################
        
        theme_name = theme_name.replace('\n','')
        theme_time = theme_time.replace('\n','')
        theme_time = theme_time.replace('年份：','')
        theme_number = theme_number.replace('\n','')
        theme_link = theme_link.replace('\n','')
        theme_sn_number = theme_sn_number.replace('\n','')
        view_num = view_num.replace('\n','')
        
        #############################################
        print('='*30)
        
        print('SN_Number:\t'+theme_sn_number) # SN_Number 
        print('影片名稱:\t'+theme_name) # 影片名稱
        print('年份:\t\t'+theme_time) # 年份
        print('集數:\t\t'+theme_number) # 集數
        print('觀看人數:\t'+view_num) # 觀看人數
        print('網址:\t\t'+theme_link) # 網址

        #############################################

        _output_file_(output_file, 'a', theme_sn_number, theme_name, theme_time, theme_number, view_num, theme_link)

tEnd = time.time()#計時結束
#列印結果
print("執行時間 %f 秒" % (tEnd - tStart))#會自動做近位
print("執行時間 %f 分鐘" % ((tEnd - tStart)/60))#會自動做近位
print("執行時間 %f 小時" % ((tEnd - tStart)/60/60))#會自動做近位