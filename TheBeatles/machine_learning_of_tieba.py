from sklearn.tree import DecisionTreeClassifier

info_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\info_list'
sex_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\sex_list'
example_sample = [[0.1, 1300], [4.4, 1617], [2.3, 5932], [0.1, 88], [0.7, 10], [2.2, 47]]  # mmffmm


def fit(source, target):
    model = DecisionTreeClassifier()
    model = model.fit(source, target)
    return model


def predict(model, sample):
    return model.predict(sample)


def get_file_from_txt(file_add):
    print('Reading file...')
    f = open(file_add, 'r')
    file = f.read()
    print("File information is " + file)
    return file


#def translate_info(file):



info_list = get_file_from_txt(info_add)
sex_list = get_file_from_txt(sex_add)

tieba_sex_model = fit(info_list, sex_list)
print(predict(tieba_sex_model, example_sample))