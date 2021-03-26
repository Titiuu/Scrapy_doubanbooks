# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from twisted.enterprise import adbapi
import pymysql


class DoubanbooksPipeline:
    def __init__(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     db='doubanbook',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS doubanbooks')
        cursor.execute('''create table doubanbooks (
        	                      name varchar (300),
        	                      author varchar (300),
        	                      press varchar (300),
                                  date varchar (90),
                                  page varchar (90),
                                  price varchar (90),
                                  score varchar (90),
                                  rating_people varchar (33),
                                  ISBN varchar (90),
                                  subject_id varchar (33),
        	                      tags varchar (2400));''')

    def process_item(self, item, spider):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     db='doubanbook',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        if item["page"] is None:
            item["page"] = 'null'
        cursor.execute("select name from doubanbooks where subject_id = %s limit 1", (item["subject_id"]))
        result = cursor.fetchone()
        if result is None:
            print("inserting ", item["name"])
            cursor.execute(
                "insert into doubanbooks (name, author, press, date, page, price, score,rating_people, ISBN,subject_id,tags) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                (item["name"], item["author"], item["press"], item["date"], item["page"], item["price"], item["score"],
                 item['rating_people'], item["ISBN"], item["subject_id"], item["tags"]))
            print(item["name"], item["author"], item["press"], item["date"], item["page"], item["price"], item["score"],
                  item['rating_people'], item["ISBN"], item["subject_id"], item["tags"])
            connection.commit()
        return item
