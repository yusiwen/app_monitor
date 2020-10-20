# -*- coding: utf-8 -*-
import scrapy

from app_monitor.items import AppMonitorItem


class SourcetreeSpider(scrapy.Spider):
    name = 'sourcetree'
    allowed_domains = ['www.sourcetreeapp.com',
                       'product-downloads.atlassian.com']
    start_urls = ['https://www.sourcetreeapp.com']

    def _parse_item(self, app_id, tag, response):
        if tag == 'Windows':
            dwn_url = response.xpath(
                '//div[@id="download-area"]//a[contains(text(), "Windows")]/@href').get()
            version = dwn_url.rsplit(
                '/')[-1].replace('.exe', '').replace('SourceTreeSetup-', '')
        else:
            dwn_url = response.xpath(
                '//div[@id="download-area"]//a[contains(text(), "Mac")]/@href').get()
            version = dwn_url.rsplit(
                '/')[-1].replace('.zip', '').replace('Sourcetree_', '')

        item = AppMonitorItem()
        item['name'] = 'SourceTree ' + tag
        item['version'] = version
        item['date'] = None
        item['notes'] = ''
        item['id'] = app_id
        item['download_url'] = dwn_url
        yield item

    def parse(self, response):
        for item in self._parse_item('sourcetree-mac', 'Mac', response):
            yield item
        for item in self._parse_item('sourcetree-win', 'Windows', response):
            yield item
