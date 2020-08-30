import csv
import requests
import codecs
import time
from datetime import datetime as dt
from collections import Counter
from bs4 import BeautifulSoup
import re
import pandas
import pprint
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

url="https://db.netkeiba.com/?pid=race_list&word=%5E%C5%EC%B5%FE%CD%A5%BD%D9"
race_html=requests.get(url)
race_html.encoding = race_html.apparent_encoding
race_soup=BeautifulSoup(race_html.text,'html.parser')

title = race_soup.find_all("a",title="東京優駿(G1)")

for i in range(20):
    title[i]=re.sub(r"\D","",str(title[i]))
    title[i]=title[i][:-2]

uma_num= 3
Race_row= 10

odds_data=[]
name_data=[]

#goukei_lists=[uma_num*Race_row]


for a in range(Race_row):
    
    url="https://race.netkeiba.com/race/result.html?race_id="+title[a]+"&rf=race_list"
    race_html=requests.get(url)
    race_html.encoding = race_html.apparent_encoding
    race_soup=BeautifulSoup(race_html.text,'html.parser')

    odds = race_soup.find_all("td",class_="Odds Txt_R")
    name = race_soup.find_all("span",class_="Horse_Name")

    print(2020-a)
    name_lists = []
    odds_lists = []


    for i in range(uma_num):
        
        odds_lists.insert(1+i, odds[i])
        name_lists.insert(1+i, name[i])
        odds_lists[i] = re.sub(r"\n","",str(odds_lists[i]))
        odds_lists[i] = re.sub(r"<[^>]*?>","",str(odds_lists[i]))
        odds_lists[i] = re.sub(r"</td>",",",str(odds_lists[i]))
        name_lists[i] = re.sub(r"\n","",str(name_lists[i]))
        name_lists[i] = re.sub(r"<[^>]*?>","",str(name_lists[i]))
        name_lists[i] = re.sub(r"</td>",",",str(name_lists[i]))
        print(i+1,name_lists[i],odds_lists[i])

    odds_data+=odds_lists
    name_data+=name_lists
    print("\n")


data_list=[float(i) for i in odds_data]

odds_main=[0]*5

for i in range(len(data_list)):
    if data_list[i]<3.0:
        odds_main[0]+=1
    elif data_list[i]<6.0:
        odds_main[1]+=1
    elif data_list[i]<9.0:
        odds_main[2]+=1
    elif data_list[i]<12.0:
        odds_main[3]+=1
    else:
        odds_main[4]+=1



x = np.array(["3.0未満","3.0~6.0","6.0~9.0","9.0~12.0","12.0~15.0"])
y = np.array(odds_main)
#x_position=np.arange(len(x))
width=0.5
plt.xticks(rotation=60)
plt.bar(x, y)
plt.title('日本ダービー')
plt.show()
s=float(0)
print(data_list)