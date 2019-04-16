from bs4 import BeautifulSoup as bs
import requests as request
import time

url = 'https://movie.douban.com/top250'
path = 'C:/Users/jkw/Desktop/新建文件夹/'
i = 0
while i <= 225:
    soup = bs(request.get('%s?start=%s&filter='%(url,i)).text)
    print(url+'?start=%s&filter='%i)
    for item in soup.select('.grid_view li .item .pic a img'):
        picurl = item.get('src')
        name = path + item.get('alt') + '.jpg'
        print(name)
        r = request.get(picurl)
        with open(name, 'wb') as f:
            f.write(r.content)
    time.sleep(3)
    i=i+25