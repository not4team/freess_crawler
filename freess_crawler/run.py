#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from spiders import freess_spider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import settings as my_settings

def start_spider():
    freessSpider = freess_spider.FreessSpider(isNeedFirefox=False)
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(freessSpider)
    process.start()


if __name__ == '__main__':
    start_spider()
