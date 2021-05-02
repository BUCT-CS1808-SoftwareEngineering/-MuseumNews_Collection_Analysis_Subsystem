# -*- coding: utf-8 -*-
import scrapy

from ..items import BaiduproItem


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        'https://www.baidu.com/s?ie=utf-8&medium=2&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86'
        '&tn=news&rsv_bp=1&tfflag=0']

    url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86&medium=2&x_bfe_rqs=03E80' \
          '&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&pn= '
    page_num = 1

    def parse_detail(self, response):
        item = response.meta['item']
        date = response.xpath('//*[@id="ssr-content"]/div[2]/div[1]/div/div/div[2]/div/span[1]/text()').extract()
        time = response.xpath('//*[@id="ssr-content"]/div[2]/div[1]/div/div/div[2]/div/span[2]/text()').extract()
        time = date[0] + " " + time[0]
        # print(time)
        item['time'] = time
        content = response.xpath('//*[@id="ssr-content"]/div[2]/div[2]/div[1]/div[1]//text()').extract()

        # item['content'] = content
        yield item

    def parse(self, response):
        div_list = response.xpath('//*[@id="content_left"]/div[2]/div')
        # print(div_list)
        for i in div_list:
            item = BaiduproItem()
            title = i.xpath('./div/h3/a//text()').extract()
            title = ''.join(title)
            news_url = i.xpath('./div/h3/a/@href').extract_first()
            source = i.xpath('./div/div/div[2]/div/span[1]/text()').extract()
            source = ''.join(source)
            # print(title,"  ",news_url,"  ",source)
            item['title'] = title
            item['source'] = source

            yield scrapy.Request(news_url, callback=self.parse_detail, meta={'item': item})

        if self.page_num <= 5:
            # page_url = format(self.url%self.page_num)
            page_url = self.url + str(self.page_num * 10)
            self.page_num += 1
            yield scrapy.Request(page_url, callback=self.parse)
