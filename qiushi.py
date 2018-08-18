import requests
import re

def parse_url(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    text = response.text
    authors = re.findall(r'<div class="author clearfix">.*?<img.*? alt="(.*?)">',text,re.DOTALL)
    contents_tags = re.findall(r'<div class="content">.*?<span>(.*?)</span>',text,re.DOTALL)
    inter_num = re.findall(r'<span class="stats-vote">.*?<i class="number">(.*?)</i>',text,re.DOTALL)
    contents = []
    duanzis = []
    for content in contents_tags:
        x = re.sub(r'<.*?>',"",content)
        contents.append(x.strip())
    for valua in zip(authors,contents,inter_num):
        author,content,inter_num = valua
        duanzi = {
            'author':author,
            'content':content,
            'inter_num':inter_num
        }
        duanzis.append(duanzi)
    for duanzi in duanzis:
        print(duanzi)
def main():
    url = 'https://www.qiushibaike.com/text/page/1/'
    parse_url(url)

if __name__ == '__main__':
    main()
