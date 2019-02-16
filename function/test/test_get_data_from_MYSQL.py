'''组成100部小说的url'''

import pymysql

#连接到spiders数据库
def get_100_id():
    novel_ids=[]
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='test123456',
                          port=3306,db='spiders'
                          )
    cursor = con.cursor()
    #查询语句,查询novel的id(查询指定字段)
    sql = 'SELECT id FROM novel_info LIMIT 0,100'
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

if __name__ == '__main__':
    ids = get_100_id()
    make_novel_url(ids)