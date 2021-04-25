import scrapy
from selenium import webdriver
from msedge.selenium_tools import  EdgeOptions
from lxml import etree


class NetEaseSpider(scrapy.Spider):
    name = "NetEase"
    start_urls = "https://art.163.com/museum"
    news_urls = []
    load_times = 5

    def __init__(self):
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument('headless')
        self.browser = webdriver.Chrome(executable_path='./spiders/msedgedriver.exe', options=options)
        self.get_news_items()

    def get_news_items(self):
        self.browser.get(self.start_urls)
        tree = etree.HTML(self.browser.page_source)
        news_items = tree.xpath('//div[@class="ndi_main"]/div[contains(@class,"data_row")]')
        for item in news_items:
            self.news_urls.append(item.xpath('.//div[@class="news_title"]/h3/a/@href')[0])
    def parse(self, response):
        pass
