import requests
from bs4 import BeautifulSoup

url_pre = 'http://tieba.baidu.com/f/index/forumpark?cn=&ci=0&pcn='
url_bac = '&pci=0&ct=1&st=new&pn='
names = ['娱乐明星','电视节目','电视剧','电影','体育迷','小说','生活家','闲·趣','游戏','动漫宅','高等院校','地区','人文自然']
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}
tieba_names = []

print(str(12*30*19))

for name in names:
    for i in range(2):
        url = url_pre + name + url_bac + str(i)
        res = requests.get(url, headers = header)
        soup = BeautifulSoup(res.text, 'html.parser')
        all_name = soup.find_all('p', class_='ba_name')
        for n in all_name:
            tieba_names.append(n.text[:-1])

print(tieba_names)
print(len(tieba_names))



