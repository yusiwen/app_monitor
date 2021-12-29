# -*- coding: utf-8 -*-
import scrapy

from app_monitor.items import AppMonitorItem


class MongodbSpider(scrapy.Spider):
    name = 'mongodb'
    allowed_domains = ['www.mongodb.com']
    start_urls = ['https://www.mongodb.com/download-center/community']

    def parse(self, response):
        tmp = response.xpath('//main//select/option[text()[re:test(.,".*current\srelease\)$")]]/text()').get()
        version = tmp.split()[0]

        item = AppMonitorItem()
        item['name'] = 'MongoDB current release'
        item['version'] = version

        item['date'] = ''

        item['notes'] = ''
        item['id'] = 'mongodb'
        item['download_url'] = 'https://www.mongodb.org/dl/win32/'
        return item
