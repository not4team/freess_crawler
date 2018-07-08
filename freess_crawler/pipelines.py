# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import msgpacktools
import logging
import logger
mLogger = logger.Logger(logging.DEBUG)
import filelogger
mFileLogger = filelogger.Logger("fress_spider.log", logging.ERROR)


class FreessCrawlerPipeline(object):
    def process_item(self, item, spider):
        mLogger.debug("pipeline:" + item)
        msgpacktools.pack_profiles(item)
        msgpacktools.unpack_profiles()
        return item
