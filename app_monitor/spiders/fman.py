# -*- coding: utf-8 -*-
import scrapy

from app_monitor.items import AppMonitorItem

class FmanSpider(scrapy.Spider):
    name = 'fman'
    allowed_domains = ['fman.io']
    start_urls = ['https://fman.io/download']

    def parse(self, response):
        version = response.xpath('//div[@class="main-content"]//p[contains(text(), "Version")]/text()').get().strip().rsplit(' ')[-1]

        item = AppMonitorItem()
        item['name'] = 'fman'
        item['version'] = version
        item['date'] = ''
        item['id'] = 'fman'
        item['download_url'] = 'https://fman.io/download'
        item['notes'] = 'Changelog: https://fman.io/changelog'
        yield item
