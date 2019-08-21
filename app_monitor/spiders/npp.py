# -*- coding: utf-8 -*-
import scrapy

from app_monitor.items import AppMonitorItem

class NppSpider(scrapy.Spider):
    name = 'npp'
    allowed_domains = ['notepad-plus-plus.org/download']
    start_urls = ['https://notepad-plus-plus.org/download/']

    def parse(self, response):
        tmp  = response.xpath('//h1/text()').get()
        name = tmp.split(' ')[1]
        version = tmp.split(' ')[2]
        item = AppMonitorItem()
        item['name'] = name
        item['version'] = version

        tmp  = response.xpath('//div[@id="main"]/p[text()[re:test(., "^Release\sDate.*")]]/text()').get()
        date = tmp.split(':')[1]
        item['date'] = date.strip()

        notes = response.xpath('//div[@id="main"]/div/ol/li/text()').extract()
        item['notes'] = notes
        item['id'] = 'npp'
        item['download_url'] = 'https://notepad-plus-plus.org' + response.xpath('//div[@id="main"]//a[text()[re:test(., "^Notepad.*zip.*x64$")]]/@href').get()
        return item
