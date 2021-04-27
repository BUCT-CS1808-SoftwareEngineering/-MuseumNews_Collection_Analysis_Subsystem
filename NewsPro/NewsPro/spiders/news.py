# -*- coding: utf-8 -*-
import scrapy
from NewsPro.items import SpemuseproItem
from NewsPro.emo_an import snow_res,cnsent_res,bixin_res
from NewsPro.getsubstr import subStr


class NewsSpider(scrapy.Spider):
    name = 'news'
    # allowed_domains = ['www.xxx.com']
    # muse_list = ['故宫博物馆','中国国家博物馆','上海科技馆','中国科学技术馆']
    # root_url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word='
    # start_urls = ['https://www.baidu.com/s?ie=utf-8&medium=2&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=%E6%95%85%E5%AE%AB%E5%8D%9A%E7%89%A9%E9%A6%86&tn=news&rsv_bp=1&tfflag=0']
    start_urls = ['https://www.baidu.com/s?ie=utf-8&medium=2&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=%E6%95%85%E5%AE%AB%E5%8D%9A%E7%89%A9%E9%A6%86&tn=news&rsv_bp=1&tfflag=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn=0']

    # def get_all_musenews(self):
    muse_list = ['中国国家博物馆', '上海科技馆', '中国科学技术馆']
    # root_url = 'https://www.baidu.com/s?ie=utf-8&medium=2&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd={}&tn=news&rsv_bp=1&tfflag=0'
    root_url = 'https://www.baidu.com/s?ie=utf-8&medium=2&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd={}&tn=news&rsv_bp=1&tfflag=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn=0'
    for i in muse_list:
        start_urls.append(root_url.format(i))
    # print(start_urls)


    page_num = 1

    def parse_detail(self, response):

        item = response.meta['item']
        date = response.xpath('//*[@id="ssr-content"]/div[2]/div[1]/div/div/div[2]/div/span[1]/text()').extract()
        time = response.xpath('//*[@id="ssr-content"]/div[2]/div[1]/div/div/div[2]/div/span[2]/text()').extract()
        time = date[0] + " " + time[0]
        # print(time)
        item['time']=time
        content = response.xpath('//*[@id="ssr-content"]/div[2]/div[2]/div[1]/div[1]//text()').extract()

        content = ''.join(content)
        # print(content[0:300])
        # snow_res(content)
        # 调用bixin的predict函数获得情感分析的分数(-1~1)，设置新闻标题的权重为0.6，新闻内容前一部分权重为0.4
        score = (bixin_res(6*item['title'])+4*bixin_res(content[0:300]))

        print(score/10)
        if score < -0.5:
            type = -1
        elif score > 2:
            type = 1
        else:
            type = 0

        # item['content'] = content
        item['type'] = type
        yield item

    def parse(self, response):
        # self.count+=1
        # print(self.count)
        # self.get_all_musenews()
        muse_name = response.xpath('//*[@id="form"]/span[1]/input/@value').extract_first()
        # print(muse_name)
        # print(response.url)

        div_list = response.xpath('//*[@id="content_left"]/div[2]/div')
        # print(div_list)
        errorlist = ['光明网', '上观新闻']
        for i in div_list:
            item = SpemuseproItem()
            # index = self.start_urls.index(response.url)
            # muse = self.muse_list[index]
            # item['muse'] = muse
            item['muse'] = muse_name
            title = i.xpath('./div/h3/a//text()').extract()
            title = ''.join(title)
            source = i.xpath('./div/div/div[2]/div/span[1]/text()').extract()
            source = ''.join(source)
            news_url = i.xpath('./div/h3/a/@href').extract_first()

            if source in errorlist or source is '光明网' or "落实" in title or "手拉手" in title:
                print("error")
                continue
            if 'https://baijiahao.baidu.com/s?id=' in news_url:
                print(title, "  ", news_url, "  ", source, " ", muse_name)
                item['title'] = title
                item['source'] = source

                # print("yes")
                yield scrapy.Request(news_url, callback=self.parse_detail, meta={'item': item})
            elif 'gmw' in news_url:
                print("no")
                continue

        if self.page_num <= 3:
            # page_url = format(self.url%self.page_num)
            url = response.url
            print(url)
            url = subStr(url, 'pn=')

            page_url = url + str(self.page_num*10)
            print(page_url)
            self.page_num += 1
            yield scrapy.Request(page_url, callback=self.parse)


