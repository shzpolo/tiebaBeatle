from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # as the function of keyboard
import time
import os


url = 'https://weibo.cn/'
cookie_save_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\cookie_save'
cookie_time_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\cookie_time'
time_list_save_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\time_list'
driver = webdriver.PhantomJS(r'C:\tieba\phantomjs-2.1.1-windows\bin\phantomjs.exe')


def start_driver(url):
    print('Going into main page ...')
    driver.get(url)
    time.sleep(10)

    login = driver.find_element_by_link_text('登录')
    login.click()
    time.sleep(10)


def login_get_cookie():
    print('logging .....')

    name = driver.find_element_by_id('loginName')
    passwd = driver.find_element_by_id('loginPassword')
    name.clear()
    name.send_keys('shuhuanze@126.com')
    passwd.clear()
    passwd.send_keys('shz88265996')
    driver.find_element_by_id('loginAction').click()
    cookies = driver.get_cookies()
    #print(cookies)
    cookie = ''
    for i in range(len(cookies)):
        buffer = cookies[i]['name'] + r'='+ cookies[i]['value'] + r';'
        cookie += buffer
    #print(cookie)
    time.sleep(20)
    return cookie


def save_file(file_add,file):  # save files
    try:
        print('Saving file...')
        f= open(file_add,'a')
        f.write(file)
        if file_add is r'C:\Users\Polo\PycharmProjects\test\ml_res\cookie_time':
            f.write('\n')
        f.close()
        print('OK')
    except Exception as e:
        print(e)
    finally:
        pass


def push_search_button():
    print('pushing search button')
    search = driver.find_element_by_class_name('iconf_navbar_search')
    search.click()
    time.sleep(10)


def search(search_txt):
    print('Searching ' + search_txt + '....')
    print(driver.page_source)
    search_bar = driver.find_element_by_name('keyword')
    search_bar.clear()
    search_bar.send_keys(search_txt)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(20)


def scroll_down(times):
    for i in range(times):
        print("This is the", str(i + 1) + "th scrolling down.")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 执行JavaScript实现网页下拉倒底部
        print(str(i + 1) + "th scroll down is complete.")
        print(str(i + 1) + "th waiting page response.")
        time.sleep(4)  # 等待x秒（时间可以根据自己的网速而定），页面加载出来再执行下拉操作


def get_time_list(page):
    time_list = []
    for i in range(page):
        print('This is the ' + str(i) +'th page.')
        all_time = BeautifulSoup(driver.page_source, 'html.parser').find_all('span', class_='ct')
        for s_time in all_time:
            if s_time.text.find('前') is not -1:
                continue
            colon = s_time.text.find(':')
            time_list.append(s_time.text[colon - 2: colon + 3])
            print(s_time.text[colon - 2: colon + 3])
        push_next_button()
    return time_list


def get_timestamp():
    try:
        tamp = time.time()
        timestamp = str(int(tamp)) + "000"
        print('Getting timestamp is ' + timestamp + '.')
        return timestamp
    except Exception as e:
        print(e)
    finally:
        pass


def get_file_from_txt(file_add):#从本地文件里读取cookie
    print('Reading file...')
    f = open(file_add, 'r')
    file = f.read()
    print("File information is " + file)
    return file


def is_valid_cookie(cookie_time_add):#判断cookie是否有效
    if os.path.isfile(cookie_time_add) is False:
        return False
    else:
        try:
            f = open(cookie_time_add)
            lines = f.readlines()
            if len(lines) is 0:
                return False
            else:
                last_time = lines[0]
                if int(get_timestamp()) - int(last_time) > 6*60*60*1000:
                    return False
                else:
                    return True
        except Exception as e:
            print(e)

def push_next_button():
    print('pushing next button....')
    next_page = driver.find_element_by_id('pagelist').find_element_by_tag_name('a')
    next_page.click()
    time.sleep(10)
'''
result = is_valid_cookie(cookie_time_add)
if result is False:
    start_driver(url)
    cookie = login_get_cookie()
    save_file(cookie_save_add, cookie)
    timestamp = get_timestamp()
    save_file(cookie_time_add, timestamp)
else:
    cookie = get_file_from_txt(cookie_save_add)
'''

start_driver(url)
login_get_cookie()
search('good night')
time_list = str(get_time_list(99))
save_file(time_list_save_add, time_list)

driver.get(url)
search('去睡了')
time_list = str(get_time_list(99))
save_file(time_list_save_add, time_list)

driver.get(url)
search('晚安')
time_list = str(get_time_list(99))
save_file(time_list_save_add, time_list)
