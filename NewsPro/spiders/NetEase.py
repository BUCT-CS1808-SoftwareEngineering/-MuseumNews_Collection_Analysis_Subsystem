import scrapy
import re
import json
from selenium import webdriver
from lxml import etree
from time import sleep
from ..processed_html import get_processed_html
from ..items import NewsItem
from ..time_process import wyxw_time
from ..get_muselist import get_list
from ..emo_an import bixin_res


class NeteaseSpider(scrapy.Spider):
    name = 'NetEase'
    # allowed_domains = ['www.xxx.com']
    start_urls = ["https://art.163.com/museum"]
    news_urls = []
    load_times = 0
    reach_latest = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        self.browser = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)

    def get_type(self, content, title):
        # 调用bixin的predict函数获得情感分析的分数(-1~1)，设置新闻标题的权重为0.6，新闻内容前一部分权重为0.4
        score = (6*bixin_res(title) + 4*bixin_res(content))


        if score < -0.5:
            type = -1
        elif score > 2:
            type = 1
        else:
            type = 0

        return type

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

    def initial_url(self):
        data = dict()
        with open("./spiders/latest_url.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
        with open("./spiders/latest_url.json", "w+", encoding="utf-8") as file:
            data['{}'.format(self.name)] = ""
            json.dump(data, file, ensure_ascii=False)

    def parse(self, response):
        self.browser.get(self.start_urls[0])
        self.update_news_items()
        tree = etree.HTML(self.browser.page_source)
        news_items = tree.xpath('//div[@class="ndi_main"]/div[contains(@class,"data_row")]')
        self.initial_url()
        latest_url = self.late_url()
        for item in news_items:
            # print(item.xpath('.//div[@class="news_title"]/h3/a/@href')[0])
            url = item.xpath('.//div[@class="news_title"]/h3/a/@href')[0]
            if url != latest_url:
                if not self.reach_latest:
                    yield scrapy.Request(url=url, callback=self.parse_details)
                else:
                    continue
            else:
                print("latest_url is " + url)
                self.reach_latest = True
                # self.crawler.engine.close_spider(self, "{} spider reach the latest url and quit".format(self.name))
        url = news_items[0].xpath('.//div[@class="news_title"]/h3/a/@href')[0]
        self.save_url(url)
        self.browser.quit()

    def parse_details(self, response):
        tf = re.compile(r"(.*)\s+.*?:\s?(.*)")

        # try:
        item = NewsItem()
        item['news_name'] = response.xpath("//h1[@class='post_title']/text()")[0].extract()
        item['news_content'] = get_processed_html('<meta name="referrer" content="no-referrer" charset="UTF-8">\n' + response.xpath("//div[@class='post_body']")[0].extract())
        context_list = response.xpath('//div[@class="post_body"]//p/text()').extract()
        context = "".join(context_list)[0:300]
        # print(context)

        # print(item['news_content'])
        mix_text = response.xpath('//div[@class="post_info"]/text()').extract_first()
        mix_text = mix_text.rstrip().lstrip()
        mix = tf.match(mix_text)
        # print(mix.group(1) + " and " + mix.group(2))
        item['news_time'] = mix.group(1)
        item['news_source'] = mix.group(2)

        news_type = self.get_type(context, item['news_name'])


        item['news_type'] = news_type
        item['muse_name'] = get_museum_name(context)
        print(item['news_name'])
        if item['muse_name'] != "":
            yield item
        # except:
        #     print("error url is " + response.url)

def get_museum_name(context):
    name = ""
    index = len(context) + 5
    museum_list = get_list()
    for item in museum_list:
        i = KMP_algorithm(context, item)
        if i != -1 and i < index:
            name = item
    print(name)
    return name


def KMP_algorithm(string, substring):
    pnext = gen_pnext(substring)
    n = len(string)
    m = len(substring)
    i, j = 0, 0
    while (i < n) and (j < m):
        if string[i] == substring[j]:
            i += 1
            j += 1
        elif j != 0:
            j = pnext[j - 1]
        else:
            i += 1
    if j == m:
        return i - j
    else:
        return -1


def gen_pnext(substring):
    index, m = 0, len(substring)
    pnext = [0] * m
    i = 1
    while i < m:
        if substring[i] == substring[index]:
            pnext[i] = index + 1
            index += 1
            i += 1
        elif index != 0:
            index = pnext[index - 1]
        else:
            pnext[i] = 0
            i += 1
    return pnext