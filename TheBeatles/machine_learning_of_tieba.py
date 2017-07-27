import pymysql
import threading
from sklearn.tree import DecisionTreeClassifier
from TheBeatles.parameter import host, user, passwd, db, example_sample

class ThreadML(threading.Thread):

    conn = None
    cursor = None

    def __init__(self, sample_percent):
        threading.Thread.__init__(self)
        self.info_fit_list = []
        self.sex_fit_list = []
        self.info_predict_list = []
        self.sex_verification_list = []
        self.fit_sample_percent = sample_percent

    def get_file_from_db(self):
        print('Reading file...')
        try:
            self.cursor.execute("SELECT * FROM test_hz.tieba_db;")
            result = self.cursor.fetchall()

            for i in range(int(len(result) * self.fit_sample_percent)):
                r = result[i]
                info_set = []
                info_set.append(r[2])
                info_set.append(r[3])
                self.info_fit_list.append(info_set)
                self.sex_fit_list.append(r[4])
            for i in range(int(len(result) * (1 - self.fit_sample_percent))):
                r = result[int(len(result) * self.fit_sample_percent) + i]
                info_set = []
                info_set.append(r[2])
                info_set.append(r[3])
                self.info_predict_list.append(info_set)
                self.sex_verification_list.append(r[4])

        except Exception as e:
            print(e)

    def set_conn(self):
        self.conn = pymysql.connect(host=host, user=user, password=passwd, db=db, charset='UTF8')
        self.cursor = self.conn.cursor()

    def run(self):
        self.set_conn()
        self.get_file_from_db()
        tieba_sex_model = DecisionTreeClassifier()
        tieba_sex_model.fit(self.info_fit_list, self.sex_fit_list)
        print(tieba_sex_model.predict(example_sample))
        sex_predict_list = tieba_sex_model.predict(self.info_predict_list)
        print(sex_predict_list)
        print(self.sex_verification_list)
        count = 0
        for i in range(min(len(sex_predict_list), len(self.sex_verification_list))):
            if sex_predict_list[i] == self.sex_verification_list[i]:
                count += 1
        out = 'Correct:', str(count) + '; Total:', str(len(sex_predict_list)) + '; Accuracy:', count/len(sex_predict_list)
        print(out)
        self.cursor.execute("update state set outcome='{result}' where id = 2;".format(result=out))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()