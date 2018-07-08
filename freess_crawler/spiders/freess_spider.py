# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import sys
sys.path.append("..")
from freess_crawler.items import Profile, Package


class FreessSpider(scrapy.Spider):
    name = "freess"
    country_dict = {'AF': '阿富汗', 'AR': '阿根廷', 'AT': '奥地利', 'AU': '澳大利亚', 'BR': '巴西', 'CA': '加拿大', 'CH': '瑞士', 'CL': '智利', 'CU': '古巴', 'CZ': '捷克', 'DE': '德国', 'DK': '丹麦',
                    'EG': '埃及', 'ES': '西班牙', 'FI': '芬兰', 'FR': '法国', 'GR': '希腊', 'HK': '香港', 'HU': '匈牙利', 'ID': '印尼', 'IE': '爱尔兰', 'IL': '以色列', 'IN': '印度', 'IT': '意大利',
                    'JP': '日本', 'MM': '缅甸', 'MO': '澳门', 'MX': '墨西哥', 'MY': '马来西亚', 'NL': '荷兰', 'NO': '挪威', 'PH': '菲律宾', 'PK': '巴基斯坦', 'PL': '波兰', 'RU': '俄罗斯', 'SE': '瑞典',
                    'SG': '新加坡', 'TH': '泰国', 'US': '美国', 'VN': '越南', 'CN': '中国', 'GB': '英国', 'TW': '台湾', 'NZ': '新西兰', 'SA': '沙特阿拉伯', 'KP': '朝鲜', 'KR': '韩国', 'PT': '葡萄牙',
                    'MN': '蒙古', 'RO': '罗马尼亚'}

    def __init__(self):
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        self.browser = webdriver.Firefox(firefox_options=fireFoxOptions)

    def start_requests(self):
        urls = [
            'https://free-ss.site/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response)
        tbody = response.css('tbody')[1]
        trs = tbody.css('tr')
        package = Package()
        profiles = []
        for tr in trs:
            tds = tr.css('td')
            host = tds.extract()[1]
            port = tds.extract()[2]
            password = tds.extract()[3]
            method = tds.extract()[4]
            country = tds.extract()[6]
            profile = Profile()
            profile.Name = self.country_dict[country]
            profile.Country = country
            profile.Host = host
            profile.RemotePort = port
            profile.Password = password
            profile.Method = method
            profiles.append(profile)
        package.Profiles = profiles
        yield package
