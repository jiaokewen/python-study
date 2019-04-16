from bs4 import BeautifulSoup as bs
import requests as request


url = 'https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6'
text = request.get(url).text
soup = bs(text)
for tar in soup.select('#pl_top_realtimehot tbody a'):
    print(tar.get_text())