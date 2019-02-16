'''
更新小说天涯网的所有小说基本信息，书名，类型，阅读数，作者等
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import datetime
import time
import pymysql

from pyquery import PyQuery as pq

browser = webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver.exe')
wait = WebDriverWait(browser,30)   #显式等待

#翻页
def get_next_page(num):
    url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=6'  #现代都市31/37      1
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=7'  #灵异悬疑31/101    2
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=1&cat_id=1'   #现代言情31/118   3
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=8'    #职场官场28/27   4   网站将这部分数据删除了
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=1&cat_id=5'    #浪漫青春28/74   5
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=1&cat_id=2'    #古代言情15/14   6
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=1&cat_id=4'      #女生悬疑6/5     7
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=10'    #历史军事 31/62  8
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=9'     #奇幻玄幻  31/111   9
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=24'    #武侠仙侠31/63     10
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=25'    #科幻小说6/5     11
    browser.get(url)
    try:
        print('\n\n翻到第%d页' % num)
        input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page")))
        input.clear()
        input.send_keys(num)
        input.send_keys(Keys.ESCAPE)  # 输入回车键

        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span.TY_view_page > a.on"), str(num))) #查看相应的页码是否高亮
        # time.sleep(6)    #等待数据渲染完成
        html = browser.page_source
        return html
    except TimeoutError as e:
        print(e)


#解析页面得到相应的数据

def parse_with_pq(html):
    onePage_novel_info = []
    doc = pq(html)
    for item in doc.find('#list-books').children('.clearfix').items():
        novel_info ={
            'novel_name': item.find('.mbody .blue').text(),
            'author' : item.find('.mhead').remove('.blue').remove('.gray').text(),
            'read_num': int(item.find('.clearfix').children().eq(1).remove('.gray').text()),
            # 'category': item.find('.clearfix').children().eq(0).remove('.gray').text(),
            'novel_type':str(1),
            'status': item.find('.clearfix').children().eq(5).remove('.gray').text(),
            'id' : item.find('.hide .btn-r').attr('_bid'),
            'web_update_time' : item.find('.clearfix').children().eq(4).remove('.gray').text()
        }
        onePage_novel_info.append(novel_info)

    return onePage_novel_info


#插入spider_time,web_update_time两个字段
def insert_data(datas):
    for data in datas:
        data['spider_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return datas

#将数据插入到数据库
def save_to_MYSQL(datas):
    #连接到数据库
    db = pymysql.connect(host='localhost', user='root', password='test123456', port=3306, db='spiders')
    cursor = db.cursor()
    sql = "INSERT INTO novel_info(novel_name,author,read_num,novel_type,status,id,spider_time,web_update_time) " \
          "values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE read_num=values(read_num),status=values(status)," \
          "spider_time=values(spider_time),web_update_time=values(web_update_time),novel_type=values(novel_type)"


    for data in datas:
        try:
            # print(data['novel_name'])
            cursor.execute(sql, (data['novel_name'],data['author'],data['read_num'],data['novel_type'],data['status'],data['id'],data['spider_time'],data['web_update_time']))
            db.commit()
            print('插入/更新数据成功',data['novel_name'])
        except Exception as e:
            print('插入数据失败！！',e)
            db.rollback()


if __name__ == '__main__':
    for num in range(1,31):
        html = get_next_page(num)
        datas = parse_with_pq(html)
        new_datas = insert_data(datas)
        save_to_MYSQL(new_datas)

