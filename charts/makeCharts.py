from pyecharts.charts.pie import Pie
from pyecharts.charts.map import Map
import static.name_map
from pymongo import MongoClient

# html代码头尾
html1 = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>疫情数据可视化</title><script src="/static/echarts/echarts.js"></script><script src="/static/china.js"></script><script src="/static/world.js"></script></head><body>'
html2 = '</body></html>'

# 绘制饼图，返回值为html代码
def make_PieChart(country):
    global Data
    Data = []

    # 读取数据库中的数据
    client = MongoClient()
    db = client.mydb
    if country == 'China':
        tb = db.ChinaData
    else:
        tb = db.WorldData
    re = list(tb.find())

    attrs = ['现存确诊', '死亡', '治愈']
    values = []
    currentConfirmedCount = 0
    deadCount = 0
    curedCount = 0


    for i in re:
        currentConfirmedCount += i['currentConfirmedCount']
        deadCount += i['deadCount']
        curedCount += i['curedCount']

    values.append(currentConfirmedCount)
    values.append(deadCount)
    values.append(curedCount)

    if country == 'China':
        country = '中国'
    else:
        country = '世界'

    # 绘制饼图
    pie = Pie(country+"疫情数据饼图")
    pie.add(
        "",
        attrs,
        values,
        is_label_show=True,
        is_more_utils=True
    )

    # pie.render_embed() 是绘制饼图的html代码

    html = html1 + pie.render_embed() + html2

    return html

# 绘制中国地图
def make_ChinaMap(type):
    global ChinaData
    ChinaData = []

    # 读取数据库中的数据
    client = MongoClient()
    db = client.mydb
    tb = db.ChinaData
    re = list(tb.find())

    allProvinces = []
    values = []

    for i in re:
        province = i['provinceName'].replace('省', '').replace('壮族自治区', '').replace('维吾尔自治区', '').replace('回族自治区', '').replace('自治区', '').replace('市', '')
        allProvinces.append(province)
        values.append(i[type])


    if type == 'currentConfirmedCount':
        type = '现存确诊'
    elif type == 'confirmedCount':
        type = '累计确诊'
    elif type == 'deadCount':
        type = '死亡'
    elif type == 'curedCount':
        type = '治愈'

    # 绘制地图
    map = Map("全国疫情"+type+"数据", '中国', width=1200, height=600)
    map.add(type, allProvinces, values, visual_range=[1, 1000], maptype='china', is_visualmap=True, visual_text_color='#000')

    # map.render_embed() 是绘制地图的html代码
    html = html1 + map.render_embed() + html2

    return html

# 绘制世界地图
def make_WorldMap(type):
    global WorldData
    WorldData = []

    # 读取数据库中的数据
    client = MongoClient()
    db = client.mydb
    tb = db.WorldData
    re = list(tb.find())

    allCountries = []
    values = []

    for i in re:
        country = i['provinceName']
        allCountries.append(country)
        values.append(i[type])

    # 国家中文名转为英文
    for a in range(len(allCountries)):
        for b in static.name_map.name_map.keys():
            if allCountries[a] == static.name_map.name_map[b]:
                allCountries[a] = b
            else:
                continue

    if type == 'currentConfirmedCount':
        type = '现存确诊'
    elif type == 'confirmedCount':
        type = '累计确诊'
    elif type == 'deadCount':
        type = '死亡'
    elif type == 'curedCount':
        type = '治愈'

    # 绘制地图
    map = Map("国外疫情" + type + "数据", '国外', width=1200, height=600)
    map.add(type, allCountries, values, visual_range=[1, 100000], maptype='world', is_visualmap=True,
            visual_text_color='#000')

    # map.render_embed() 是绘制地图的html代码
    html = html1 + map.render_embed() + html2

    return html
