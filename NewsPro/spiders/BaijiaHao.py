import scrapy
import json
from ..items import NewsItem
from ..processed_html import get_processed_html
from ..emo_an import snow_res, cnsent_res, bixin_res
from ..get_muselist import get_list
from .. getsubstr import subStr
from time import sleep
from ..time_process import Baijiahao_time


class BaijiahaoSpider(scrapy.Spider):
    name = 'BaijiaHao'
    # allowed_domains = ['www.xxx.com']
    # 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86&tn=news&rsv_bp=1&rsv_sug3=2&oq=&rsv_sug2=0&rsv_btype=t&f=8&inputT=575&rsv_sug4=1120'
    start_urls = []

    # 第一种翻页方式的源url
    url = 'https://www.baidu.com/s?tn=news&&rtt=1&bsst=1&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86&medium=2&x_bfe_rqs' \
          '=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&pn= '
    page_num = 1
    reach_latest = False

    muse_list = get_list()
    print(muse_list)

    # 第二种翻页方式的源url
    root_url = 'https://www.baidu.com/s?ie=utf-8&medium=2&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd={}&tn=news&rsv_bp=1&tfflag=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn={}'
    # 表示取muse_list中的前几个博物馆，如果全取的话一次性爬取太多会造成IP被禁
    p = muse_list.index('齐国故城遗址博物馆')
    for i in muse_list[0: p]:
        # 分页
            # 加入start_urls中
        # if muse_list.index(i) == 100:
        # sleep(20)
        start_urls.append(root_url.format(i, 0))
    for i in muse_list[p+1:]:
        # 分页
        # 加入start_urls中
        # if muse_list.index(i) == 100:
        # sleep(20)
        start_urls.append(root_url.format(i, 0))

    # print(start_urls)
    forbidden_url = ['https://baijiahao.baidu.com/s?id=1699722267644466512&wfr=spider&for=pc']
    count = 1

    def save_url(self, url, name):
        data = dict()
        with open("./spiders/latest_url.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
        with open("./spiders/latest_url.json", "w+", encoding="utf-8") as file:
            data['{}'.format(self.name + name)] = '{}'.format(url)  # 修改self.name -> musename,通过传参来实现
            # print(data)
            json.dump(data, file, ensure_ascii=False)

    def late_url(self, name):   # 修改, self.name -> muse_name
        with open("./spiders/latest_url.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            url = data['{}'.format(self.name + name)]
            return url

    def initial_url(self, name):
        data = dict()
        with open("./spiders/latest_url.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
        with open("./spiders/latest_url.json", "w+", encoding="utf-8") as file:
            data['{}'.format(self.name + name)] = ""
            json.dump(data, file, ensure_ascii=False)

    def parse_detail(self, response):
        try:
            item = response.meta['item']
            date = response.xpath('//*[@id="ssr-content"]/div[2]/div[1]/div/div/div[2]/div/span[1]/text()').extract()
            time = response.xpath('//*[@id="ssr-content"]/div[2]/div[1]/div/div/div[2]/div/span[2]/text()').extract()
            time = date[0] + " " + time[0]
            # print(time)
            item['news_time'] = Baijiahao_time(time)
            html = response.xpath('//*[@id="ssr-content"]/div[2]/div[2]/div[1]/div[1]')
            # 加上<meta="utf-8">解决网页乱码的问题
            htmlContent = '<meta name="referrer" content="no-referrer" charset="UTF-8">\n' + html[0].extract()
            htmlContent = get_processed_html(htmlContent)
            item['news_content'] = htmlContent
            # item['news_content'] = get_processed_html(response.xpath('//*[@id="ssr-content"]/div[2]/div[2]/div[1]/div[1]')[0].extract())
            # item['news_name']
            # item['news_type']
            # 调用bixin的predict函数获得情感分析的分数(-1~1)，设置新闻标题的权重为0.4，新闻内容前一部分权重为0.6
            content = response.xpath('//*[@id="ssr-content"]/div[2]/div[2]/div[1]/div[1]//text()').extract()
            content = ''.join(content).replace('\n', '').replace('\r', '')
            score = (4*bixin_res(item['news_name']) + 6*bixin_res(content[0:300]))
            if score < -0.5:
                type = -1
            elif score > 2:
                type = 1
            else:
                type = 0

            item['news_type'] = type
            self.count += 1

            yield item
        except:
            pass

    def parse(self, response):

        div_list = response.xpath('//*[@id="content_left"]/div[2]/div')
        news_url = div_list[0].xpath('./div/h3/a/@href').extract_first()
        muse_name = response.xpath('//*[@id="form"]/span[1]/input/@value').extract_first()
        self.initial_url(muse_name)
        self.save_url(news_url, muse_name)
        # yield的url应该是当前的url，改成

        self.count += 1
        # if self.count is 50 or self.count is 100 or self.count is 150 or self.count is 200:
        #     print(self.count, "sleep(30)")
        #     sleep(30)

        for i in range(1, 5):
            # page_list = self.root_url.format(muse_name, i*10)
            # sleep(0.5)
            yield scrapy.Request(self.root_url.format(muse_name, i*10), callback=self.parse_next)
        # yield scrapy.Request(self.start_urls[0], callback=self.parse_next)

    def parse_next(self, response):
        # self.count += 1
        # if self.count is 50 or self.count is 100 or self.count is 150 or self.count is 200:
        #     sleep(30)
        # 获取当前查找的博物馆名称
        muse_name = response.xpath('//*[@id="form"]/span[1]/input/@value').extract_first()
        div_list = response.xpath('//*[@id="content_left"]/div[2]/div')
        latest_url = self.late_url(muse_name)
        # print(div_list)
        for i in div_list:
            item = NewsItem()
            news_url = i.xpath('./div/h3/a/@href').extract_first()

            if news_url != latest_url and news_url not in self.forbidden_url and news_url != self.forbidden_url[0]:
                if not self.reach_latest:
                    # 将muse_name存入item
                    item['muse_name'] = muse_name
                    title = i.xpath('./div/h3/a//text()').extract()
                    title = ''.join(title)
                    source = i.xpath('./div/div/div[2]/div/span[1]/text()').extract()
                    source = ''.join(source)
                    print(muse_name, title, "  ", news_url, "  ", source)
                    item['news_name'] = title
                    item['news_source'] = source
                    if muse_name == '故宫博物院':
                        item['muse_id'] = 1
                    else:
                        item['muse_id'] = self.muse_list.index(muse_name)+1
                    if news_url.startswith("https://baijiahao.baidu.com/"):
                        # if self.muse_list.index(muse_name) % 10 == 0:
                        # sleep(0.1)
                        yield scrapy.Request(news_url, callback=self.parse_detail, meta={'item': item})
                else:
                    continue
            else:
                print("latest_url is " + news_url)
                self.reach_latest = True
                # self.crawler.engine.close_spider(self, "{} spider reach the latest url and quit".format(self.name))

        # 第一中分页方法的操作
        # if self.page_num <= 5:
        #     # page_url = format(self.url%self.page_num)
        #     page_url = self.url + str(self.page_num * 10)
        #     self.page_num += 1
        #     yield scrapy.Request(page_url, callback=self.parse_next)
