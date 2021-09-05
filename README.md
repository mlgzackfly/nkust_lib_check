# 說明
~~這是工作拿來偷懶用的~~，寫快樂的，所以 code 很亂。  
能檢查圖書館的[電子資源](https://www.lib.nkust.edu.tw/portal/portal__db_list_1.php)。  
HTTP status code 只要 ok 都算是連線正常。  
會額外寫一個 output.txt 紀錄連線有問題的網址。  
最後會紀錄花了多久時間(以秒為單位)。  

# 使用
python3  

 安裝套件  
`pip install -r requirements.txt`

執行  
`python3 lib.py`

# 之後要改的
1. 有些網站明明能連但還是顯示錯誤
2. 輸出格式或許可以考慮 json
3. code 可以寫好看一點
