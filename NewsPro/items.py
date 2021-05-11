# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    muse_name = scrapy.Field()  # museum_id ?
    news_name = scrapy.Field()  # 标题
    news_content = scrapy.Field()  # 内容
    news_type = scrapy.Field()  # 类型
    news_time = scrapy.Field()  # 时间
    news_source = scrapy.Field()  # 来源
    muse_id = scrapy.Field() # 暂时添加一个博物馆id，在muse_list中的位置