from queue import Queue
import requests
from bs4 import BeautifulSoup
import threading
import time
import pymysql
from pymysql.err import IntegrityError
from TheBeatles.parameter import host, user, passwd, db, tieba_names, firefox_title

thread_limit = 4

class TiebaInfoBeatle():

    def __init__(self, name, num):
        self.com_header = {'User-Agent': firefox_title}
        self.folder_path=r'C:\tieba\info'
        self.tieba_url = 'https://tieba.baidu.com'
        self.tieba_name = name
        self.thread_num = num

    def request(self, url, header):
        try:
            res = requests.get(url, header)
            return res
        except Exception as e:
            print('Can not get response!')
            print(e)
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
            tieba_header = {
                'User-Agent': firefox_title,
                'kw': self.tieba_name, 'ie': 'utf-8', 'pn': str(0)}
            bar_url = self.tieba_url + '/f'
            res = self.request(bar_url, tieba_header)
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
            return 2
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
        cursor.execute("update state set val = 1 where id = 0;")
        conn.commit()

    def get_title(self):

        print('Getting connection with database.....')
        conn = pymysql.connect(host=host, user=user, password=passwd, db=db, charset='UTF8')
        cursor = conn.cursor()

        print('Requesting tieba of ' + self.tieba_name)
        cursor.execute("update state set name = '{tieba}' where id = {num};".format(tieba=self.tieba_name, num=self.thread_num + 2))
        conn.commit()
        total = 0
        sex_list = []
        info_list = []
        calculated_page = self.calc_page()

        for page in range(calculated_page):
            tieba_header = {
                'User-Agent': firefox_title,
                'kw': self.tieba_name, 'ie': 'utf-8', 'pn': str(page * 50)}
            bar_url = self.tieba_url + '/f'
            res = self.request(bar_url, tieba_header)
            if res is None:
                continue
            soup = BeautifulSoup(res.text, 'html.parser')
            all_a = soup.find_all('a', class_='j_th_tit ')



            total += len(all_a)
            for a in all_a:
                if s.stop is True:
                    while s.stop:
                        print('Thread engaging information of tieba of ' + self.tieba_name + ' is pausing.....')
                        time.sleep(5)
                else:
                    internet_pointer = threading.Timer(20, self.set_exit, (conn, cursor))
                    internet_pointer.start()
                    span = self.infoFind(a)

                    if a is None:
                        continue

                    ag = self.ageFind(span)
                    po = self.postFind(span)
                    na = self.nameFind(span)

                    internet_pointer.cancel()
                    if ag and po and na is not None:
                        info_set = []
                        info_set.append(ag)
                        info_set.append(po)
                        info_list.append(info_set)
                        se = self.sexFind(span)
                        sex_list.append(se)
                        try:
                            cursor.execute("INSERT into test_hz.tieba_db (user_name, title, age, amount, sex) values ('{sql_user_name}', '{sql_title}', {sql_age}, {sql_amount}, '{sql_sex}');".format(sql_user_name=na, sql_title=a['title'], sql_age=ag,sql_amount=po, sql_sex=se))
                            conn.commit()
                        except IntegrityError as ie:
                            print('This user is duplicated, this information will not save again!')
                            conn.commit()
                            continue
                        except Exception as e:
                            print(
                                'There are some invalid character in the name or title. anonymous and no_title will added as name and title!')
                            cursor.execute("select val from state where id = 1")
                            anonymous_num = cursor.fetchone()[0] + 1
                            cursor.execute(
                                "INSERT into test_hz.tieba_db (user_name, title, age, amount, sex) values ('{sql_user_name}', '{sql_title}', {sql_age}, {sql_amount}, '{sql_sex}');".format(
                                    sql_user_name='Anonymous' + str(anonymous_num), sql_title='no_title', sql_age=ag, sql_amount=po,
                                    sql_sex=se))
                            cursor.execute("update state set val = {new} where name = 'An_id'".format(new=anonymous_num))
                            conn.commit()
                            continue
                        #finally:
                            #cursor.close()
                            #conn.close()

                    print(a['title'])

        print(info_list)
        print(sex_list)
        cursor.close()
        conn.close()

class ThreadCrawl(threading.Thread):

    def __init__(self, num):
        threading.Thread.__init__(self)
        self.id = num

    def run(self):
        while True:
            if name_queue is None or name_queue.empty() is True:
                break
            exe = TiebaInfoBeatle(name_queue.get(), self.id)
            try:
                print('This is thread ' + str(self.id))
                exe.get_title()
            except Exception as e:
                print('Unexpectable thread stop!')
                print(e)
                continue


class ThreadState(threading.Thread):

    stop = False

    def __inti__(self):
        threading.Thread.__init__(self)

    def run(self):
        conn = pymysql.connect(host=host, user=user, password=passwd, db=db, charset='UTF8')
        cursor = conn.cursor()
        thread_amount = len(threads) - 1
        while True:
            cursor.execute("SELECT val from state where id = 0;")
            result = cursor.fetchone()[0]

            if result == 0:
                self.stop = False
            else:
                self.stop = True
            time.sleep(1)
            conn.commit()

# First send all tieba names which will construct url into queue
threads = []
name_queue = Queue()
for t_name in tieba_names:
    name_queue.put(t_name)


# Then open (n+1) threads, 1 for opration like pause and add, n for crawl
s = ThreadState()

s.setDaemon(True)
threads.append(s)
s.start()
time.sleep(1)

conn = pymysql.connect(host=host, user=user, password=passwd, db=db, charset='UTF8')
cursor = conn.cursor()

for thread_num in range(thread_limit):
    cursor.execute("insert into state (id, name, val) values ({num}, 'no_state', 0);".format(num=thread_num+2))
    conn.commit()
    t = ThreadCrawl(thread_num)
    threads.append(t)
    t.start()
    time.sleep(0.3)

cursor.close()
conn.close()

for i in range(thread_limit + 1):
    threads[i].join()

