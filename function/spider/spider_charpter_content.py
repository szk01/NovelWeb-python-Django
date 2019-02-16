'''
从表novel_info中拿到小说章节的id，剩下的章节id从网页上获取，最后组成url，开始爬取
'''
import time
import pymysql
from threading import Thread
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
sql = "INSERT INTO charpter_detail(charpter_id,charpter_content,charpter_name) values(%s,%s,%s)"

def get_100_novel_id():
    novel_ids = []
    sql = 'SELECT id FROM novel_info LIMIT 880,6966'
    cursor.execute(sql) #result是共有多少条结果
    result = cursor.fetchall() #数据类型是元组,可迭代类型数据

    for data in result:
       novel_ids.append(data)

    return novel_ids

#组成小说页面的url
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
        # time.sleep(4)
        contents = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'volume-list')))
        html = browser.page_source
        return html
    except:
        html = click_href(url)
        return html


#拿到免费章节的相应信息,id,name.组成相应的url。
def get_charpter_info(html):
    datas=[]
    doc = pq(html)
    li_list=doc('.volume-list').children().children().items()
    for li in li_list:
        if '（免）' in li('.clearfix').attr('title')+li('.cfree').text():
            data={
                'charpter_id':li.attr('_cid'),
                'charpter_name':li('.clearfix').attr('title')+li('.cfree').text(),
                'content_href':'https:'+li('.clearfix').attr('href'),
            }
            datas.append(data)
    # print('基本信息保存完成')
    return datas


#插入charpter_content并保存到MYSQL数据库
def insert_charpterContent_and_save(datas):
    for data in datas:
        charpter_url = data['content_href']
        # print(charpter_url)
        content = get_one_charpter_content(charpter_url)
        data['charpter_content'] = content
        save_to_MYSQL(data)


#装饰器，给get_one_cahrpter_content(url)函数新增功能
def time_limited_pri(time_limited):
    def wrapper(func):  #接收的参数是函数
        def __wrapper(params):
            class TimeLimited(Thread):  #class中的两个函数是必须的
                def __init__(self):
                    Thread.__init__(self)

                def run(self):
                    func(params)

            t = TimeLimited()
            t.setDaemon(True)  #这个用户线程必须设置在start()前面
            t.start()
            t.join(timeout=time_limited)
            if t.is_alive():
                raise Exception('连接超时')

        return __wrapper

    return wrapper

#获取免费章节的文本内容
@time_limited_pri(15)
def get_one_charpter_content(url):
    try:
        browser.get(url)
        wait = WebDriverWait(browser, 20)
        contents = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'bd')))
        # time.sleep(2)
        html = browser.page_source
        doc = pq(html)
        content = doc('.bd').html().replace('<br xmlns="http://www.w3.org/1999/xhtml"/>', '\n\n')
        # data['novel_id'] = doc('#main').attr('bookid')
        # print(data['novel_id'])
        return content
    except:
        content = get_one_charpter_content(url)
        return content


#将数据插入到数据库，一次只插入一条
def save_to_MYSQL(new_data):
    try:
        cursor.execute(sql, (new_data['charpter_id'],new_data['charpter_content'],new_data['charpter_name']))
        db.commit()
        print('插入数据成功',new_data['charpter_name'])
    except Exception as e:
        print('插入数据失败！！',e)
        db.rollback()



if __name__ == '__main__':
    ids = get_100_novel_id()
    urls = make_novel_url(ids)
    count = 0
    for url in urls:
        count += 1
        html = click_href(url)
        datas = get_charpter_info(html)
        try:
            insert_charpterContent_and_save(datas)  #循环拿到章节url,然后爬取数据
        except Exception as e:
            print('跳出这一层循环',e)
            continue

        print('第%s部小说保存完成\n'%count)
