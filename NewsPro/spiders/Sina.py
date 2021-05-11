import scrapy
import json
from ..items import NewsItem
from ..processed_html import get_processed_html


class SinaSpider(scrapy.Spider):
    name = 'Sina'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://search.sina.com.cn/?q=博物馆&c=news&page=1']
    url = 'https://search.sina.com.cn/?q=博物馆&c=news&page='
    page_num = 1
    latest_url = ""

    def save_url(self, url):
        data = dict()
        with open("./spiders/latest_url.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
        with open("./spiders/latest_url.json", "w+", encoding="utf-8") as file:
            data['{}'.format(self.name)] = '{}'.format(url)
            print(data)
            json.dump(data, file, ensure_ascii=False)

    def late_url(self):
        with open("./spiders/latest_url.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            url = data['{}'.format(self.name)]
            return url

    def parse(self, response):
        div_list = response.xpath('//div[@class="box-result clearfix"]')
        desc_url = div_list[0].xpath('./h2/a/@href | ./div/h2/a/@href').extract_first()
        self.latest_url = self.late_url()
        self.save_url(desc_url)
        yield scrapy.Request(self.start_urls[0], callback=self.parse_next)

    def parse_next(self, response):
        div_list = response.xpath('//div[@class="box-result clearfix"]')
        for div in div_list:
            item = NewsItem()
            desc_url = div.xpath('./h2/a/@href | ./div/h2/a/@href').extract_first()
            if desc_url != self.latest_url:
                news_source, time1, time2 = div.xpath('.//span[@class="fgray_time"]/text()').extract_first().split(' ')
                news_time = time1 + " " + time2
                # print(news_source, news_time)
                item['news_source'] = news_source
                item['news_time'] = news_time
                yield scrapy.Request(desc_url, callback=self.parse_desc, meta={'item': item})
            else:
                print(desc_url)
                self.crawler.engine.close_spider(self, "{} spider reach the latest url and quit".format(self.name))
        if self.page_num <= 3:
            self.page_num += 1
            next_url = self.url + str(self.page_num)
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse_next)

    def parse_desc(self, response):
        news_name = response.xpath(
            '//h1[@class="main-title"]/text() | //div[@class="article-header clearfix"]/h1/text() | //h1['
            '@id="artibodyTitle"]/text() | //div[@class="main"]/h1/text() | //div[@class="article-header"]/h1/text('
            ')').extract_first()
        news_content = response.xpath('//div[@id="article"]').extract()
        item = response.meta['item']
        # item['news_name'] = news_name
        # item['news_type']
        try:
            item['news_content'] = get_processed_html(news_content[0])
            # print(item['news_content'])
            if news_name is not None:
                yield item
        except:
            pass

