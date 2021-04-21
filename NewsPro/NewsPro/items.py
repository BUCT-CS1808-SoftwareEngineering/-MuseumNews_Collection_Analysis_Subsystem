# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaproItem(scrapy.Item):
    # define the fields for your item here like:
    museum_name = scrapy.Field()
    news_name = scrapy.Field()
    news_content = scrapy.Field()
    news_time = scrapy.Field()
    news_source = scrapy.Field()
    pass
