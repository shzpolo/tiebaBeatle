import requests
from bs4 import BeautifulSoup

url_pre = 'http://tieba.baidu.com/f/index/forumpark?pcn='
url_bac = '&pci=429&ct=0&rn=20&pn='
names = ['娱乐明星','爱综艺','追剧狂','看电影','体育小说','生活家','闲·趣','游戏','动漫宅','高校','地区','人文自然']
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}

for name in names:
    res = requests(url_pre+name+url_bac, headers = header)


