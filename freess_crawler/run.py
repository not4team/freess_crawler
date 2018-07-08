#!/usr/bin/python
# -*- coding: utf-8 -*-
from spiders import freess_spider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import settings as my_settings
import msgpacktools
if __name__ == '__main__':
    freessSpider = freess_spider.FreessSpider()
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(freessSpider)
    process.start()
