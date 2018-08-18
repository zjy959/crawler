import requests
import re
# 解析网页
def parse_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    text = response.text
    title = re.findall(r'<div\sclass="cont">.*?<b>(.*?)</b>',text,re.DOTALL)
    dynasty = re.findall(r'<div\sclass="cont">.*?<p\sclass="source">.*?<a.*?>(.*?)</a>',text,re.DOTALL)
    authors = re.findall(r'<p\sclass="source".*?><a.*?>.*?</a><span>.*?</span><a.*?>(.*?)</a>',text,re.DOTALL)
    contents_tags = re.findall(r'<div\sclass="contson".*?>(.*?)</div>',text,re.DOTALL)
    contents = []
    peoms = []
    for content in contents_tags:
        x = re.sub(r'<.*?>',"",content)
        contents.append(x.strip())
    # 利用zip函数将以上列表组合新列表再提取每一项组成新的一个字典，再放入一个列表中
    for valua in zip(title,dynasty,authors,contents):
        title,dynasty,authors,contents = valua
        peom = {
            'title':title,
            'dynasty':dynasty,
            'authors':authors,
            'contents':contents
        }
        peoms.append(peom)
    for peom in peoms:
        print(peom)
        print('*'*30)


# 获取网页url
def main():
    for x in range(1,11):
        url = 'https://www.gushiwen.org/default_%s.aspx'%x
        parse_page(url)

if __name__ == '__main__':
    main()