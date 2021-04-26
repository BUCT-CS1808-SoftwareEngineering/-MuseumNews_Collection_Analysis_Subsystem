import scrapy
from selenium import webdriver
from msedge.selenium_tools import  EdgeOptions
from lxml import etree


class NetEaseSpider(scrapy.Spider):
    name = "NetEase"
    start_urls = ["https://art.163.com/museum"]
    news_urls = []
    # 最大刷新新闻次数
    load_times = 5

    def __init__(self):
        options = EdgeOptions()
        options.use_chromium = True
        # options.add_argument('headless')
        self.browser = webdriver.Chrome(executable_path='./spiders/msedgedriver.exe', options=options)
        self.get_news_items()
        # while self.load_times:
        #     self.load_more_btn = self.browser.find_element_by_xpath('//*[@id="ne_wrap"]/body/div[1]/div[3]/div[3]/div[2]/div/div/div/div[1]/a[1]/div[1]/span')

    def get_news_items(self):
        self.browser.get(self.start_urls[0])
        tree = etree.HTML(self.browser.page_source)
        news_items = tree.xpath('//div[@class="ndi_main"]/div[contains(@class,"data_row")]')
        for item in news_items:
            # 可修改成直接yield Response
            self.news_urls.append(item.xpath('.//div[@class="news_title"]/h3/a/@href')[0])

    def update_news_items(self):
        if self.load_times > 0:
            self.load_times -= 1
            self.load_more_btn.click()

    def parse(self, response):
        pass
