'''从novel_info表中查询书的id,(查询指定数据)并打印出来'''

import pymysql

#连接到spiders数据库
con = pymysql.connect(host='localhost',
                      user='root',
                      password='test123456',
                      port=3306,db='spiders'
                      )
cursor = con.cursor()

#查询语句,查询novel的id(查询指定字段)
sql = 'SELECT * FROM charpter'

cursor.execute(sql) #result是共有多少条结果

result = cursor.fetchall() #数据类型是元组,可迭代类型数据

print(result)


s= set()
for data in result:
    each_list = list(data)  #将元组tuple转变成列表list
    # print(each_list)
    s.add(each_list)

print(s)

