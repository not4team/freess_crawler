# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
import sys
sys.path.append("..")
import logging
from freess_crawler import logger
mLogger = logger.Logger(logging.DEBUG)
from freess_crawler import filelogger
mFileLogger = filelogger.Logger("fress_spider.log", logging.ERROR)
from freess_crawler.items import Profile, Package
from scrapy import signals
from selenium.webdriver.common.proxy import Proxy, ProxyType


class FreessSpider(scrapy.Spider):
    name = "freess"
    country_dict = {'AF': '阿富汗', 'AR': '阿根廷', 'AT': '奥地利', 'AU': '澳大利亚', 'BR': '巴西', 'CA': '加拿大', 'CH': '瑞士', 'CL': '智利', 'CU': '古巴', 'CZ': '捷克', 'DE': '德国', 'DK': '丹麦',
                    'EG': '埃及', 'ES': '西班牙', 'FI': '芬兰', 'FR': '法国', 'GR': '希腊', 'HK': '香港', 'HU': '匈牙利', 'ID': '印尼', 'IE': '爱尔兰', 'IL': '以色列', 'IN': '印度', 'IT': '意大利',
                    'JP': '日本', 'MM': '缅甸', 'MO': '澳门', 'MX': '墨西哥', 'MY': '马来西亚', 'NL': '荷兰', 'NO': '挪威', 'PH': '菲律宾', 'PK': '巴基斯坦', 'PL': '波兰', 'RU': '俄罗斯', 'SE': '瑞典',
                    'SG': '新加坡', 'TH': '泰国', 'US': '美国', 'VN': '越南', 'CN': '中国', 'GB': '英国', 'TW': '台湾', 'NZ': '新西兰', 'SA': '沙特阿拉伯', 'KP': '朝鲜', 'KR': '韩国', 'PT': '葡萄牙',
                    'MN': '蒙古', 'RO': '罗马尼亚'}

    def __init__(self, isNeedFirefox=True):
        if isNeedFirefox:
            profile = webdriver.FirefoxProfile()
            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.http', '127.0.0.1')
            profile.set_preference('network.proxy.http_port', 8118)
            profile.set_preference('network.proxy.ssl', '127.0.0.1')
            profile.set_preference('network.proxy.ssl_port', 8118)
            profile.update_preferences()
            fireFoxOptions = webdriver.FirefoxOptions()
            # fireFoxOptions.set_headless()
            self.browser = webdriver.Firefox(
                firefox_profile=profile, options=fireFoxOptions)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FreessSpider, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        self.browser.quit()

    def start_requests(self):
        urls = [
            'https://free-ss.site/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        body = response.css('body').extract_first()
        if "Checking your browser before accessing" in body:
            time.sleep(10)
            now = time.strftime("%b-%d-%Y_%H:%M:%S", time.localtime())
            yield response.follow("https://free-ss.site/?time="+now, self.parse)
            return
        mLogger.debug(body)
        tbody = response.css('tbody')[3]
        mFileLogger.error(tbody)
        trs = tbody.css('tr')
        package = Package()
        profiles = []
        for tr in trs:
            tds = tr.css('td::text')
            host = tds.extract()[1]
            port = tds.extract()[2]
            password = tds.extract()[3]
            method = tds.extract()[4]
            country = tds.extract()[6]
            profile = Profile()
            profile["Name"] = self.country_dict[country]
            profile["Country"] = country
            profile["Host"] = host
            profile["RemotePort"] = port
            profile["Password"] = password
            profile["Method"] = method
            profiles.append(profile)
        package["Profiles"] = profiles
        yield package
