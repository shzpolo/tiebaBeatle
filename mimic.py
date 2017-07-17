from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # as the function of keyboard
import time


url = 'https://m.weibo.com/'
driver = webdriver.PhantomJS(r'C:\tieba\phantomjs-2.1.1-windows\bin\phantomjs.exe')

def scroll_down(driver, times):
    for i in range(times):
        print("开始执行第", str(i + 1), "次下拉操作")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 执行JavaScript实现网页下拉倒底部
        print("第", str(i + 1), "次下拉操作执行完毕")
        print("第", str(i + 1), "次等待网页加载......")
        time.sleep(5)  # 等待x秒（时间可以根据自己的网速而定），页面加载出来再执行下拉操作


driver.get(url)
#print(driver.page_source)

print('go into main page')
login = driver.find_element_by_class_name('action').find_elements_by_tag_name('a')[1]
login.click()
time.sleep(10)

print('logging')
name = driver.find_element_by_id('loginName')
passwd = driver.find_element_by_id('loginPassword')
name.clear()
name.send_keys('shuhuanze@126.com')
passwd.clear()
passwd.send_keys('shz88265996')
icon = driver.find_element_by_id('loginAction')
icon.click()
time.sleep(20)

print('pushing search button')
search = driver.find_element_by_class_name('iconf_navbar_search')
search.click()
time.sleep(10)

print('searching')
search_bar = driver.find_element_by_name('queryVal')
search_bar.clear()
search_bar.send_keys('去睡觉')
search_bar.send_keys(Keys.RETURN)
time.sleep(20)

scroll_down(driver, 20)
all_time = BeautifulSoup(driver.page_source, 'html.parser').find_all('span', class_='time')

for time in all_time:
    print(time.text)
