'''
将一本小说内容插入到MYSQL中
'''
import time
import pymysql
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#url = 'https://book.tianya.cn/chapter-83237-9175309'
#https://book.tianya.cn/chapter-89223  小说页面

# url = 'https://book.tianya.cn/chapter-89223'
browser = webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver.exe')

db = pymysql.connect(host='localhost', user='root', password='test123456', port=3306, db='spiders')
cursor = db.cursor()
sql = "INSERT INTO charpter(charpter_id,charpter_name,novel_id) values(%s,%s,%s)"

def get_100_novel_id():
    novel_ids = []
    sql = 'SELECT id FROM novel_info LIMIT 6066,6966'
    cursor.execute(sql) #result是共有多少条结果
    result = cursor.fetchall() #数据类型是元组,可迭代类型数据
    for data in result:
       novel_ids.append(data)

    return novel_ids

def make_novel_url(novel_ids):
    urls = []
    for id in novel_ids:
        url = 'https://book.tianya.cn/chapter-'+id[0]
        urls.append(url)
    return urls
#点击目录链接
def click_href(url):
    try:
        browser.get(url)
        wait = WebDriverWait(browser, 20)
        # 显示等待,小说页面加载完成
        content_click = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'directory'))).click()
        # browser.find_element_by_link_text('目录').click()
        time.sleep(4)
        contents = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'contents')))
        html = browser.page_source
        return html
    except:
        html = click_href(url)
        return html


def get_charpter_info_and_save(html):
    datas = []
    doc = pq(html)
    li_list=doc('.volume-list').children().children().items()
    for li in li_list:
        if '（免）' in li('.clearfix').attr('title')+li('.cfree').text():
            data={
                'charpter_id':li.attr('_cid'),
                'charpter_name':li('.clearfix').attr('title')+li('.cfree').text(),
                'novel_id' : doc('#main').attr('bookid')
            }
            # print(data)
            datas.append(data)
    # print('基本信息保存完成')
    return datas

#将数据插入到数据库
def save_to_MYSQL(new_datas):

    for data in new_datas:
        try:
            cursor.execute(sql, (data['charpter_id'],data['charpter_name'],data['novel_id']))
            db.commit()
            print('插入数据成功',data['charpter_name'])
        except Exception as e:
            print('插入数据失败！！',e)
            db.rollback()


if __name__ == '__main__':
    #组成url
    ids = get_100_novel_id()
    urls = make_novel_url(ids)
    count = 0
    for url in urls:
        count += 1
        html = click_href(url)
        new_datas = get_charpter_info_and_save(html)
        save_to_MYSQL(new_datas)
        print('第%s部小说章节信息保存完成'%count)