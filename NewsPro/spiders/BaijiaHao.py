import scrapy
import json
from ..items import NewsItem
from ..processed_html import get_processed_html


class BaijiahaoSpider(scrapy.Spider):
    name = 'BaijiaHao'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86&tn=news&rsv_bp=1&rsv_sug3=2&oq=&rsv_sug2=0&rsv_btype=t&f=8&inputT=575&rsv_sug4=1120']
    url = 'https://www.baidu.com/s?tn=news&&rtt=1&bsst=1&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86&medium=2&x_bfe_rqs' \
          '=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&pn= '
    page_num = 1

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

    def parse_detail(self, response):
        item = response.meta['item']
        date = response.xpath('//*[@id="ssr-content"]/div[2]/div[1]/div/div/div[2]/div/span[1]/text()').extract()
        time = response.xpath('//*[@id="ssr-content"]/div[2]/div[1]/div/div/div[2]/div/span[2]/text()').extract()
        time = date[0] + " " + time[0]
        print(time)
        item['news_time'] = time
        item['news_content'] = get_processed_html(response.xpath('//*[@id="ssr-content"]/div[2]/div[2]/div[1]/div[1]')[0].extract())
        # item['news_name']
        # item['news_type']
        yield item

    def parse(self, response):
        div_list = response.xpath('//*[@id="content_left"]/div[2]/div')
        news_url = div_list[0].xpath('./div/h3/a/@href').extract_first()
        self.save_url(news_url)
        yield scrapy.Request(self.start_urls[0], callback=self.parse_next)

    def parse_next(self, response):
        div_list = response.xpath('//*[@id="content_left"]/div[2]/div')
        latest_url = self.late_url()
        # print(div_list)
        for i in div_list:
            item = NewsItem()
            news_url = i.xpath('./div/h3/a/@href').extract_first()
            if news_url != latest_url:
                title = i.xpath('./div/h3/a//text()').extract()
                title = ''.join(title)
                source = i.xpath('./div/div/div[2]/div/span[1]/text()').extract()
                source = ''.join(source)
                print(title, "  ", news_url, "  ", source)
                item['news_name'] = title
                item['news_source'] = source
                if news_url.startswith("https://baijiahao.baidu.com/"):
                    yield scrapy.Request(news_url, callback=self.parse_detail, meta={'item': item})
            else:
                self.crawler.engine.close_spider(self, "{} spider reach the latest url and quit".format(self.name))
        if self.page_num <= 2:
            # page_url = format(self.url%self.page_num)
            page_url = self.url + str(self.page_num * 10)
            self.page_num += 1
            yield scrapy.Request(page_url, callback=self.parse_next)
