import requests,pymongo
from lxml import etree
import time
import re

client = pymongo.MongoClient("127.0.0.1",port=27017)
db = client.LG_python
collection = db.qa


url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Referer':'https://www.lagou.com/jobs/list_pyhton?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
    'Cookie':'_ga=GA1.2.375530964.1535975029; user_trace_token=20180903194338-9964a99d-af6e-11e8-8570-525400f775ce; LGUID=20180903194338-9964b209-af6e-11e8-8570-525400f775ce; _gid=GA1.2.344236421.1535975029; LG_LOGIN_USER_ID=152df2075669be5154c736fdbd4d7df5fe39605607a41136d4477d9436ce8377; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; index_location_city=%E6%B7%B1%E5%9C%B3; WEBTJ-ID=20180904105026-165a27d0403197-0e7269cf0f339f-323b5b03-2073600-165a27d040463c; _gat=1; LGSID=20180904105017-4166eff5-afed-11e8-8594-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E6%258B%2589%25E9%2592%25A9%25E7%25BD%2591%26rsv_spt%3D1%26rsv_iqid%3D0x8c4e7d3700007653%26issp%3D1%26f%3D3%26rsv_bp%3D1%26rsv_idx%3D2%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3D94112622_hao_pg%26rsv_enter%3D1%26oq%3D%2525E6%25258B%252589%2525E9%252592%2525A9%26rsv_t%3D4f7ftRnYcQXggs3pxqfoha7IYG0askOn265whe0lilpRI%252F5v6ml13cKlDQZGLjl4TD5xdyV6%26rsv_sug3%3D8%26rsv_sug1%3D7%26rsv_sug7%3D100%26rsv_pq%3Db70096df000053eb%26rsv_sug2%3D1%26prefixsug%3D%2525E6%25258B%252589%2525E9%252592%2525A9%26rsp%3D1%26rsv_sug4%3D682%26rsv_sug%3D1; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535975029,1536029427; _putrc=52F5B1CBE9DF0C8D123F89F2B170EADC; JSESSIONID=ABAAABAAADEAAFID1416A330BDF404896F8DCA964607503; login=true; unick=%E5%91%A8%E4%BF%8A%E5%AE%87; gate_login_token=485afdabf5ee2b1c6761a68b42685cfcafc4ba3110836f9c5a97dca856de53a4; SEARCH_ID=588b8f1097c04b73a35c6ca112c29734; LGRID=20180904105451-e5031cba-afed-11e8-b4e7-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536029701'
}
data={
    'first': 'true',
    'pn': 1,
    'kd': 'python'
}
def parse_url(url):
    response=requests.get(url,headers=headers)
    text = response.text
    html = etree.HTML(text)
    detail = {}
    job_name = html.xpath('//span[@class="name"]/text()')[0]
    job_request = html.xpath('//dd[@class="job_request"]//span')
    salary_span = job_request[0]
    salary = salary_span.xpath('./text()')[0].strip()
    city = job_request[1].xpath('./text()')[0].strip()
    city = re.sub(r'[\s/]','',city)
    work_years = job_request[2].xpath('./text()')[0].strip()
    work_years = re.sub(r'[\s/]','',work_years)
    education = job_request[3].xpath('./text()')[0].strip()
    education = re.sub(r'[\s/]','',education)
    desc = ''.join(html.xpath('//dd[@class="job_bt"]//text()')).strip()
    detail = {
        'job_name':job_name,
        'salary':salary,
        'city':city,
        'work_years':work_years,
        'education':education,
        'desc':desc
    }
    print(detail)
    collection.insert(detail)
def requests_url():
    for x in range(1,11):
        data['pn'] = x
        response = requests.post(url,data=data,headers=headers)
        text = response.json()
        positions = text['content']['positionResult']['result']
        for position in positions:
            positionID=position['positionId']
            position_url = 'https://www.lagou.com/jobs/%s.html'% positionID
            parse_url(position_url)
            break
        break
if __name__ == '__main__':
    requests_url()