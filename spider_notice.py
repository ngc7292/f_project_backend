import requests
import jieba
import pymysql.cursors
import time



def get_infos(id=20,new_date=0):
    url = "http://www.szse.cn/disclosure/notice/company/index.html"

    if new_date == 0:
        res = requests.get(url=url)

        print(res.encoding)
        print(res.text.encode('ISO-8859-1').decode('utf-8'))
    else:
        pass

def get_info():
    pass

def save_info():
    pass

if __name__ == '__main__':
    get_info()
