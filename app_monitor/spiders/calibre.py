# -*- coding: utf-8 -*-
import scrapy
import lxml.html

from app_monitor.items import AppMonitorItem

class CalibreSpider(scrapy.Spider):
    name = 'calibre'
    allowed_domains = ['calibre-ebook.com']
    start_urls = ['https://calibre-ebook.com/whats-new']

    def parse(self, response):
        tmp = response.xpath('//div[@id="release-pane"]/div').extract_first()
        doc = lxml.html.fromstring(tmp)
        tmp = doc.xpath('//h2/text()')[0]
        version = tmp.split()[1]
        date = tmp.split('[')[1]
        date = date.replace(']', '')

        item = AppMonitorItem()
        item['name'] = 'Calibre'
        item['version'] = version

        item['date'] = date

        item['notes'] = ''
        item['id'] = 'calibre'
        item['download_url'] = ''
        return item
