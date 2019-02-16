from selenium import webdriver
import time
from pyquery import PyQuery as pq

def get_page_source():
    url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=6'
    browser = webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver.exe')
    browser.get(url)
    time.sleep(10)
    html = browser.page_source
    return html

def parse_with_pq(html):
    doc = pq(html)
    for item in doc.items('#list-books'):
        print(item)

if __name__ == '__main__':
    html = get_page_source()
    parse_with_pq(html)