'''
测试使用selenium的创建的翻页功能
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from pyquery import PyQuery as pq

browser = webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver.exe')
wait = WebDriverWait(browser,10)   #显式等待

def get_next_page(num):
    url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=6'
    browser.get(url)

    try:
        print('翻到第%d页'%num)
        input = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"page")))
        input.clear()
        input.send_keys(num)
        input.send_keys(Keys.ESCAPE)     #输入回车键
        time.sleep(5)                    #等待ajax加载完成
    except TimeoutError as e:
        print(e)

if __name__ == '__main__':
    for num in range(1,5):
        get_next_page(num)
