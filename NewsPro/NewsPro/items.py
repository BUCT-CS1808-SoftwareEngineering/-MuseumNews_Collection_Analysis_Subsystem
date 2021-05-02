# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    museum_name = scrapy.Field()
    news_name = scrapy.Field()
    news_content = scrapy.Field()
    news_time = scrapy.Field()
    news_source = scrapy.Field()


class Baidu2OthproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()


class BaiduproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()


class SpemuseproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    muse = scrapy.Field()
    type = scrapy.Field()


class NetEaseItem(scrapy.Item):
    # define the fields for your item here like:
    museum_name = scrapy.Field()  # museum_id ?
    news_name = scrapy.Field()
    news_content = scrapy.Field()
    news_type = scrapy.Field()
    news_time = scrapy.Field()
    news_source = scrapy.Field()
