import pymysql

#连接到spiders数据库
con = pymysql.connect(host='localhost',
                      user='root',
                      password='test123456',
                      port=3306,db='spiders')
cursor = con.cursor()

#查询语句,查询novel的id(查询指定字段)
sql0 = 'SELECT id FROM novel_info WHERE novel_type = 4'

cursor.execute(sql0) #result是共有多少条结果

result = cursor.fetchall() #数据类型是元组,可迭代类型数据

# print(result)
def remove_charpter(result):
    sql = 'DELETE FROM charpter WHERE novel_id = %s'
    for novel_id in result:
        # print(novel_id[0])
        try:
            cursor.execute(sql,novel_id[0])
            con.commit()
        # result1 = cursor.fetchall()
        # print(result1,'\n\n')
        except:
            con.rollback()

def remove_novelInfo():
    try:
        sql0 = 'DELETE FROM novel_info WHERE novel_type = 4'
        cursor.execute(sql0)
        con.commit()
        print('完成删除')
    except:
        con.rollback()


if __name__ == '__main__':
    # remove_charpter(result)
    remove_novelInfo()