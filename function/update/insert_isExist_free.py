'''更新小说的章节目录'''

import time
import pymysql
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#写在这里最好,不会总是重复性地打开浏览器
browser = webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver.exe')


def get_novelID():
    con = pymysql.connect(host='localhost',user='root',password='test123456',port=3306, db='spiders')
    cursor = con.cursor()
    sql = "SELECT id FROM novel_info LIMIT 2248,6898"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


#得到小说的url
def make_url(novel_id):
    url = 'https://book.tianya.cn/chapter-' + novel_id[0]
    return url


#根据小说的id从web上拿到相应的章节目录

    #点击目录链接
def click_href(url):
    try:
        browser.get(url)
        wait = WebDriverWait(browser, 10)
        # 显示等待,小说页面加载完成
        content_click = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'directory'))).click()
        # browser.find_element_by_link_text('目录').click()
        # time.sleep(4)
        #点击后目录加载成功
        contents = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'volume-list')))
        html = browser.page_source
        return html
    except:
        html = click_href(url)
        return html

    #比较免费章节与所有章节的数量
def compare_count(html):
    doc = pq(html)
    li_list=doc('.volume-list').children().children().items()
    novel_id = doc('#main').attr('bookid')  # novel_id
    count_free = 0
    count_all = 0
    for li in li_list:
        count_all += 1
        if '（免）' in li('.clearfix').attr('title')+li('.cfree').text():
            count_free += 1

    print(novel_id,count_free,count_all)
    # print('基本信息保存完成')

    return count_all,count_free



#从数据库中取到相应novel_id的章节信息
def insert_db(count_all,count_free,novel_id):
    con = pymysql.connect(host='localhost', user='root', password='test123456', port=3306, db='spiders')
    cursor = con.cursor()
    sql = "UPDATE novel_info SET isExist_free = %s WHERE id= %s"
    try:
        if count_free == count_all:
            cursor.execute(sql,(1,novel_id))
            con.commit()
            print('插入数据成功,相等')
        elif count_all > count_free:
            cursor.execute(sql, (0,novel_id))
            con.commit()
            print('插入数据成功,不等')

    except Exception as e:
        print('插入数据失败！！', e)
        con.rollback()


if __name__ == '__main__':
    result = get_novelID()
    COUNT = 0
    for novel_id in result:
       COUNT +=1
       url = make_url(novel_id)
       html = click_href(url)
       all,free = compare_count(html)
       insert_db(all,free,novel_id)
       print('第'+str(COUNT)+'部小说','\n')



