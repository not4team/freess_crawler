# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy import signals
from selenium.webdriver.common.proxy import Proxy, ProxyType


class BaseSpider(scrapy.Spider):
    name = "base_spider"

    def __init__(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 1080)
        profile.update_preferences()
        fireFoxOptions = webdriver.FirefoxOptions()
        # fireFoxOptions.set_headless()
        self.browser = webdriver.Firefox(
            firefox_profile=profile, options=fireFoxOptions)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_opened)
        return spider

    def spider_closed(self, spider):
        self.browser.quit()
