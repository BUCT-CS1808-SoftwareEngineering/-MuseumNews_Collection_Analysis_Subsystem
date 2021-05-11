import scrapy
import json
from selenium import webdriver
from ..items import NewsItem
from ..processed_html import get_processed_html


class BaiduSpider(scrapy.Spider):
    name = 'Baidu'
    start_urls = [
        "https://www.baidu.com/s?ie=utf-8&medium=1&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86&tn=news&rsv_bp=1&tfflag=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn=10"]

    news_site = ['澎湃新闻', '网易新闻', '腾讯网', '手机凤凰网']
    page_num = 1
    selenium_url = []
    url = 'https://www.baidu.com/s?ie=utf-8&medium=1&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86&tn=news&rsv_bp=1&tfflag=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn='
    latest_url = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        self.bro = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)

    def parse_detail_ppxw(self, response):
        item = response.meta['item']
        time = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/p[2]/text()').extract_first()
        # print(time)
        item['news_time'] = time
        content = response.xpath('/html/body/div[3]/div[1]/div[1]/div[6]')[0].extract()
        item['news_content'] = get_processed_html(content)
        # item['news_type']
        # item['museum_name']
        yield item

    def parse_detail_wyxw(self, response):
        item = response.meta['item']
        time = response.xpath(
            '//*[@id="container"]/div[1]/div[2]/text() | // *[ @ id = "contain"] / div[1] / div[2]/text()').extract_first()
        item['news_time'] = time
        content = response.xpath('//*[@id="content"]/div[2]')[0].extract()
        item['news_content'] = get_processed_html(content)
        # item['news_type']
        # item['museum_name']
        yield item

    def parse_detail_txxw(self, response):
        item = response.meta['item']
        year = response.xpath('//*[@id="LeftTool"]/div/div[1]/span/text()').extract_first()
        monthday = response.xpath('//*[@id="LeftTool"]/div/div[2]//text()').extract()
        monthday = ''.join(monthday)
        time = response.xpath('//*[@id="LeftTool"]/div/div[3]//text()').extract()
        time = ''.join(time)
        # print(year, monthday, time)
        try:
            item['news_time'] = year + monthday + time
            # print(item['news_time'])
            content = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]')[0].extract()
            item['news_content'] = get_processed_html(content)
            # item['news_type']
            # item['museum_name']
            yield item
        except:
            pass

    def parse_detail_fhxw(self, response):
        try:
            item = response.meta['item']
            time = response.xpath('//*[@id="root"]/div/div[3]/div[1]/div[1]/div[1]/div[1]/p/span[1]/text()').extract_first()
            item['news_time'] = time
            content = response.xpath('//*[@id="root"]/div/div[3]/div[1]/div[1]/div[3]/div/div[1]')[0].extract()
            item['news_content'] = get_processed_html(content)
            # item['news_type']
            # item['museum_name']
            yield item
        except:
            pass

    def save_url(self, url):
        data = dict()
        with open("./spiders/latest_url.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
        with open("./spiders/latest_url.json", "w+", encoding="utf-8") as file:
            data['{}'.format(self.name)] = '{}'.format(url)
            json.dump(data, file, ensure_ascii=False)

    def late_url(self):
        with open("./spiders/latest_url.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            url = data['{}'.format(self.name)]
            return url

    def parse(self, response):
        div_list = response.xpath('//*[@id="content_left"]/div[2]/div')
        self.latest_url = self.late_url()
        url = div_list[0].xpath('./div/h3/a/@href').extract_first()
        self.save_url(url)
        yield scrapy.Request(self.start_urls[0], callback=self.parse_next)

    def parse_next(self, response):
        div_list = response.xpath('//*[@id="content_left"]/div[2]/div')
        for i in div_list:
            # print(i)
            news_url = i.xpath('./div/h3/a/@href').extract_first()
            if news_url != self.latest_url:
                item = NewsItem()
                title = i.xpath('./div/h3/a//text()').extract()
                title = ''.join(title)
                source = i.xpath('./div/div/div/div/span[1]/text()').extract_first()
                # print(title, news_url, source)
                if source in self.news_site:
                    # print("yes")
                    item['news_name'] = title
                    item['news_source'] = source
                    if source in self.news_site[0]:
                        # print("ppxw")
                        self.selenium_url.append(news_url)
                        yield scrapy.Request(news_url, callback=self.parse_detail_ppxw, meta={'item': item})
                    elif source in self.news_site[1]:
                        # print("wyxw")
                        yield scrapy.Request(news_url, callback=self.parse_detail_wyxw, meta={'item': item})
                    elif source in self.news_site[2] and news_url.startswith('https://new.qq.com/'):

                        # print("txxw")
                        self.selenium_url.append(news_url)
                        yield scrapy.Request(news_url, callback=self.parse_detail_txxw, meta={'item': item})
                    elif source in self.news_site[3]:
                        # print("fhxw")
                        yield scrapy.Request(news_url, callback=self.parse_detail_fhxw, meta={'item': item})
            else:
                self.crawler.engine.close_spider(self, "{} spider reach the latest url and quit".format(self.name))
        if self.page_num <= 4:
            # page_url = format(self.url%self.page_num)
            self.page_num += 1
            page_url = self.url + str(self.page_num * 10)
            print(page_url)
            yield scrapy.Request(page_url, callback=self.parse_next)

    def closed(self, spider):
        self.bro.quit()
