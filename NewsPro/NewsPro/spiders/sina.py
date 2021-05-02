# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://search.sina.com.cn/?q=博物馆&c=news']
    url = 'https://search.sina.com.cn/?q=博物馆&c=news&page=%d'
    page_num = 2

    def parse(self, response):
        div_list = response.xpath('//div[@class="box-result clearfix"]')
        for div in div_list:
            easy_title = div.xpath('.//a//text()').extract()
            easy_title = ''.join(easy_title)
            # print(easy_title) # 等拿到表后，找museum_name依据的简单内容
            easy_content = div.xpath('.//p[@class="content"]/text()').extract_first()
            # print(easy_content) # 等拿到表后，找museum_name依据的简单内容

            desc_url = div.xpath('./h2/a/@href | ./div/h2/a/@href').extract_first()
            item = NewsItem()
            news_source, time1, time2 = div.xpath('.//span[@class="fgray_time"]/text()').extract_first().split(' ')
            news_time = time1 + " " + time2
            # print(news_source, news_time)
            item['news_source'] = news_source
            item['news_time'] = news_time
            yield scrapy.Request(desc_url, callback=self.parse_desc, meta={'item': item})
        if self.page_num <= 20:
            next_url = self.url % self.page_num
            self.page_num += 1
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_desc(self, response):
        news_name = response.xpath(
            '//h1[@class="main-title"]/text() | //div[@class="article-header clearfix"]/h1/text() | //h1['
            '@id="artibodyTitle"]/text() | //div[@class="main"]/h1/text() | //div[@class="article-header"]/h1/text('
            ')').extract_first()
        news_content = response.xpath(
            '//div[@class="mainBody"]/p/text() | //font[@cms-style="font-L"]/text() | //div['
            '@class="article"]/div/p/text() |//div[@id="article_content"]/div/div/div/text() | //div['
            '@class="article"]/p/text() | //div[@class="article"]/div/div/text() | //font[@cms-style="font-L '
            'strong-Bold"]/text() | //div[@id="artibody"]/p/text() | //div[@class="article"]/p/text() | //div['
            '@class="article"]/p/font/text() | //p[@cms-style="font-L"]/font/text() | //div['
            '@id="article"]/p/font/text() | //div[@class="article-body main-body"]/p/text() | //p['
            '@cms-style="font-L"]/text() | //div[@class="article"]/font/font/font/p/font/text() | //div['
            '@class="article"]/font/p/font/text() | //div[@class="article clearfix"]/p/font/text() | //div['
            '@class="img_wrapper"]/font/text() | //div[@class="img_wrapper"]/p/font/text()').extract()
        news_content = ''.join(news_content)
        item = response.meta['item']
        item['news_name'] = news_name
        item['news_content'] = news_content
        # print(news_name)  # 有个news_name为None, 且该网站访问不了
        # print(news_content)
        # print(response.url)
        # if news_name != None:
        #     yield item
