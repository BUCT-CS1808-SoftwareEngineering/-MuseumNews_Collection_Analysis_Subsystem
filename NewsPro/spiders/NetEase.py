import scrapy
import re
import json
from selenium import webdriver
from lxml import etree
from time import sleep
from ..processed_html import get_processed_html
from ..items import NewsItem


class NeteaseSpider(scrapy.Spider):
    name = 'NetEase'
    # allowed_domains = ['www.xxx.com']
    start_urls = ["https://art.163.com/museum"]
    news_urls = []
    load_times = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        self.browser = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)

    def save_url(self, url):
        data = dict()
        with open("./spiders/latest_url.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
        with open("./spiders/latest_url.json", "w+", encoding="utf-8") as file:
            data['{}'.format(self.name)] = '{}'.format(url)
            json.dump(data, file, ensure_ascii=False)

    def update_news_items(self):
        while self.load_times < 2:
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            load_btn = self.browser.find_element_by_css_selector(".load_more_btn")
            load_btn.click()
            # print(self.load_times)
            self.load_times += 1
            sleep(1)

    def late_url(self):
        with open("./spiders/latest_url.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            url = data['{}'.format(self.name)]
            return url

    def parse(self, response):
        self.browser.get(self.start_urls[0])
        self.update_news_items()
        tree = etree.HTML(self.browser.page_source)
        news_items = tree.xpath('//div[@class="ndi_main"]/div[contains(@class,"data_row")]')
        latest_url = self.late_url()
        for item in news_items:
            # print(item.xpath('.//div[@class="news_title"]/h3/a/@href')[0])
            url = item.xpath('.//div[@class="news_title"]/h3/a/@href')[0]
            if url != latest_url:
                yield scrapy.Request(url=url, callback=self.parse_details)
            else:
                self.crawler.engine.close_spider(self, "{} spider reach the latest url and quit".format(self.name))
        url = news_items[0].xpath('.//div[@class="news_title"]/h3/a/@href')[0]
        self.save_url(url)
        self.browser.quit()

    def parse_details(self, response):
        tf = re.compile(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+\w\w:\s*(.*)')
        item = NewsItem()
        try:
            item['news_name'] = response.xpath("//h1[@class='post_title']/text()").extract_first()
            item['news_content'] = get_processed_html(response.xpath("//div[@class='post_body']")[0].extract())
            # print(item['news_content'])
            mix = tf.match(response.xpath("//div[@class='post_info']/text()").extract_first())
            item['news_time'] = mix.group(1)
            item['news_source'] = mix.group(2)
            # item['news_type']
            # item['museum_name']
            yield item
        except:
            print(response.url)
