import requests
from pymongo import MongoClient
import json
from bs4 import BeautifulSoup

# 获取分页html
def get_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        # 如果返回的状态码不是200，则抛出异常
        response.raise_for_status()
        # 根据响应信息判断网页的编码格式，便于response.text知道如何解码
        response.encoding = response.apparent_encoding

    except Exception as e:
        print('爬取错误')

    else:
        print('爬取成功')
        return response.text

def getWorldData(htmlContent):
    # 实例化soup对象
    soup = BeautifulSoup(htmlContent, 'lxml')
    # 1.所有疫情数据信息存储在script[7]标签
    script = soup.find_all('script')[6]

    # 2.获取每个地区的疫情数据的详细信息
    d = script.string

    # 3.获取需要的疫情数据信息
    d = d.replace('try { window.getListByCountryTypeService2true = ', '').replace('}catch(e){}', '')
    print(d)
    res = json.loads(d)
    return res

url = 'https://ncov.dxy.cn/ncovh5/view/en_pneumonia'
htmlContent = get_content(url)
data = getWorldData(htmlContent)
print(data)

# 存入mongodb数据库
client = MongoClient()
db = client.mydb
WorldData = db.WorldData
WorldData.drop()
WorldData.insert_many(data)
