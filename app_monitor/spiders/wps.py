from datetime import datetime

import scrapy

from app_monitor.items import AppMonitorItem


class WpsSpider(scrapy.Spider):
    name = 'wps'
    allowed_domains = ['wps.cn']
    start_urls = ['https://platform.wps.cn/', 'https://mac.wps.cn/', 'https://linux.wps.cn/']

    def parse_pc(self, response):
        tmp = response.xpath(
            '//div[@class="system" and contains(text(), "Window")]/following-sibling::div[1]/text()').get()
        version = tmp.split('/')[0].strip().split(' ')[0].strip()
        version_date = datetime.strptime(version, '%Y.%m.%d')
        datestr = version_date.strftime('%Y-%m-%d')
        down_url = response.xpath(
            '//div[@class="system" and contains(text(), "Window")]/parent::a/parent::div/following-sibling::a/@href').get()

        item = AppMonitorItem()
        item['name'] = 'WPS(PC)'
        item['version'] = version
        item['date'] = datestr
        item['notes'] = ''
        item['id'] = 'wps-pc'
        item['download_url'] = down_url
        item['category'] = 'office'
        return item

    def parse_mac(self, response):
        tmp = response.xpath(
            '//div[@id="download1"]/p[@class="banner_txt"]/text()').get().split('/')
        version = tmp[0].strip()
        version_date = datetime.strptime(tmp[1].strip(), '%Y.%m.%d')
        datestr = version_date.strftime('%Y-%m-%d')
        down_url = response.xpath('//a[@id="downloadButton"]/@data-href').get()

        item = AppMonitorItem()
        item['name'] = 'WPS(MAC)'
        item['version'] = version
        item['date'] = datestr
        item['notes'] = ''
        item['id'] = 'wps-mac'
        item['download_url'] = down_url
        item['category'] = 'office'
        return item

    def parse_linux(self, response):
        version = response.xpath(
            '//div[@class="banner"]/p[@class="banner_txt"]/text()').get()

        item = AppMonitorItem()
        item['name'] = 'WPS(Linux)'
        item['version'] = version
        item['date'] = None
        item['notes'] = ''
        item['id'] = 'wps-linux'
        item['category'] = 'office'
        item['download_url'] = response.xpath('//div[@class="box"]//a[contains(@href, "amd64.deb")]/@href').get()
        return item

    def parse(self, response, **kwargs):
        platform = response.url.split('//')[1].split('.')[0]
        if platform == 'platform':
            return self.parse_pc(response)
        elif platform == 'mac':
            return self.parse_mac(response)
        else:
            return self.parse_linux(response)
