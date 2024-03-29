# -*- coding: utf-8 -*-
import scrapy

from app_monitor.items import AppMonitorItem


class NodeSpider(scrapy.Spider):
    name = 'node'
    allowed_domains = ['nodejs.org']
    start_urls = ['https://nodejs.org/en/download/']

    def parse(self, response, **kwargs):
        version = response.xpath('//main/div/article/section[1]/p[1]/strong/text()').get()

        item = AppMonitorItem()
        item['name'] = 'Node.js LTS'
        item['version'] = version

        item['date'] = None
        item['notes'] = None
        item['id'] = 'node-lts'
        item['category'] = 'develop'
        item['tags'] = ['nodejs', 'javascript']

        down_urls = ['https://nodejs.org/dist/v' + version + '/node-v' + version + '-x64.msi',
                     'https://nodejs.org/dist/v' + version + '/node-v' + version + '.pkg',
                     'https://nodejs.org/dist/v' + version + '/node-v' + version + '-linux-x64.tar.xz',
                     'https://nodejs.org/dist/v' + version + '/node-v' + version + '-linux-arm64.tar.xz']
        item['download_url'] = down_urls

        return item
