# -*- coding: utf-8 -*-
import scrapy

from app_monitor.items import AppMonitorItem

class NodeSpider(scrapy.Spider):
    name = 'node'
    allowed_domains = ['nodejs.org']
    start_urls = ['https://nodejs.org/en/download/releases/']

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

        if 'latest-v10' in response.url:
            item['notes'] = '<a href="https://github.com/nodejs/node/blob/master/doc/changelogs/CHANGELOG_V10.md#' + version + '">Changelog</a>'
        else:
            item['notes'] = '<a href="https://github.com/nodejs/node/blob/master/doc/changelogs/CHANGELOG_V8.md#' + version + '">Changelog</a>'

        item['id'] = 'node-' + tmp

        if 'latest-v10' in response.url:
            item['download_url'] = 'https://nodejs.org/dist/latest-v10.x/' + response.xpath('//a[text()[re:test(.,"^node.*x64\.msi$")]]/@href').get()
        else:
            item['download_url'] = 'https://nodejs.org/dist/latest-v8.x/' + response.xpath('//a[text()[re:test(.,"^node.*x64\.msi$")]]/@href').get()
        return item
