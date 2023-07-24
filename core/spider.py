import re
import sys
import bs4 
import requests
import sys
import csv 
import pandas as pd

#-----  csv資料庫搜尋
df = pd.read_csv("medicine.csv", delimiter=',',header = None, na_filter=False)
data = df.to_numpy()

def search_drug(name):    
    
    medicine_list = []    
    medicine_list_id = []
    medicine_chosen = []
    #name = '旅暈'
    for i in range(1, 27182):        
        if name in data[i][1]:
            medicine_list.append(data[i][1])            
            medicine_list_id.append(i)
            id = i
    for i in range(len(medicine_list_id)):        
        medicine_list_id[i] = data[medicine_list_id[i]][0][:]
        tempDict = {}        
        tempDict['name'] = medicine_list[i]
        tempDict['id'] = medicine_list_id[i]        
        medicine_chosen.append(tempDict)
    
    return medicine_chosen







def ti1(soup):
    titles_m1 = soup.find_all("span", attrs={"style": "font-family:標楷體;"}) 
    out_list=[]
    for s in titles_m1: 
        out_list.append(s.text.strip())
    #print(out_list)
    point_1=out_list.index("副作用")
    #print(point_1)

    for i in range(point_1+2,len(out_list),2):
        return(f"{out_list[i-1]}: {out_list[i]}")


def ti2(soup):
    out_list=[]
    titles_m2 = soup.find_all("span", attrs={"style":"color:black;font-family:標楷體;"})
    for s in titles_m2: 
        out_list.append(s.text.strip())
    #print(out_list)
    point_1=out_list.index("副作用")
    for i in range(point_1+2,len(out_list),2):
        return(f"{out_list[i-1]}: {out_list[i]}")
    
#續寫串列中資料整理 ti3 待處理 透過 層3 的藥物進行歸納

def ti3(soup):
    titles_m3 = soup.find_all("span", attrs={"style": "color:black;"})
    out_list=[]
    for s in titles_m3: 
        out_list.append(s.text.strip())
    #print(out_list)
    point_1=out_list.index("副作用")
    for i in range(point_1+2,len(out_list),2):
        return(f"{out_list[i-1]}: {out_list[i]}")    


def ti4(soup):
    for i in soup.find_all('table', class_="sub-table"):    
        if re.match(r'臨床重要副作用/不良反應', ''.join(i.text.strip().split()[1:])):      
            return(re.sub("\n+", "\n", i.text.strip())[21:])

        elif re.match(r'5.1', ''.join(i.text.strip().split())):
            return(re.sub("\n+", "\n", i.text.strip())[21:])
            break




#<span style="font-family:標楷體;">發疹</span> 
# 印出每個分析結果,strip:去除文字首尾空白 


#o~10 #11~len(out_list)

def search_side_effect(name):

    # 利用 cfscrape 存取指定網頁 
    #scraper = cfscrape.create_scraper() 
    result = requests.get(f'https://mcp.fda.gov.tw/im_detail_1/{name}' ).text

    # 利用 bs4 解析指定網頁 
    soup = bs4.BeautifulSoup(result, "html.parser")

    print("如有以下副作用，請立即停止使用 :")
    x = '如有以下副作用，請立即停止使用 :\n'
    try:
        x += ti1(soup)
        #print("由層1輸出")
    except:
        try:
            x += ti2(soup)
            #print("由層2輸出")
        except:
            try:
                x += ti3(soup)
                #print("由層3輸出")
            except:
                try:
                    x += ti4(soup)
                    #print("由層4輸出")
                except:
                    pass

                pass
        pass
    finally: 
        return(x)

    #print(f"副作用  {out_put}")
