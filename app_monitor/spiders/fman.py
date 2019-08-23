# -*- coding: utf-8 -*-
import scrapy

from app_monitor.items import AppMonitorItem

class FmanSpider(scrapy.Spider):
    name = 'fman'
    allowed_domains = ['fman.io']
    start_urls = ['https://fman.io/download']

    def _parse_changelog(self, response):
        item = response.meta['item']
        notes = response.xpath('//h2[@id="v1.6.5"]/following-sibling::*[count(preceding-sibling::h2[@id="v1.6.4"])=0]')
        notes = notes[:len(notes) - 4]
        notes = ''.join(notes.getall())
        item['notes'] = notes
        yield item

    def parse(self, response):
        version = response.xpath('//div[@class="main-content"]//p[@class="icon-caption"]/text()').get().strip()
        version = version.split()[1]
        date = response.xpath('//div[@class="main-content"]//p[@class="icon-caption"]/br/following-sibling::text()').get().strip()


        item = AppMonitorItem()
        item['name'] = 'fman'
        item['version'] = version
        item['date'] = date
        item['id'] = 'fman'
        item['download_url'] = 'https://fman.io/download'
        yield scrapy.Request('https://fman.io/changelog', meta={'item':item}, callback=self._parse_changelog)
