import scrapy


class NetEaseSpider(scrapy.Spider):
    name = "NetEase"
    start_urls = ["https://art.163.com/museum"]

    def parse(self, response):
        pass
