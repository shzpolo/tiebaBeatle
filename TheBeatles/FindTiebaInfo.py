import requests
import threading
import time
import pymysql
from queue import Queue
from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout
from pymysql.err import IntegrityError
from TheBeatles.parameter import host, user, passwd, db, name_queue

name_list = name_queue
mutex = threading.Lock()

class TiebaInfoBeatle():

    def __init__(self, name, num):
        self.com_header = {'dummy': 'foo'}
        self.folder_path=r'C:\tieba\info'
        self.tieba_url = 'https://tieba.baidu.com'
        self.tieba_name = name
        self.thread_num = num

    def request(self, url, payload):
        try:
            res = requests.get(url, params=payload, timeout=5)
            res.raise_for_status()
            return res
        except ConnectTimeout as ce:
            print('Can not get response!')
            print(ce)
            return None
        except requests.exceptions.RequestException as re:
            print(re)
            return None

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
        user_res = self.request(user_url, self.com_header)
        if user_res is None:
            return None
        span = BeautifulSoup(user_res.text, 'html.parser').find('span', class_='user_name')
        return span

    def ageFind(self, user_personal_span):
        span = user_personal_span
        if span is not None:
            userS = str(span)
            first_pos = userS.index('吧龄:') + 3
            second_pos = userS.find('年', first_pos)
            if second_pos != -1:
                age = float(userS[first_pos: second_pos])
            else:
                age = 0.0
            return age

    def nameFind(self, user_personal_span):
        span = user_personal_span
        if span is not None:
            userS = str(span)
            first_pos = userS.index('户名:') + 3
            second_pos = userS.find('<', first_pos)
            return userS[first_pos: second_pos]


    def postFind(self, user_personal_span):
        span = user_personal_span
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

    def sexFind(self, user_personal_span):
        div = user_personal_span.parent
        sex_span = div.find('span')

        if sex_span is not None:
            if sex_span['class'][1] == 'userinfo_sex_male':
                #print('m')
                return 'male'
            else:
                #print('f')
                return 'female'

    def calc_page(self):
        try:
            tieba_payload = {'kw': self.tieba_name, 'ie': 'utf-8', 'pn': str(0)}
            bar_url = self.tieba_url + '/f'
            res = self.request(bar_url, tieba_payload)
            soup = BeautifulSoup(res.text, 'html.parser')
            if soup.find('h2', class_='icon-attention'):
                return 0
            titles = soup.find('span', class_='red_text')
            if(titles == None):
                print('Internet situation bad.')
                return 50
            mains = titles.text
        except:
            print('Page get error!')
            return 10
        print('Calculating...')
        try:
            mains = float(mains)
            mains /= 50
            mains = int(mains)
            print('Total pages are ' + str(mains))
            return (mains - 1)
        except:
            print('Final 10')
            return 10

    def set_exit(self, conn, cursor):
        print('Internet state is awful! Suggest wait a moment.')
        print('System automatically change state to stop, if you want to continue, please'
              ' open it again.')
        cursor.execute("update state set amount = 1 where id = 0;")
        conn.commit()

    def if_user_name_duplicate(self, a, cursor, conn):
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
        if userA is None:
            print('This user cannot access. Going to next one.')
            return True
        name = userA.text
        cursor.execute("select id from tieba_db where user_name='{user_name}'".format(user_name=name))
        conn.commit()
        user_id = cursor.fetchone()
        if user_id is None:
            return False
        else:
            print('This user is duplicated. Going to next one.')
            return True

    def get_title(self, controller):

        print('Getting connection with database.....')
        conn = pymysql.connect(host=host, user=user, password=passwd, db=db, charset='UTF8')
        cursor = conn.cursor()

        print('Requesting tieba of ' + self.tieba_name)
        cursor.execute("update state set name = '{tieba}' where id = {num};".format(tieba=self.tieba_name, num=self.thread_num + 3))
        conn.commit()
        total = 0
        sex_list = []
        info_list = []
        calculated_page = min(self.calc_page(), 1000)

        for page in range(calculated_page):
            tieba_payload = {'kw': self.tieba_name, 'ie': 'utf-8', 'pn': str(page*50)}
            bar_url = self.tieba_url + '/f'
            res = self.request(bar_url, tieba_payload)
            if res is None:
                continue
            soup = BeautifulSoup(res.text, 'html.parser')
            all_a = soup.find_all('a', class_='j_th_tit ')



            total += len(all_a)
            for a in all_a:
                if controller.is_stop():
                    while controller.is_stop():
                        print('Thread engaging information of tieba of ' + self.tieba_name + ' is pausing.....')
                        time.sleep(5)
                elif a is None or self.if_user_name_duplicate(a, cursor, conn):
                    continue
                else:

                    internet_pointer = threading.Timer(20, self.set_exit, (conn, cursor))
                    internet_pointer.start()
                    span = self.infoFind(a)
                    internet_pointer.cancel()

                    ag = self.ageFind(span)
                    po = self.postFind(span)
                    na = self.nameFind(span)


                    if ag and po and na is not None:
                        info_set = []
                        info_set.append(ag)
                        info_set.append(po)
                        info_list.append(info_set)
                        se = self.sexFind(span)
                        sex_list.append(se)
                        mutex.acquire()
                        cursor.execute("select val from state where id = 1")
                        now_id = cursor.fetchone()[0] + 1
                        mutex.release()
                        try:
                            cursor.execute("INSERT into test_hz.tieba_db (user_name, title, age, amount, sex, id) values ('{sql_user_name}', '{sql_title}', {sql_age}, {sql_amount}, '{sql_sex}', {sql_id});"
                                           .format(sql_user_name=na, sql_title=a['title'], sql_age=ag,sql_amount=po, sql_sex=se, sql_id=now_id))
                            cursor.execute("update state set val = {new} where id = 1".format(new=now_id))
                            conn.commit()
                        except IntegrityError as ie:
                            print('This user is duplicated, this information will not save again!')
                            conn.commit()
                            continue
                        except Exception as e:
                            mutex.acquire()
                            print(
                                'There are some invalid character in the name or title. anonymous and no_title will added as name and title!')
                            print(e)
                            cursor.execute("select amount from state where id = 1")
                            anonymous_num = cursor.fetchone()[0] + 1
                            cursor.execute(
                                "INSERT into test_hz.tieba_db (user_name, title, age, amount, sex, id) values ('{sql_user_name}', '{sql_title}', {sql_age}, {sql_amount}, '{sql_sex}', {sql_id});".format(
                                    sql_user_name='Anonymous' + str(anonymous_num), sql_title='no_title', sql_age=ag, sql_amount=po,
                                    sql_sex=se, sql_id = now_id))
                            cursor.execute("update state set amount = {new} where id = 1".format(new=anonymous_num))
                            cursor.execute("update state set val = {new} where id = 1".format(new=now_id))
                            conn.commit()
                            mutex.release()
                            continue

                    print(a['title'])

        print(info_list)
        print(sex_list)
        cursor.close()
        conn.close()

class ThreadCrawl(threading.Thread):

    def __init__(self, num, controller):
        threading.Thread.__init__(self)
        self.id = num
        self.controller = controller

    def run(self):
        global name_list, mutex
        while True:
            if name_list is None or name_list.empty() is True:
                break
            mutex.acquire()
            exe = TiebaInfoBeatle(name_list.get(), self.id)
            mutex.release()
            print('This is thread ' + str(self.id))
            exe.get_title(self.controller)
'''
            try:
                print('This is thread ' + str(self.id))
                exe.get_title(self.controller)
            except Exception as e:
                print('Unexpectable thread stop!')
                print(e)
                continue
                '''

