# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Profile(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    OriginUrl = scrapy.Field()
    ID = scrapy.Field()
    Name = scrapy.Field()
    Host = scrapy.Field()
    LocalPort = scrapy.Field()
    RemotePort = scrapy.Field()
    Password = scrapy.Field()
    Protocol = scrapy.Field()
    ProtocolParam = scrapy.Field()
    Obfs = scrapy.Field()
    ObfsParam = scrapy.Field()
    Method = scrapy.Field()
    Route = scrapy.Field()
    RemoteDNS = scrapy.Field()
    ProxyApps = scrapy.Field()
    Bypass = scrapy.Field()
    Udpdns = scrapy.Field()
    Ipv6 = scrapy.Field()
    Individual = scrapy.Field()
    Date = scrapy.Field()
    UserOrder = scrapy.Field()
    Plugin = scrapy.Field()
    Country = scrapy.Field()
    VpnType = scrapy.Field()  # 1 ss,2 brook,3 strongswan
    BrookType = scrapy.Field()


class Package(scrapy.Item):
    Profiles = []
