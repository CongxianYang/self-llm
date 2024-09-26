#读取数据库的指定表
import pyodbc
import pandas as pd
# 导入模块
import pymysql
# 连接MySQL数据库
conn = pymysql.connect(host='192.168.11.199', user='root', password='mRoRPw7wQ7HxMDn',
                database='wisdom', port=3306, charset='utf8')
# 读取数据表 database数据库    brand表名
df = pd.read_sql_query('select * from brand', conn)
conn.close()
# 将数据写入Excel文件
df.to_excel('D:\mywork\DataSet\sqldata\dbbrand.xlsx', index=False)


