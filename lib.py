'''
電子資源檢測程式
https://github.com/mlgzackfly/nkust_lib_check
有任何問題可以送PR
'''
import time
import os
import shutil

import requests
from requests.packages import urllib3
import json
from bs4 import BeautifulSoup

if os.path.isfile('output.txt'):
    file_path = 'output_backup.txt'
    shutil.copyfile('output.txt',file_path)

file_path = 'output.txt'
f = open(file_path,'w', encoding='UTF-8')

print("歡迎使用電子資源檢測程式")

def main(): #Δημήτηρ 抓抓編號名字跟alma
    time_start = time.time()
    url = 'https://www.lib.nkust.edu.tw/portal/portal__db_list_1.php'
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text,'html.parser')

    list = soup.find_all(class_='uk-text-nowrap') # 取得全部資源
    list_count = len(list) # 取得資源總數

    for i in range(0,list_count):
        name = soup.find_all('td',{'headers':'col-2'})[i].text.strip()
        number = soup.find_all('td', {'headers': 'col-1'})[i].text
        link = soup.find_all('td',{'headers':'col-2'})[i].find("a", recursive=False)['href']
        position = link.find('alma')
        #print(number)
        #print(name)
        if "alma" in link: # 有些資源是直接連到網站(ex. 136) 如果沒有 alma 則直接進入最後的確認
            alma = link[int(position):int(position)+22]
            get_data(alma,name,number)
        else:
            try:
                last_check(url, name, number)
            except TimeoutError:
                print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name))
                print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name), file=f)
                print(url,file=f)
            except urllib3.exceptions.NewConnectionError:
                print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name))
                print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name), file=f)
                print(url, file=f)
            except requests.exceptions.ConnectionError:
                print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name))
                print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name), file=f)
                print(url, file=f)
            except:
                print("{} {} 有錯誤!!".format(number, name))
                print("{} {} 有錯誤!!".format(number, name), file=f)
                print(url, file=f)
    time_end = time.time()
    time_c = time_end - time_start
    print('time cost', round(time_c,2), 's') # 計算花費多久時間

def get_data(alma,name,number): #ʽἙρμῆς 用電子資源ㄉ庫json抓alma
    url ='https://nkust.primo.exlibrisgroup.com/primaws/rest/pub/edelivery/' + alma + '?vid=886NKUST_INST:86NKUST'
    res = requests.get(url=url)
    json_data = json.loads(res.text)

    if ("electronicServices" not in json_data): # 單機版資源無法測試QQ
        print("{} {} 限圖書館內單機使用！".format(number,name))
    else:
        road = json_data['electronicServices'][0]['serviceUrl']
        path = 'https://nkust.primo.exlibrisgroup.com'

        ture_url = path + road
        try:
            last_check(ture_url,name,number)
        except TimeoutError:
            print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name))
            print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name), file=f)
            print(ture_url, file=f)
        except urllib3.exceptions.NewConnectionError:
            print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name))
            print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name), file=f)
            print(ture_url, file=f)
        except requests.exceptions.ConnectionError:
            print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name))
            print("{} {} 有錯誤!! \n連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。".format(number, name), file=f)
            print(ture_url, file=f)
        except:
            print("{} {} 有錯誤!!".format(number, name))
            print("{} {} 有錯誤!!".format(number, name), file=f)
            print(ture_url, file=f)
        #time.sleep(3) # 怕流量異常被擋住

def last_check(url,name,number): #Ἑκάτη 測試最後的連線是否正常
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    urllib3.disable_warnings()
    res = requests.get(url=url,headers=user_agent,verify=False)
    #print(res.headers)
    if (not res.ok): #200 <= res.status_code >= 299
        print("{} {} 連線有問題!".format(number, name))
        print("{} {} 連線有問題!".format(number,name), file=f)
        print(url, file=f)
    else:
        print("{} {} 連線成功!".format(number,name))

if __name__ == '__main__':
    main()

