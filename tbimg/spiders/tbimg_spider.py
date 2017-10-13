# -*- coding: utf-8 -*-
import re
import scrapy
from tbimg.items import TbimgItem
from selenium import webdriver
from scrapy import signals
import pandas
import tbimg.settings as settings


class TbimgSpiderSpider(scrapy.Spider):
    name = 'tbimg_spider'
    allowed_domains = ['www.tmall.com']
    df = pandas.read_csv(settings.IMAGES_STORE + "/urls.csv")
    start_urls = list(df["链接"].values)
    download_delay = 2

    def __init__(self):
        super(TbimgSpiderSpider, self).__init__()
        self.browser = webdriver.PhantomJS()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(TbimgSpiderSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        self.browser.quit()

    def extract_num(self, text, prefix=""):
        # 从字符串中提取出数字，可指定数字的前缀字符串
        match_re = re.match(".*%s?(\d+).*" % prefix, text)
        if match_re:
            nums = int(match_re.group(1))
        else:
            nums = 1
        return nums

    def parse(self, response):
        category = response.meta.get("category", "")
        page = self.extract_num(response.url, prefix="pageNo=")
        item = TbimgItem()
        cur_url = response.url
        srcs = response.css('.ks-switchable-panel-internal322>img::attr(src)').extract()
        if srcs:
            if page == 1:
                df = self.df[self.df["链接"]==cur_url]
                category = df["分类"].values[0]
                if "?" not in cur_url:
                    cur_url += "?pageNo=1"
                else:
                    cur_url += "&pageNo=1"

            my_srcs = ["http:" + src.replace("30x30", "300x300") for src in srcs]
            item['image_urls'] = my_srcs
            item['category'] = category
            yield item

            next_page = page + 1
            next_url = cur_url.replace("pageNo={0}".format(page), "pageNo={0}".format(next_page))
            yield scrapy.Request(url=next_url, dont_filter=True, callback=self.parse, meta={"category":category})