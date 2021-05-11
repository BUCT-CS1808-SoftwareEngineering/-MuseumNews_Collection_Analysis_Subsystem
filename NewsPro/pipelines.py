# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NewsproPipeline(object):
    def process_item(self, item, spider):
        # print(item)
        return item


import pymysql


# 继承自object
# class QiubaiproPipeline(object):
#     # 存储到本地
#     fp = None
#     # 重写父类方法：该方法只在开始爬虫的时候被调用一次
#     def open_spider(self,spider):
#         print('start...')
#         self.fp = open('./qiubai.txt', 'w', encoding='utf-8')
#
#     # 专门用来处理Item对象
#     # 该方法可以接收爬虫文件提交过来的item对象
#     # 每接收一个item就会调用一次该方法
#     def process_item(self, item, spider):
#         # 持久化存储
#         # print(item)
#         author = item['author']
#         content = item['content']
#
#         self.fp.write(author+':'+content+'\n')
#
#         # 这个return的item会传递给下一个即将被执行的管道类
#         return item
#
#     def close_spider(self,spider):
#         print("end...")
#         self.fp.close()
#
# class mysqlPipeline(object):
#     conn = None
#     cursor = None
#
#     def open_spider(self, spider):
#         print("db open...")
#         self.conn = pymysql.Connect(
#             host='127.0.0.1',
#             port=3306,
#             user='root',
#             password='',
#             db='cs1808en',
#             charset='utf8'
#         )
#
#     def process_item(self, item, spider):
#         self.cursor = self.conn.cursor()
#         # i=0
#         try:
#             self.cursor.execute( \
#                 'insert into news_info_table(muse_ID, news_Name, news_content, news_type, news_time, news_source) values("%d","%s","%s","%d","%s","%s")' \
#                 % (item['muse_id'], item["title"], item["content"], item['type'], item['time'], item['source']))
#             # i+=1
#             self.conn.commit()
#         except Exception as e:
#             print(e)
#             self.conn.rollback()
#
#         return item
#
#     def close_spider(self, spider):
#         print("db close...")
#         self.cursor.close()
#         self.conn.close()
#
# # 爬虫文件提交的item类型的对象最终会提交给优先级较高的管道类
