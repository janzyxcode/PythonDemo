# _*_ coding: utf-8 _*_
import pymysql
import RequestTool
import re
import json

# SET SQL_SAFE_UPDATES = 0
# 如果要存储中文，需要设置mysql中字段的Collation
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='admin',charset='utf8',db='Fund')
cur = conn.cursor()

def close():
    cur.close()
    conn.close()


def readAllTopic(tkey):
    topicKey = '"' + tkey + '"'
    sql = 'select TTypeName from allTopics where topicKey = ' + topicKey
    try:
        cur.execute(sql)
        results = cur.fetchall()
        list = []
        for item in results:
            list.append(item[0])
        return list
    except Exception as e:
        print(e)



