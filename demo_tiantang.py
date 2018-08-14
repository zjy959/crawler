import requests
from lxml import etree
INDEX_URL = 'http://www.ygdy8.net'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'Referer':'http://www.dytt8.net/'
}
#获取每个a标签上电影详情url
def get_url(url):
    response = requests.get(url,headers=headers)
    # text = response.content.decode('gbk')网站一些字符不能解码
    text = response.text
    html = etree.HTML(text)
    movies = html.xpath('//table[@class="tbspan"]//a/@href')
    # for movie in movies:
    #     movie_url = movie.xpath('.//a/@href')[0]
    #     movie_url2 =INDEX_URL + movie_url
    #     print(movie_url2)
    movies_url = map(lambda a_url:INDEX_URL+a_url,movies)
    return movies_url


def parse_detail_page(url):
    movie = {}
    movie_page = requests.get(url,headers=headers)
    text = movie_page.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath('//div[@class="title_all"]//font[@color="#07519a"]/text()')[0]
    movie['title']=title
    zoomE = html.xpath('//div[@id="Zoom"]')[0]
    covers = zoomE.xpath('.//img/@src')
    cover = covers[0]
    screenshot = covers[len(covers)-1]
    movie['cover'] = cover
    movie['screenshot'] = screenshot
    infos = zoomE.xpath('.//text()')
    def parse_info(info,relu):
        return info.replace(relu,"").strip()
    for index,info in enumerate(infos):
        if info.startswith('◎年　　代'):
            year = parse_info(info,'◎年　　代')
            movie['year'] = year
        elif info.startswith('◎产　　地'):
            country = parse_info(info,'◎产　　地')
            movie['country'] = country
        elif info.startswith('◎类　　别'):
            info = parse_info(info,'◎类　　别')
            movie['category'] = info
        elif info.startswith('◎豆瓣评分'):
            info = parse_info(info,'◎豆瓣评分')
            movie['douban_rating'] = info
        elif info.startswith('◎片　　长'):
            info = parse_info(info,'◎片　　长')
            movie['duration'] = info
        elif info.startswith('◎导　　演'):
            info = parse_info(info,'◎导　　演')
            movie['director'] = info
        elif info.startswith('◎主　　演'):
            info = parse_info(info,'◎主　　演')
            actors = [info]
            for x in range(index+1,len(infos)):
                actor = infos[x].strip()
                if actor.startswith('◎'):
                    break
                actors.append(actor)
            movie['actors'] = actors

        elif info.startswith('◎简　　介 '):
            info = parse_info(info,'◎简　　介 ')
            profiles = []
            for x in range(index + 1, len(infos)):
                profile = infos[x].strip()
                if profile.startswith('【下载地址】'):
                    break
                profiles.append(profile)
                movie['profiles'] = profiles

    download_url = html.xpath('//td[@bgcolor="#fdfddf"]/a/@href')[0]
    movie['download_url'] = download_url
    return movie

#获取页数url
def page_url():
    f_url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html'
    movies = []
    for x in range(1,8):
        p_url = f_url.format(x)
        movie_urls = get_url(p_url)
        for detail_url in movie_urls:
            #获取每一页下面所有电影详情url
            movie=parse_detail_page(detail_url)
            movies.append(movie)
            print(movie)
if __name__ == '__main__':
    page_url()
