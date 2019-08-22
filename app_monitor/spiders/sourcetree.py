# -*- coding: utf-8 -*-
import scrapy

from app_monitor.items import AppMonitorItem

class SourcetreeSpider(scrapy.Spider):
    name = 'sourcetree'
    allowed_domains = ['www.sourcetreeapp.com', 'product-downloads.atlassian.com']
    start_urls = ['https://www.sourcetreeapp.com/download-archives']

    def _parse_item(self, id, tag, response):
        dwn_url_mac = response.xpath('//div[@id="download-area"]//h3[text()[re:test(.,"^' + tag + '$")]]/../following-sibling::div[1]//tr[1]/td[1]/div/a/@href').get()
        version_mac = response.xpath('//div[@id="download-area"]//h3[text()[re:test(.,"^' + tag + '$")]]/../following-sibling::div[1]//tr[1]/td[1]/div/a/b/text()').get()
        date_mac = response.xpath('//div[@id="download-area"]//h3[text()[re:test(.,"^' + tag + '$")]]/../following-sibling::div[1]//tr[1]/td[3]/text()').get()
        release_note_url = response.xpath('//div[@id="download-area"]//h3[text()[re:test(.,"^' + tag + '$")]]/../following-sibling::div[1]//tr[1]/td[1]/small/a/@href').get()


        item = AppMonitorItem()
        item['name'] = 'SourceTree ' + tag
        item['version'] = version_mac

        item['date'] = date_mac

        item['notes'] = ''
        item['id'] = id
        item['download_url'] = dwn_url_mac
        yield scrapy.Request(release_note_url, meta={'item':item}, callback=self._parse_release_notes)

    def _parse_release_notes(self, response):
        item = response.meta['item']
        if 'windows' in response.url:
            item['notes'] = response.xpath('//body').get()
        else:
            tmp = ''
            tmp = tmp.join(response.xpath('//a[1]/following-sibling::li').extract())
            item['notes'] = tmp

        yield item

    def parse(self, response):
        for item in self._parse_item('sourcetree-mac', 'Mac', response):
            yield item
        for item in self._parse_item('sourcetree-win', 'Windows', response):
            yield item
