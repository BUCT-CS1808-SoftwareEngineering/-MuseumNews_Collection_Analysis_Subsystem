# -*- coding: utf-8 -*-
import scrapy
from sinaPro.items import SinaproItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://search.sina.com.cn/?q=博物馆&c=news']
    url = 'https://search.sina.com.cn/?q=博物馆&c=news&page=%d'
    page_num = 2

    def parse(self, response):
        div_list = response.xpath('//div[@class="box-result clearfix"]')
        for div in div_list:
            desc_url = div.xpath('./h2/a/@href | ./div/h2/a/@href').extract_first()
            # print(desc_url)
            yield scrapy.Request(desc_url, callback = self.parse_desc)
        # if self.page_num <= 20:
        #     next_url = self.url % self.page_num
        #     self.page_num += 1
        #     yield scrapy.Request(next_url, callback = self.parse)

    def parse_desc(self, response):
        news_name = response.xpath('//div[@class="article-header clearfix"]/h1/text()').extract_first()
        news_content = response.xpath('//p/text()').extract()
        # print(news_name)
        # print(news_content)
