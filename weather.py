import requests
from bs4 import BeautifulSoup
from pyecharts import Bar
ALL_DATA =[]
#解析网页并提取出城市名和城市最高温度
def parse_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    html = requests.get(url,headers=headers)
    text = html.content.decode('utf-8')
    soup = BeautifulSoup(text, 'html5lib')
    conMidtab = soup.find('div',class_='conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index==0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({"city":city,"hight_temp":temp})
            # print({"city":city,"hight_temp":temp})
            data = ALL_DATA[0:10]

#获取每个地区对应的url
def main():
    urls = ['http://www.weather.com.cn/textFC/hb.shtml',
            'http://www.weather.com.cn/textFC/db.shtml',
            'http://www.weather.com.cn/textFC/hd.shtml',
            'http://www.weather.com.cn/textFC/hz.shtml',
            'http://www.weather.com.cn/textFC/hn.shtml',
            'http://www.weather.com.cn/textFC/xb.shtml',
            'http://www.weather.com.cn/textFC/xn.shtml',
            'http://www.weather.com.cn/textFC/gat.shtml'
            ]
    for url in urls:
        parse_page(url)
    ALL_DATA.sort(key=lambda data:int(data['hight_temp']))
    data = ALL_DATA[0:10]
    chart = Bar("八月中国那里最凉快")
    cities=list(map(lambda x:x['city'],data))
    temp = list(map(lambda x:x['hight_temp'],data))
    chart.add('',cities,temp)
    chart.render('temp.html')
if __name__ == '__main__':
    main()