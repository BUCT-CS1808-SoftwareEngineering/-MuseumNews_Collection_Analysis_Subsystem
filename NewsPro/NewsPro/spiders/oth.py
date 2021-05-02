# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from lxml import etree
from ..items import Baidu2OthproItem

options = EdgeOptions()
options.use_chromium = True
options.add_argument('headless')
browser = webdriver.Chrome(executable_path='./spiders/msedgedriver.exe', options=options)


class OthSpider(scrapy.Spider):
    name = 'oth'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        'https://www.baidu.com/s?ie=utf-8&medium=1&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86'
        '&tn=news&rsv_bp=1&tfflag=0']

    news_site = ['澎湃新闻', '网易新闻', '腾讯网', '手机凤凰网']
    page_num = 1
    url = 'https://www.baidu.com/s?ie=utf-8&medium=1&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6' \
          '%86&tn=news&rsv_bp=1&tfflag=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12' \
          '&pn= '

    def parse_detail_ppxw(self, response, item):
        time = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/p[2]/text()').extract()
        item['time'] = time
        content = response.xpath('/html/body/div[3]/div[1]/div[1]/div[6]//text()').extract()
        yield item

    def parse_detail_wyxw1(self, response):

        item = response.meta['item']
        time = response.xpath(
            '//*[@id="container"]/div[1]/div[2]/text() | // *[ @ id = "contain"] / div[1] / div[2]/text()').extract_first()
        item['time'] = time
        content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
        # item['content'] = content
        yield item

    def parse_detail_txxw(self, response):
        item = response.meta['item']
        year = response.xpath('//*[@id="LeftTool"]/div/div[1]//text()').extract()
        mouthday = response.xpath('//*[@id="LeftTool"]/div/div[2]//text()').extract()
        time = response.xpath('//*[@id="LeftTool"]/div/div[3]//text()').extract()
        # print(year,mouthday,time)
        item['time'] = year + mouthday + time
        content = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]//text()').extract()
        # item['content'] = content
        yield item

    def parse_detail_fhxw(self, response):
        item = response.meta['item']
        time = response.xpath('//*[@id="root"]/div/div[3]/div[1]/div[1]/div[1]/div[1]/p/span[1]/text()').extract_first()
        item['time'] = time
        content = response.xpath('//*[@id="root"]/div/div[3]/div[1]/div[1]/div[3]/div/div[1]//text()').extract()
        # item['content'] = content
        yield item

    def parse(self, response):
        div_list = response.xpath('//*[@id="content_left"]/div[2]/div')
        for i in div_list:
            item = Baidu2OthproItem()
            title = i.xpath('./div/h3/a//text()').extract()
            title = ''.join(title)
            news_url = i.xpath('./div/h3/a/@href').extract_first()
            source = i.xpath('./div/div/div/div/span[1]/text()').extract_first()
            # print(title,news_url,source)
            if source in self.news_site:
                # print("yes")
                item['title'] = title
                item['source'] = source
                if source in self.news_site[0]:  # 澎湃新闻
                    # print("ppxw")
                    browser.get(news_url)
                    tree = etree.HTML(browser.page_source)
                    yield self.parse_detail_ppxw(tree, item)
                elif source in self.news_site[1]:  # 网易新闻
                    # print("wyxw1")
                    yield scrapy.Request(news_url, callback=self.parse_detail_wyxw1, meta={'item': item})

                elif source in self.news_site[2]:  # 腾讯新闻
                    # print("txxw")
                    browser.get(news_url)
                    tree = etree.HTML(browser.page_source)
                    yield self.parse_detail_ttxw(tree, item)
                elif source in self.news_site[3]:  # 凤凰新闻
                    # print("fhxw")
                    yield scrapy.Request(news_url, callback=self.parse_detail_fhxw, meta={'item': item})
        if self.page_num <= 3:
            # page_url = format(self.url%self.page_num)
            page_url = self.url + str(self.page_num * 10)
            self.page_num += 1
            yield scrapy.Request(page_url, callback=self.parse)

browser.quit()
