from sklearn.tree import DecisionTreeClassifier
import pymysql
from TheBeatles.parameter import host, user, passwd, db

example_sample = [[0.1, 1300], [4.4, 1617], [2.3, 5932], [0.1, 88], [0.7, 10], [2.2, 47]]  # mmffmm
info_fit_list = []
sex_fit_list = []
info_predict_list = []
sex_verification_list = []
fit_sample_percent = 0.8


def fit(source, target):
    model = DecisionTreeClassifier()
    model = model.fit(source, target)
    return model


def predict(model, sample):
    return model.predict(sample)


def get_file_from_db():
    print('Reading file...')
    try:
        cursor.execute("SELECT * FROM test_hz.tieba_db;")
        result = cursor.fetchall()

        for i in range(int(len(result) * fit_sample_percent)):
            r = result[i]
            info_set = []
            info_set.append(r[2])
            info_set.append(r[3])
            info_fit_list.append(info_set)
            sex_fit_list.append(r[4])
        for i in range(int(len(result) * (1 - fit_sample_percent))):
            r = result[int(len(result) * fit_sample_percent) + i]
            info_set = []
            info_set.append(r[2])
            info_set.append(r[3])
            info_predict_list.append(info_set)
            sex_verification_list.append(r[4])

    except Exception as e:
        print(e)

conn = pymysql.connect(host=host, user=user, password=passwd, db=db, charset='UTF8')
cursor = conn.cursor()
get_file_from_db()

tieba_sex_model = fit(info_fit_list, sex_fit_list)
print(predict(tieba_sex_model, example_sample))
print(predict(tieba_sex_model, info_predict_list))
print(sex_verification_list)
'''
print(info_fit_list)
print(sex_fit_list)
'''
cursor.close()
conn.close()