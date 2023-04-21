import pymysql
import pandas as pd
from sqlalchemy import create_engine


def create_db():
    connect = pymysql.connect(  # 连接数据库服务器-*-*-
        user="root",
        password="12345",
        host="127.0.0.1",
        port=3306,
        charset="utf8"
    )
    conn = connect.cursor()  # 创建操作游标
    # 你需要一个游标 来实现对数据库的操作相当于一条线索

    #                          创建表
    conn.execute("CREATE DATABASE IF NOT EXISTS KB_QA")  # 新创建一个数据库
    conn.execute("USE KB_QA")  # 选择这个数据库
    conn.execute("SET @@global.sql_mode=''")#设置sql_model

    # sql 中的内容为创建一个名为 new_table 的表
    conn.execute("""create table IF NOT EXISTS nlpccQA(entity VARCHAR(50) character set utf8 collate utf8_unicode_ci,
    attribute VARCHAR(50) character set utf8 collate utf8_unicode_ci, answer VARCHAR(255) character set utf8 
    collate utf8_unicode_ci)""")  # 创建表 collate:排序的规则

    conn.close()  # 关闭游标连接
    connect.close()  # 关闭数据库服务器连接 释放内存


def loaddata():
    engine = create_engine('mysql+pymysql://root:12345@localhost:3306/kb_qa?charset=utf8')

    # 读取本地CSV文件
    df = pd.read_csv("DB_Data/clean_triple.csv", sep=',', encoding='utf-8')
    print(df)
    # 将新建的DataFrame储存为MySQL中的数据表，不储存index列(index=False)
    # if_exists:
    # 1.fail:如果表存在，啥也不做
    # 2.replace:如果表存在，删了表，再建立一个新表，把数据插入
    # 3.append:如果表存在，把数据插入，如果表不存在创建一个表！！
    pd.io.sql.to_sql(df, 'nlpccqa', con=engine, index=False, if_exists='append', chunksize=10000)
    # df.to_sql('example', con=engine,  if_exists='replace')这种形式也可以
    print("Write to MySQL successfully!")


def upload_data(sql):
    connect = pymysql.connect(  # 连接数据库服务器
        user="root",
        password="12345",
        host="127.0.0.1",
        port=3306,
        db="kb_qa",
        charset="utf8"
    )
    cursor = connect.cursor()  # 创建操作游标
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except Exception as e:
        print("Error: unable to fecth data: %s ,%s" % (repr(e), sql))
    finally:
        # 关闭数据库连接
        cursor.close()
        connect.close()
    return results


if __name__ == '__main__':
    #create_db()
    #loaddata()
    sql = "select * from nlpccqa where entity = '高等数学'"

    #ret = upload_data(sql)
    #print(list(ret))