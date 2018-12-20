#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import logging
sys.path.append(os.environ["FREESS_SPIDER_HOME"])
import re
from freess_crawler import msgpacktools
from urllib import parse
import base64
from selenium.webdriver.common.proxy import Proxy, ProxyType
from scrapy import signals
from freess_crawler.items import Profile, Package
import scrapy
import time
from selenium import webdriver


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
            # profile.set_preference('network.proxy.type', 1)
            # profile.set_preference('network.proxy.http', '127.0.0.1')
            # profile.set_preference('network.proxy.http_port', 8118)
            # profile.set_preference('network.proxy.ssl', '127.0.0.1')
            # profile.set_preference('network.proxy.ssl_port', 8118)
            # profile.set_preference('network.proxy.socks', '127.0.0.1')
            # profile.set_preference('network.proxy.socks_port', 1080)
            profile.set_preference(
                "general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0")
            profile.update_preferences()
            fireFoxOptions = webdriver.FirefoxOptions()
            fireFoxOptions.set_headless(True)
            self.browser = webdriver.Firefox(
                log_path=os.environ["GOBIN"] + "/ss-server/geckodriver.log",
                firefox_profile=profile,
                options=fireFoxOptions)
            # self.browser.set_page_load_timeout(10)
            # self.browser.set_script_timeout(10)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FreessSpider, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        logging.info("freess spider closed")
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

        scripts = response.css('head').extract_first()
        pattern = re.compile(r'(?<=var table = ).+?(?=DataTable)', re.I)
        matchObj = re.search(pattern, scripts)
        _id = matchObj.group(0)
        logging.info("parse id is " + _id)
        thead = response.css('table' + _id[3:len(_id)-3] + ' thead')
        thead_dict = {}
        for i, th in enumerate(thead.css('tr th')):
            thead_dict[th.css('::text').extract_first()] = i
        logging.info(thead_dict)
        tbody = response.css('table' + _id[3:len(_id)-3] + ' tbody')
        trs = tbody.css('tr')
        package = Package()
        profiles = []
        for tr in trs:
            tds = tr.css('td::text')
            host = tds.extract()[thead_dict["Address"]]
            port = tds.extract()[thead_dict["Port"]]
            password = tds.extract()[thead_dict["Password"]]
            method = tds.extract()[thead_dict["Method"]]
            country = tds.extract()[6]
            profile = Profile()
            country_count = self.count_country(country, profiles)
            name = self.country_dict[country]
            if country_count > 0:
                name += str(country_count)
            profile["Name"] = name
            profile["Country"] = country
            profile["Host"] = host
            profile["RemotePort"] = int(port)
            profile["Password"] = password
            profile["Method"] = method
            profile["OriginUrl"] = msgpacktools.aesencrypt(
                self.create_originurl(profile))
            profile["Password"] = msgpacktools.aesencrypt(password)
            profiles.append(dict(profile))
        package["Profiles"] = profiles
        yield package

    def create_originurl(self, profile):
        host = profile["Method"] + ":" + profile["Password"] + \
            "@" + profile["Host"] + ":" + str(profile["RemotePort"])
        ss = "ss://" + str(base64.b64encode(host.encode("utf-8")), 'utf-8')
        return parse.quote(ss)

    def count_country(self, country, profiles):
        count = 0
        for profile in profiles:
            if country in profile["Country"]:
                count += 1
        return count
