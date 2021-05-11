import scrapy
import json
from selenium import webdriver
from ..items import NewsItem
from ..processed_html import get_processed_html
from ..emo_an import snow_res, cnsent_res, bixin_res
from ..get_muselist import get_list
from ..time_process import ppxw_time, wyxw_time, txxw_time, fhxw_tiem, shxw_time



class BaiduSpider(scrapy.Spider):
    name = 'Baidu'
    start_urls = []

    news_site = ['澎湃新闻', '网易新闻', '腾讯网', '手机凤凰网']
    # 第一种分页处理
    page_num = 1
    url = 'https://www.baidu.com/s?ie=utf-8&medium=1&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86&tn=news&rsv_bp=1&tfflag=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn='

    # 需要使用selenium进行处理的url列表
    selenium_url = []
    latest_url = ""

    muse_list = get_list()
    root_url = 'https://www.baidu.com/s?ie=utf-8&medium=1&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd={}&tn=news&rsv_bp=1&oq=&rsv_sug3=6&rsv_sug1=1&rsv_sug7=100&rsv_sug2=0&rsv_btype=t&f=8&inputT=1379&rsv_sug4=1379&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn={}'
    for i in muse_list[0:3]:
        for j in range(0, 3):
            start_urls.append(root_url.format(i, j*10))
    cnt=0
    print(start_urls)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        self.bro = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)

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

    def parse_detail_ppxw(self, response):
        try:
            item = response.meta['item']
            time = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/p[2]/text()').extract_first()
            # print(time)
            item['news_time'] = ppxw_time(time)

            html = response.xpath('/html/body/div[3]/div[1]/div[1]/div[3]')
            htmlContent = '<meta="utf-8">' + html[0].extract()
            htmlContent = get_processed_html(htmlContent)
            item['news_content'] = htmlContent

            content = response.xpath('/html/body/div[3]/div[1]/div[1]/div[3]//text()').extract()
            content = ''.join(content)[0:300]
            news_type = self.get_type(content, item['news_name'])
            item['news_type'] = news_type

            # content = response.xpath('/html/body/div[3]/div[1]/div[1]/div[6]')[0].extract()
            # item['news_content'] = get_processed_html(content)
            # item['news_type']
            # item['museum_name']
            yield item
        except:
            pass

    def parse_detail_wyxw(self, response):
        try:
            item = response.meta['item']
            time = response.xpath(
                '//*[@id="container"]/div[1]/div[2]/text() | // *[ @ id = "contain"] / div[1] / div[2]/text()').extract_first()
            item['news_time'] = wyxw_time(time)

            html = response.xpath('//*[@id="content"]/div[2]')
            htmlContent = '<meta="utf-8">' + html[0].extract()
            htmlContent = get_processed_html(htmlContent)
            item['news_content'] = htmlContent

            content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
            content = ''.join(content)[0:300]
            news_type = self.get_type(content, item['news_name'])
            item['news_type'] = news_type

            # content = response.xpath('//*[@id="content"]/div[2]')[0].extract()
            # item['news_content'] = get_processed_html(content)
            # item['news_type']
            # item['museum_name']
            yield item
        except:
            pass

    def parse_detail_txxw(self, response):
        try:
            item = response.meta['item']
            year = response.xpath('//*[@id="LeftTool"]/div/div[1]/span/text()').extract_first()
            monthday = response.xpath('//*[@id="LeftTool"]/div/div[2]//text()').extract()
            monthday = ''.join(monthday)
            time = response.xpath('//*[@id="LeftTool"]/div/div[3]//text()').extract()
            time = ''.join(time)
            # print(year, monthday, time)
            item['news_time'] = txxw_time(year + monthday + time)
            # print(item['news_time'])

            html = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]')
            htmlContent = '<meta="utf-8">' + html[0].extract()
            htmlContent = get_processed_html(htmlContent)
            item['news_content'] = htmlContent

            content = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]//text()').extract()
            content = ''.join(content)[0:300]
            news_type = self.get_type(content, item['news_name'])
            item['news_type'] = news_type

            # content = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]')[0].extract()
            # item['news_content'] = get_processed_html(content)
            # item['news_type']
            # item['museum_name']
            yield item
        except:
            pass

    def parse_detail_fhxw(self, response):
        try:
            item = response.meta['item']
            time = response.xpath('//*[@id="root"]/div/div[3]/div[1]/div[1]/div[1]/div[1]/p/span[1]/text()').extract_first()
            item['news_time'] = fhxw_tiem(time)

            html = response.xpath('//*[@id="root"]/div/div[3]/div[1]/div[1]/div[3]')
            htmlContent = '<meta="utf-8">' + html[0].extract()
            htmlContent = get_processed_html(htmlContent)
            item['news_content'] = htmlContent

            content = response.xpath('//*[@id="root"]/div/div[3]/div[1]/div[1]/div[3]//text()').extract()
            content = ''.join(content)[0:300]
            news_type = self.get_type(content, item['news_name'])
            item['news_type'] = news_type

            # content = response.xpath('//*[@id="root"]/div/div[3]/div[1]/div[1]/div[3]/div/div[1]')[0].extract()
            # item['news_content'] = get_processed_html(content)
            # item['news_type']
            # item['museum_name']
            yield item
        except:
            pass

    def parse_detail_shxw(self, response):
        try:
            item = response.meta['item']
            time = response.xpath('//*[@id="news-time"]/text()').extract_first()
            item['news_time'] = shxw_time(time)

            html = response.xpath('//*[@id="mp-editor"]')
            htmlContent = '<meta="utf-8">' + html[0].extract()
            htmlContent = get_processed_html(htmlContent)
            item['news_content'] = htmlContent

            content = response.xpath('//*[@id="mp-editor"]//text()').extract()
            content = ''.join(content)[0:300]
            news_type = self.get_type(content, item['news_name'])
            item['news_type'] = news_type

            # content = response.xpath('//*[@id="mp-editor"]')[0].extract()
            # item['news_content'] = get_processed_html(content)
            # item['news_type']
            # item['museum_name']

            yield item
        except:
            pass

    # 增量爬取
    def save_url(self, url, name):
        data = dict()
        with open("./spiders/latest_url.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
        with open("./spiders/latest_url.json", "w+", encoding="utf-8") as file:
            data['{}'.format(self.name + name)] = '{}'.format(url)
            json.dump(data, file, ensure_ascii=False)

    def late_url(self, name):
        with open("./spiders/latest_url.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            url = data['{}'.format(self.name + name)]
            return url


    def parse(self, response):
        muse_name = response.xpath('//*[@id="kw"]/@value').extract_first()
        div_list = response.xpath('//*[@id="content_left"]/div[2]/div')
        # self.latest_url = self.late_url()
        url = div_list[0].xpath('./div/h3/a/@href').extract_first()
        self.save_url(url, muse_name)
        # yield scrapy.Request(response.url, callback=self.parse_next)
        yield scrapy.Request(self.start_urls[0], callback=self.parse_next)

    def parse_next(self, response):
        muse_name = response.xpath('//*[@id="kw"]/@value').extract_first()
        div_list = response.xpath('//*[@id="content_left"]/div[2]/div')
        print(div_list)
        self.latest_url = self.late_url(muse_name)
        for i in div_list:
            # print(i)
            news_url = i.xpath('./div/h3/a/@href').extract_first()
            if news_url != self.latest_url:
                item = NewsItem()
                title = i.xpath('./div/h3/a//text()').extract()
                title = ''.join(title)
                source = i.xpath('./div/div/div/div/span[1]/text()').extract_first()
                # 澎湃新闻
                if news_url.startswith('https://www.thepaper.cn/'):
                    self.cnt+=1
                    item['muse_name'] = muse_name
                    item['news_name'] = title
                    item['news_source'] = '澎湃新闻'
                    self.selenium_url.append(news_url)
                    yield scrapy.Request(news_url, callback=self.parse_detail_ppxw, meta={'item': item})
                    # pass
                # 腾讯新闻
                elif news_url.startswith('https://new.qq.com/'):
                    self.cnt+=1
                    item['muse_name'] = muse_name
                    item['news_name'] = title
                    item['news_source'] = '腾讯新闻'
                    self.selenium_url.append(news_url)
                    yield scrapy.Request(news_url, callback=self.parse_detail_txxw, meta={'item': item})
                    # pass
                # 网易新闻
                elif news_url.startswith('https://www.163.com/'):
                    self.cnt+=1
                    item['muse_name'] = muse_name
                    item['news_name'] = title
                    item['news_source'] = '网易新闻'
                    # self.selenium_url.append(news_url)
                    yield scrapy.Request(news_url, callback=self.parse_detail_wyxw, meta={'item': item})
                # 凤凰新闻
                elif news_url.startswith('https://finance.ifeng.com/'):
                    self.cnt+=1
                    item['muse_name'] = muse_name
                    item['news_name'] = title
                    item['news_source'] = '凤凰新闻'
                    # self.selenium_url.append(news_url)
                    yield scrapy.Request(news_url, callback=self.parse_detail_fhxw, meta={'item': item})
                    # pass
                # 搜狐新闻
                elif news_url.startswith('https://www.sohu.com/a/'):
                    self.cnt+=1
                    item['muse_name'] = muse_name
                    item['news_name'] = title
                    item['news_source'] = '搜狐新闻'
                    # self.selenium_url.append(news_url)
                    yield scrapy.Request(news_url, callback=self.parse_detail_shxw, meta={'item': item})
                print(self.cnt)
                    # pass
                # item = NewsItem()
                # title = i.xpath('./div/h3/a//text()').extract()
                # title = ''.join(title)
                # source = i.xpath('./div/div/div/div/span[1]/text()').extract_first()
                # # print(title, news_url, source)
                # if source in self.news_site:
                #     # print("yes")
                #     item['news_name'] = title
                #     item['news_source'] = source
                #     if source in self.news_site[0]:
                #         # print("ppxw")
                #         self.selenium_url.append(news_url)
                #         yield scrapy.Request(news_url, callback=self.parse_detail_ppxw, meta={'item': item})
                #     elif source in self.news_site[1]:
                #         # print("wyxw")
                #         yield scrapy.Request(news_url, callback=self.parse_detail_wyxw, meta={'item': item})
                #     elif source in self.news_site[2] and news_url.startswith('https://new.qq.com/'):
                #
                #         # print("txxw")
                #         self.selenium_url.append(news_url)
                #         yield scrapy.Request(news_url, callback=self.parse_detail_txxw, meta={'item': item})
                #     elif source in self.news_site[3]:
                #         # print("fhxw")
                #         yield scrapy.Request(news_url, callback=self.parse_detail_fhxw, meta={'item': item})
            else:
                self.crawler.engine.close_spider(self, "{} spider reach the latest url and quit".format(self.name))
        # if self.page_num <= 4:
        #     # page_url = format(self.url%self.page_num)
        #     self.page_num += 1
        #     page_url = self.url + str(self.page_num * 10)
        #     print(page_url)
        #     yield scrapy.Request(page_url, callback=self.parse_next)

    def closed(self, spider):
        self.bro.quit()
