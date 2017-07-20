import requests
import os
from bs4 import BeautifulSoup
import threading
import time

state_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\state'
info_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\info_list'
sex_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\sex_list'
tieba_names = ['橙光', '女装子', '李毅', '贴吧娱乐', '吴亦凡', '多肉', '美剧', '鹿晗', '显卡']

class TiebaInfoBeatle():

    def __init__(self, name):
        self.com_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}
        self.folder_path=r'C:\tieba\info'
        self.tieba_url = 'https://tieba.baidu.com'
        self.tieba_name = name
    def request(self, url):
        res = requests.get(url, self.com_header)
        return res

    def request(self, url, header):
        res = requests.get(url, header)
        return res

    def mkdir(self, path):
        path = path.strip()  # delete char at top and bottom, if (), delete nothing
        isExists = os.path.exists(path)
        if not isExists:
            print('Creating named"' + path + '" folder')
            os.makedirs(path)
            print('Complete!')
        else:
            print('Folder is exists!')

    def infoFind(self, a):
        ap = a.parent
        userA = None
        if ap is not None:
            user_line = ap.next_sibling
            if user_line is not None:
                span1 = user_line.find('span')
                if span1 is not None:
                    span2 = span1.find('span')
                    if span2 is not None:
                        userA = span2.find('a')
        if(userA == None):
            return None
        user_href = userA['href']
        user_url = self.tieba_url + user_href
        user_res = requests.get(user_url, self.com_header)
        span = BeautifulSoup(user_res.text, 'html.parser').find('span', class_='user_name')
        return span

    def ageFind(self, a):
        span = self.infoFind(a)
        if span is not None:
            userS = str(span)
            first_pos = userS.index('吧龄:') + 3
            second_pos = userS.find('年', first_pos)
            if second_pos != -1:
                age = float(userS[first_pos: second_pos])
            else:
                age = 0.0
            return age

    def postFind(self, a):
        span = self.infoFind(a)
        if span is not None:
            userS = str(span)
            #print(userS)
            first_pos = userS.find(r'发贴:') + 3
            second_pos = userS.find(r'万', first_pos)
            if second_pos == -1:
                second_pos = userS.find(r'<', first_pos)
                post = int(userS[first_pos: second_pos])
            else:
                post = int(float(userS[first_pos: second_pos]) * 10000)
            return post

    def sexFind(self, a):
        div = self.infoFind(a).parent
        if div is not None:
            if div.find('span',{"class":"userinfo_sex userinfo_sex_male"}) is not None:
                #print('m')
                return 'male'
            else:
                #print('f')
                return 'female'

    def get_title(self):

        print('Making directory folder')
        self.mkdir(self.folder_path)

        print('Change to target folder')
        os.chdir(self.folder_path)

        print('Requesting...')
        total = 0
        info_list = []
        sex_list = []

        for page in range(0,50):
            if s.stop is False:
                time.sleep(10)
                continue
            else:
                tieba_header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
                    'kw': self.tieba_name, 'ie': 'utf-8', 'pn': str(page * 50)}
                bar_url = self.tieba_url + '/f'
                res = self.request(bar_url, tieba_header)
                all_a = BeautifulSoup(res.text, 'html.parser').find_all('a', class_='j_th_tit ')
                total += len(all_a)
                for a in all_a:
                    ag = self.ageFind(a)
                    po = self.postFind(a)
                    if ag and po is not None:
                        info_set = []
                        info_set.append(ag)
                        info_set.append(po)
                        info_list.append(info_set)
                        sex_list.append(self.sexFind(a))
                    print(a['title'])

        print(info_list)
        print(sex_list)

        #save = pickle.dumps(model)
        try:
            info_file_object = open(info_add, 'a')
            sex_file_object = open(sex_add, 'a')
            info_file_object.write(str(info_list))
            sex_file_object.write(str(sex_list))
            info_file_object.close()
            sex_file_object.close()
        except Exception as e:
            print(e)


class ThreadCrawl(threading.Thread):
    def __init__(self, tieba_name):
        threading.Thread.__init__(self)
        self.name = tieba_name

    def run(self):
        exe = TiebaInfoBeatle(self.name)
        exe.get_title()


class ThreadState(threading.Thread):
    def __inti__(self, stop):
        threading.Thread.__init__(self)
        self.stop = True

    def run(self):
        while True:
            state = open(state_add, 'r').read()
            if state is not '1':
                self.stop = False
                state.close()
            else:
                state.close()
            time.sleep(10)


threads = []
for i in range(5):
    t = ThreadCrawl(p_name)
    threads.append(t)
s = ThreadState()
threads.append(s)


for i in range(len(tieba_names)):
    threads[i].start()
for i in range(len(tieba_names)):
    threads[i].join()

