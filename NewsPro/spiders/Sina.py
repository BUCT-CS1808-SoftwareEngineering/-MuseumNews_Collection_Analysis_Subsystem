import scrapy
import json
from ..items import NewsItem
from ..processed_html import get_processed_html
from ..emo_an import snow_res, cnsent_res, bixin_res
from ..time_process import sina_time
from ..get_muselist import get_list

class SinaSpider(scrapy.Spider):
    name = 'Sina'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['https://search.sina.com.cn/?q=博物馆&c=news&page=1']
    # url = 'https://search.sina.com.cn/?q=博物馆&c=news&page='
    # page_num = 1
    start_urls = []

    muse_list = get_list()
    root_url = 'https://search.sina.com.cn/?q={}&c=news&page={}'
    for i in muse_list:
        # for j in range(1, 3):
        start_urls.append(root_url.format(i, 1))

    # print(start_urls)


    latest_url = ""
    reach_latest = False

    def get_type(self, content, title):
        # 调用bixin的predict函数获得情感分析的分数(-1~1)，设置新闻标题的权重为0.4，新闻内容前一部分权重为0.6
        score = (4*bixin_res(title) + 6*bixin_res(content))


        if score < -0.5:
            type = -1
        elif score > 2:
            type = 1
        else:
            type = 0

        return type

    def save_url(self, url, name):
        data = dict()
        with open("./spiders/latest_url.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
        with open("./spiders/latest_url.json", "w+", encoding="utf-8") as file:
            data['{}'.format(self.name + name)] = '{}'.format(url)
            # print(data)
            json.dump(data, file, ensure_ascii=False)

    def late_url(self, name):
        with open("./spiders/latest_url.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            url = data['{}'.format(self.name + name)]
            return url

    def parse(self, response):
        muse_name = response.xpath('//*[@id="keyword"]/@value').extract_first()
        div_list = response.xpath('//div[@class="box-result clearfix"]')
        desc_url = div_list[0].xpath('./h2/a/@href | ./div/h2/a/@href').extract_first()
        # self.latest_url = self.late_url(muse_name)
        self.save_url(desc_url, muse_name)

        for i in range(2, 5):
            yield scrapy.Request(self.root_url.format(muse_name, i), callback=self.parse_next)

    def parse_next(self, response):
        muse_name = response.xpath('//*[@id="keyword"]/@value').extract_first()
        div_list = response.xpath('//div[@class="box-result clearfix"]')
        for div in div_list:
            desc_url = div.xpath('./h2/a/@href | ./div/h2/a/@href').extract_first()
            if desc_url != self.latest_url:
                if not self.reach_latest:
                    item = NewsItem()
                    item['muse_name'] = muse_name
                    news_source, time1, time2 = div.xpath('.//span[@class="fgray_time"]/text()').extract_first().split(' ')
                    news_time = time1 + " " + time2
                    item['muse_id'] = self.muse_list.index(muse_name)+1
                    item['news_source'] = news_source
                    item['news_time'] = news_time
                    if muse_name == '故宫博物馆':
                        item['muse_id'] = 1
                    else:
                        item['muse_id'] = self.muse_list.index(muse_name)+1
                    yield scrapy.Request(desc_url, callback=self.parse_desc, meta={'item': item})
                else:
                    continue
            else:
                print("latest_url is " + desc_url)
                self.reach_latest = True
        # if self.page_num <= 3 and not self.reach_latest:
        #     self.page_num += 1
        #     next_url = self.url + str(self.page_num)
        #     yield scrapy.Request(next_url, callback=self.parse_next)

    def parse_desc(self, response):
        try:
            news_name = response.xpath(
                '//h1[@class="main-title"]/text() | //div[@class="article-header clearfix"]/h1/text() | //h1['
                '@id="artibodyTitle"]/text() | //div[@class="main"]/h1/text() | //div[@class="article-header"]/h1/text('
                ')').extract_first()

            html = response.xpath('//div[@id="article"]')
            # 加上<meta="utf-8">解决网页乱码的问题
            htmlContent = '<meta name="referrer" content="no-referrer" charset="UTF-8">\n' + html[0].extract()
            htmlContent = get_processed_html(htmlContent)

            # news_content = response.xpath('//div[@id="article"]').extract()
            content = response.xpath('//*[@id="article"]//text()').extract()
            content = ''.join(content)[0:200]
            item = response.meta['item']
            # item['news_name'] = news_name
            # item['news_type']
            item['news_content'] = htmlContent
            # print(item['news_content'])
            if news_name is not None:
                item['news_name'] = news_name
                news_type = self.get_type(content, news_name)
                item['news_type'] = news_type
                print(item['news_name'], news_type, item['news_source'], item['news_time'])
                yield item
        except:
            print("Error url is " + response.url)

