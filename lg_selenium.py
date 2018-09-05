from selenium import webdriver
from lxml import etree
import re,time,csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class LagouSpider(object):
    driver_path = r"D:\chrome\chromedriver.exe"
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=LagouSpider.driver_path)
        self.url = 'https://www.lagou.com/jobs/list_python?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput='
        self.positions = []
        fp = open('lagou.csv','a',newline='',encoding='utf-8')
        self.writer = csv.DictWriter(fp,['job_name','company_name','salary','city','work_years','education','desc'])
        self.writer.writeheader()

# 请求招聘主页
    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            WebDriverWait(driver=self.driver,timeout=10).until(
                EC.presence_of_all_elements_located((By.XPATH,"//span[@action='next']"))
            )
            self.parse_list_page(source)
            next_btn = self.driver.find_element_by_xpath("//span[@action='next']")
            if "pager_next_disabled" in next_btn.get_attribute("class"):
                break
            else:
                next_btn.click()
            time.sleep(1)


# 获取职位详情页url
    def parse_list_page(self,source):
        html = etree.HTML(source)
        links = html.xpath('//a[@class="position_link"]/@href')
        for link in links:
            self.request_detail_page(link)
            time.sleep(1)

# 请求职位详情页
    def request_detail_page(self,url):
        self.driver.execute_script("window.open('%s')"%url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_all_elements_located((By.XPATH,"//span[@class='name']"))
        )
        source = self.driver.page_source
        self.parse_detail_page(source)
        #关闭当前这个详情页
        self.driver.close()
        #继续切换回职位列表页
        self.driver.switch_to.window(self.driver.window_handles[0])

 # 解析职位详情页
    def parse_detail_page(self,source):
        html = etree.HTML(source)
        job_name = html.xpath('//span[@class="name"]/text()')[0]
        job_request = html.xpath('//dd[@class="job_request"]//span')
        salary_span = job_request[0]
        salary = salary_span.xpath('./text()')[0].strip()
        city = job_request[1].xpath('./text()')[0].strip()
        city = re.sub(r'[\s/]', '', city)
        work_years = job_request[2].xpath('./text()')[0].strip()
        work_years = re.sub(r'[\s/]', '', work_years)
        education = job_request[3].xpath('./text()')[0].strip()
        education = re.sub(r'[\s/]', '', education)
        desc = ''.join(html.xpath('//dd[@class="job_bt"]//text()')).strip()
        company_name = html.xpath("//h2[@class='fl']/text()")[0].strip()
        detail = {
            'job_name': job_name,
            'company_name':company_name,
            'salary': salary,
            'city': city,
            'work_years': work_years,
            'education': education,
            'desc': desc
        }
        # self.positions.append(detail)
        # self.writer.writerows(detail)
        # print(detail)
        # print('='*30)
        self.write_position(detail)

    def write_position(self,position):
        self.writer.writerow(position)
        print(position)

if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()