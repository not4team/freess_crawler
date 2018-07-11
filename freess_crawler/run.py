#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from freess_crawler.spiders import freess_spider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from items import Package, Profile
import settings as my_settings
import msgpacktools
import threading
import time
import logging
from freess_crawler import filelogger
mFileLogger = filelogger.Logger(os.environ["GOBIN"] + "/ss-server/fress_spider.log", logging.ERROR)

interval = 3600 * 3


def start_spider():
    mFileLogger.error("start_spider")
    freessSpider = freess_spider.FreessSpider(isNeedFirefox = False)
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(freessSpider)
    process.start()
    threading.Timer(interval, start_spider).start()


if __name__ == '__main__':
    # msgpacktools.unpack_profiles()
    # package = Package()
    # profiles = []
    # profile = Profile()
    # profile["Name"] = "测试"
    # profile["Country"] = "US"
    # profile["Host"] = "127.0.0.1"
    # profile["RemotePort"] = 1080
    # profile["Password"] = "password"
    # profile["Method"] = "aes-256"
    # profile["OriginUrl"] = msgpacktools.aesencrypt("ss://ihwogjojgaljsldjljglsdjf")
    # profile["Password"] = msgpacktools.aesencrypt("password")
    # profiles.append(dict(profile))
    # package["Profiles"] = profiles
    # msgpacktools.pack_profiles(package)
    # msgpacktools.unpack_profiles()
    if len(sys.argv) == 1:
        start_spider()
    else:
        interval = int(sys.argv[1])
        start_spider()
