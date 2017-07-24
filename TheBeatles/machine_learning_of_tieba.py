from sklearn.tree import DecisionTreeClassifier
import pymysql

info_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\info_list'
sex_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\sex_list'
host = '172.17.60.108'
user = 'hz'
passwd = 'hz123456'
db = 'test_hz'
example_sample = [[0.1, 1300], [4.4, 1617], [2.3, 5932], [0.1, 88], [0.7, 10], [2.2, 47]]  # mmffmm
info_list = []
sex_list = []

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
        for r in result:
            info_set = []
            info_set.append(r[2])
            info_set.append(r[3])
            info_list.append(info_set)
            sex_list.append(r[4])
    except Exception as e:
        print(e)

conn = pymysql.connect(host='172.17.60.108', user=user, password=passwd, db=db, charset='UTF8')
cursor = conn.cursor()
get_file_from_db()

tieba_sex_model = fit(info_list, sex_list)
print(predict(tieba_sex_model, example_sample))