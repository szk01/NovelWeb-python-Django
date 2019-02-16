'''把两个表中的charpter_id拿出来，一个个比较，存在则更新相应的has_spidered字段'''

import pymysql

con = pymysql.connect(host='localhost',user='root',password='test123456',port=3306,db='spiders')
cursor = con.cursor()

# #查询语句,查询novel的id(查询指定字段)
# sql = 'SELECT * FROM charpter'
#
# cursor.execute(sql) #result是共有多少条结果
#
# result = cursor.fetchall() #数据类型是元组,可迭代类型数据
#
# print(result)


#拿到相应的charpter表中的charpter_id,然后将数据存储到列表charpter中
def get_charpter():
    sql = "SELECT charpter_id FROM charpter"
    cursor.execute(sql)
    result = cursor.fetchall()
    charpter = []
    for charpter_id in result:
        charpter.append(charpter_id[0])
    return charpter

#拿到相应的charpter表中的charpter_id,然后将数据存储到列表charpter_detail中
def get_charpter_detail():
    sql = "SELECT charpter_id FROM charpter_detail"
    cursor.execute(sql)
    result = cursor.fetchall()
    charpter_detail = []
    for charpter_id in result:
        charpter_detail.append(charpter_id[0])
    return charpter_detail


#比较两者，更新字段
def compare_two_list(charpter,charpter_detail):
    for charpter_id in charpter:
        if charpter_id in charpter_detail:
            try:
                sql = "UPDATE charpter SET has_spidered=%s WHERE charpter_id=%s"
                cursor.execute(sql,(1,charpter_id))
                con.commit()
                print(charpter_id+'的has_spidered章节已经爬取')
            except Exception as e:
                print('更新失败',e)
                con.rollback()
        else:
            try:
                sql = "UPDATE charpter SET has_spidered=%s WHERE charpter_id=%s"
                cursor.execute(sql, (0, charpter_id))
                con.commit()
                print(charpter_id + '的has_spidered章节没有爬取')
            except Exception as e:
                print('更新失败', e)
                con.rollback()


if __name__ == '__main__':
    charpter = get_charpter()
    # print('\n')
    # print(charpter)
    charpter_detail = get_charpter_detail()
    print(charpter_detail)
    compare_two_list(charpter,charpter_detail)

    # sql = "UPDATE charpter SET has_spidered=%s"
    # cursor.execute(sql,0)