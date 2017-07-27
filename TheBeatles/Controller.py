from queue import Queue
import threading
import pymysql
import time
from TheBeatles.parameter import host, user, passwd, db
import TheBeatles.FindTiebaInfo as crawl
import TheBeatles.machine_learning_of_tieba as ml


class Controller():

    conn = None
    cursor = None

    def __init__(self, *num):
        self.thread_amount = 5
        for limit_num in num:
            self.set_thread_amount(limit_num)
        self.stop = False
        self.sample_percent = 0.8
        self.crawl_threads = []
        self.monitor_thread = None
        self.create_connection_of_mysql()

    def set_thread_amount(self, num):
        self.thread_amount = num

    def get_thread_amount(self):
        return self.thread_amount

    def is_stop(self):
        return self.stop

    def find_if_stop(self, cursor, conn):
        cursor.execute("SELECT amount from state where id = 0;")
        result = cursor.fetchone()[0]

        if result == 0:
            self.stop = False
        else:
            self.stop = True
        time.sleep(1)
        conn.commit()

    def start_predict(self, cursor, conn):
        print('System find you want to use data in database to predict.')
        self.set_sample_percent(cursor, conn)
        ml_thread = ml.ThreadML(self.sample_percent)
        ml_thread.start()

    def set_sample_percent(self, cursor, conn):
        print('System find you want to see the last tieba titles.')
        cursor.execute("SELECT val from state where id = 0;")
        new_percent = cursor.fetchone()[0] / 100
        if new_percent >= 1 or new_percent <= 0:
            print('Your new rate is invalid.')
        else:
            self.sample_percent = new_percent
            print('Success!')
        conn.commit()

    def find_last_titles(self, cursor, conn):
        print('System find you want to see the last tieba titles.')
        cursor.execute("SELECT amount from state where id = 1;")
        now_id = cursor.fetchone()[0]
        titles = []
        conn.commit()
        for i in range(10):
            cursor.execute("SELECT title from tieba_db where id = {id};".format(id=now_id-i))
            titles.append(cursor.fetchone()[0])
        conn.commit()
        print(titles)
        return titles

    def find_working_tieba(self, cursor, conn):
        print('System find you want to find out what tieba is crawling.')
        name_result = []
        for i in range(self.thread_amount):
            try:
                cursor.execute("SELECT name from state where id = {num};".format(num=i+3))
                result = cursor.fetchone()[0]
                name_result.append(result)
            except TypeError as te:
                print('No tieba is fetching.')
            conn.commit()
        print(name_result)
        return name_result

    def find_command(self, cursor, conn):
        cursor.execute("SELECT command_name from state where id = 0;")
        conn.commit()
        result = cursor.fetchone()[0]
        if result == 'start_predict':
            cursor.execute("update state set command_name='start' where id = 0;")
            conn.commit()
            self.start_predict(cursor, conn)
            cursor.execute("update state set command_name='idle' where id = 0;")
            conn.commit()
        elif result == 'last_titles':
            cursor.execute("update state set command_name='start' where id = 0;")
            conn.commit()
            outcome = self.find_last_titles(cursor, conn)
            cursor.execute("update state set outcome='{string}' where id = 0;".format(string=str(outcome)))
            cursor.execute("update state set command_name='idle' where id = 0;")
            conn.commit()
        elif result == 'working_tieba':
            cursor.execute("update state set command_name='start' where id = 0;")
            conn.commit()
            outcome = self.find_working_tieba(cursor, conn)
            cursor.execute("update state set outcome='{string}' where id = 0;".format(string=str(outcome)))
            cursor.execute("update state set command_name='finish' where id = 0;")
            conn.commit()
        else:
            pass

    def create_connection_of_mysql(self):
        self.conn = pymysql.connect(host=host, user=user, password=passwd, db=db, charset='UTF8')
        self.cursor = self.conn.cursor()

    def start_monitor(self):
        while True:
            self.find_if_stop(self.cursor, self.conn)
            self.find_command(self.cursor, self.conn)
            print('Controller is monitoring.............')
            time.sleep(5)

    def start_crawl(self):
        for thread_num in range(self.thread_amount):

            try:
                self.cursor.execute(
                "insert into state (id, name, val) values ({num}, 'no_state', 0);".format(num=thread_num + 3))
            except pymysql.err.IntegrityError:
                self.cursor.execute(
                "update state set name='no_title' where id = {num};".format(num=thread_num + 3))
            finally:
                self.conn.commit()

            thread = crawl.ThreadCrawl(thread_num, self)
            self.crawl_threads.append(thread)
            thread.setDaemon(True)
            time.sleep(0.5)

    def run(self):
        self.monitor_thread = threading.Thread(target=self.start_monitor)
        self.start_crawl()
        for thread in self.crawl_threads:
            thread.start()
        self.monitor_thread.start()
        self.monitor_thread.join()
        for thread in self.crawl_threads:
            thread.join()




if __name__ == '__main__':
    c = Controller()
    c.run()