from flask import Flask
from flask import render_template
from pymongo import MongoClient
from jinja2 import Markup
import charts.makeCharts


app = Flask(__name__)

# 默认网页
@app.route('/')
def show_start():
    return render_template('Start.html')

# 关于网页
@app.route('/about/')
def show_about():
    return render_template('About.html')


# 中国每个省的疫情详细数据网页
@app.route('/china/')
def show_ChinaData():
    global ChinaData
    ChinaData = []
    client = MongoClient()
    db = client.mydb
    tb = db.ChinaData
    re = list(tb.find())

    for i in re:
        temp = []
        temp.append(i['provinceName'])
        temp.append(i['currentConfirmedCount'])
        temp.append(i['confirmedCount'])
        temp.append(i['deadCount'])
        temp.append(i['curedCount'])
        ChinaData.append(temp)

    return render_template('ChinaData.html', ChinaData=ChinaData)

# 省的每个地区的疫情详细数据网页
@app.route('/china/<province>/')
def show_provinceData(province):
    global citiesData
    citiesData = []
    client = MongoClient()
    db = client.mydb
    tb = db.ChinaData
    re = list(tb.find())

    for i in re:
        if i['provinceName'] == province:
            cities = i['cities']

            if not cities:
                citiesData.append( [i['provinceName'], i['currentConfirmedCount'], i['confirmedCount'], i['suspectedCount'], i['curedCount'], i['deadCount']])
            else:
                for j in cities:
                    city = [j['cityName'], j['currentConfirmedCount'], j['confirmedCount'], j['suspectedCount'],
                            j['curedCount'], j['deadCount']]
                    citiesData.append(city)

    return render_template('ProvinceData.html', citiesData=citiesData)

# 世界每个国家的疫情详细数据网页
@app.route('/world/')
def show_worldData():
    global worldData
    worldData = []
    client = MongoClient()
    db = client.mydb
    tb = db.WorldData
    re = list(tb.find())

    for i in re:
        temp = []
        temp.append(i['provinceName'])
        temp.append(i['currentConfirmedCount'])
        temp.append(i['confirmedCount'])
        temp.append(i['deadCount'])
        temp.append(i['curedCount'])
        worldData.append(temp)

    return render_template('WorldData.html', WorldData=worldData)

# 数据可视化之地图网页
@app.route('/map/<area>', methods=['GET', 'POST'])
def show_map(area):
    if area == '中国疫情现存确诊':
        map_chart = charts.makeCharts.make_ChinaMap('currentConfirmedCount')
    elif area == '中国疫情累计确诊':
        map_chart = charts.makeCharts.make_ChinaMap('confirmedCount')
    elif area == '中国疫情治愈':
        map_chart = charts.makeCharts.make_ChinaMap('curedCount')
    elif area == '中国疫情死亡':
        map_chart = charts.makeCharts.make_ChinaMap('deadCount')
    elif area == '国外疫情现存确诊':
        map_chart = charts.makeCharts.make_WorldMap('currentConfirmedCount')
    elif area == '国外疫情累计确诊':
        map_chart = charts.makeCharts.make_WorldMap('confirmedCount')
    elif area == '国外疫情治愈':
        map_chart = charts.makeCharts.make_WorldMap('curedCount')
    else:
        map_chart = charts.makeCharts.make_WorldMap('deadCount')

    return Markup(map_chart)

# 数据可视化之饼图网页
@app.route('/pie/<area>',methods=['GET', 'POST'])
def show_pie(area):
    if area == '中国':
        pie_chart = charts.makeCharts.make_PieChart('China')
    else:
        pie_chart = charts.makeCharts.make_PieChart('World')

    return Markup(pie_chart)

if __name__ == '__main__':
    app.run()
