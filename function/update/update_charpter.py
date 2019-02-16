'''比较数据库已存在的章节与网站的现有的章节，数据库中章节没有更新，插入新的章节'''

import time
import pymysql
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#写在这里最好,不会总是重复性地打开浏览器
browser = webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver.exe')


#拿到数据库中状态为'连载中'的小说id
def get_unfinished_novelID():
    con = pymysql.connect(host='localhost',user='root',password='test123456',port=3306, db='spiders')
    cursor = con.cursor()
    sql = "SELECT id FROM novel_info WHERE status='连载'"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


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
        contents = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'volume-list')))
        html = browser.page_source
        return html
    except:
        html = click_href(url)
        return html

    #拿到章节信息,charpter_id,charpter_name,novel_id三项,并组成列表list_web
def get_charpterInfo(html):
    datas = []
    doc = pq(html)
    li_list=doc('.volume-list').children().children().items()
    for li in li_list:
        if '（免）' in li('.clearfix').attr('title')+li('.cfree').text():
            data=[
                li.attr('_cid'), #charpter_id
                li('.clearfix').attr('title')+li('.cfree').text(), #charpter_name
                doc('#main').attr('bookid') #novel_id
            ]
            # print(data)
            datas.append(data)
    # print('基本信息保存完成')
    return datas



#从数据库中取到相应novel_id的章节信息
def get_charpterInfo_from_db(id):
    con = pymysql.connect(host='localhost', user='root', password='test123456', port=3306, db='spiders')
    cursor = con.cursor()
    sql = "SELECT * FROM charpter WHERE novel_id=%s"
    cursor.execute(sql,id)
    result = cursor.fetchall()
    return result

    #将小说信息改成列表list嵌入列表list的形式
def changeToList(charpter_infos):
    list_db = []
    for charpter_info in charpter_infos:
        new_type = list(charpter_info)
        # print(new_type)
        list_db.append(new_type)
    return list_db


#比较两个列表，不同则插入数据库
def compare_two_list(list_web,list_db):
    # diffSet = list(set(list_web).difference(set(list_db)))  # 求差集，在list_web中但不在list_db中
    if len(list_web)>len(list_db):
        for one_charpter in list_web:
            if one_charpter not in list_db:
                con = pymysql.connect(host='localhost', user='root', password='test123456', port=3306, db='spiders')
                cursor = con.cursor()
                sql = "INSERT INTO charpter(charpter_id,charpter_name,novel_id) values(%s,%s,%s)"
                try:
                    cursor.execute(sql,(one_charpter[0],one_charpter[1],one_charpter[2]))
                    con.commit()
                    print('更新数据成功', one_charpter[0])
                except Exception as e:
                    print('更新数据失败！！', e)
                    con.rollback()
    elif len(list_web)==len(list_db):
        print('id为'+list_db[0][2]+'的小说还未更新\n')


if __name__ == '__main__':
    novel_ids = get_unfinished_novelID()
    for novel_id in novel_ids:
        result = get_charpterInfo_from_db(novel_id[0])
        list_db = changeToList(result)

        url = 'https://book.tianya.cn/chapter-' + novel_id[0]
        html = click_href(url)
        list_web = get_charpterInfo(html)

        compare_two_list(list_web,list_db)


