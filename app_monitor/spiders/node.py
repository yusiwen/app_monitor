# -*- coding: utf-8 -*-
import scrapy

from app_monitor.items import AppMonitorItem

class NodeSpider(scrapy.Spider):
    name = 'node'
    allowed_domains = ['nodejs.org']
    start_urls = ['http://nodejs.org/en/download/releases/']

    def parse(self, response):
        url = response.xpath('//div[@id="main"]//section//a[text()[re:test(., "^Node.js\s10.x$")]]/@href').extract_first()
        if url:
            yield scrapy.Request(url = url, callback = self.parse_node)

        url = response.xpath('//div[@id="main"]//section//a[text()[re:test(., "^Node.js\s8.x$")]]/@href').extract_first()
        if url:
            yield scrapy.Request(url = url, callback = self.parse_node)

    def parse_node(self, response):
        tmp = response.xpath('//a[text()[re:test(.,"^node.*x64\.msi$")]]/text()').extract_first()
        version = tmp.split('-')[1]

        tmp = response.xpath('//a[text()[re:test(.,"^node.*x64\.msi$")]]/following-sibling::text()').extract_first()
        date = tmp.strip().split()[0]

        tmp = response.url.rsplit('/', 2)[-2]
        tmp = tmp.split('-')[1]

        item = AppMonitorItem()
        item['name'] = 'Node.js ' + tmp
        item['version'] = version

        item['date'] = date

        item['notes'] = ''
        item['id'] = 'node-' + tmp
        return item
