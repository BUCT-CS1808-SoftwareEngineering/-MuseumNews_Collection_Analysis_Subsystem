import scrapy
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from lxml import etree
from time import sleep


class NetEaseSpider(scrapy.Spider):
    name = "NetEase"
    start_urls = ["https://art.163.com/museum"]
    news_urls = []
    load_times = 0

    def __init__(self):
        options = EdgeOptions()
        options.use_chromium = True
        # options.add_argument('headless')
        self.browser = webdriver.Chrome(executable_path='./spiders/msedgedriver.exe', options=options)
        self.get_news_items()

    def get_news_items(self, max_times):
        self.browser.get(self.start_urls[0])
        self.update_news_items()
        tree = etree.HTML(self.browser.page_source)
        news_items = tree.xpath('//div[@class="ndi_main"]/div[contains(@class,"data_row")]')
        for item in news_items:
            # 可修改成直接yield Response
            # self.news_urls.append(item.xpath('.//div[@class="news_title"]/h3/a/@href')[0])
            yield scrapy.Request(url=item.xpath('.//div[@class="news_title"]/h3/a/@href')[0], callback=self.parse)
        print(self.news_urls)
        self.browser.quit()

    def update_news_items(self, max_times=5):
        while self.load_times < max_times:
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            load_btn = self.browser.find_element_by_css_selector(".load_more_btn")
            load_btn.click()
            print(self.load_times)
            self.load_times += 1

    def parse(self, response):
        pass
