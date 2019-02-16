'''
爬取小说天涯网的所有小说的基本信息，书名，类型，阅读数，作者等
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pymysql

from pyquery import PyQuery as pq

browser = webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver.exe')
wait = WebDriverWait(browser,30)   #显式等待

#翻页
def get_next_page(num):
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=6' #现代都市11/37
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=7'  #灵异悬疑31/101
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=1&cat_id=1'   #现代言情31/118
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=8'    #职场官场28/27
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=1&cat_id=5'    #浪漫青春28/74
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=1&cat_id=2'    #古代言情15/14
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=1&cat_id=4'      #女生悬疑6/5
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=10'    #历史军事 31/62
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=9'     #奇幻玄幻  31/111
    # url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=24'    #武侠仙侠31/63
    url = 'https://book.tianya.cn/html2/allbooks-cat.aspx?cat_bigid=2&cat_id=25'    #科幻小说6/5
    browser.get(url)
    try:
        print('\n\n翻到第%d页' % num)
        input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page")))
        input.clear()
        input.send_keys(num)
        input.send_keys(Keys.ESCAPE)  # 输入回车键
        time.sleep(8)    #等待数据渲染完成
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
            'novel_type':str(11),
            'status': item.find('.clearfix').children().eq(5).remove('.gray').text(),
            'id' : item.find('.hide .btn-r').attr('_bid')
        }
        onePage_novel_info.append(novel_info)

    return onePage_novel_info


#将数据插入到数据库
def save_to_MYSQL(datas):
    #连接到数据库
    db = pymysql.connect(host='localhost', user='root', password='test123456', port=3306, db='spiders')
    cursor = db.cursor()
    sql = "INSERT INTO novel_info(novel_name,author,read_num,novel_type,status,id) values(%s,%s,%s,%s,%s,%s)"


    for data in datas:
        try:
            # print(data['novel_name'])
            cursor.execute(sql, (data['novel_name'],data['author'],data['read_num'],data['novel_type'],data['status'],data['id']))
            db.commit()
            print('插入数据成功',data['novel_name'])
        except Exception as e:
            print('插入数据失败！！',e)
            db.rollback()


if __name__ == '__main__':
    for num in range(1,31):
        html = get_next_page(num)
        datas = parse_with_pq(html)
        save_to_MYSQL(datas)

