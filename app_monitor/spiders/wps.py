import scrapy

from app_monitor.items import AppMonitorItem
from datetime import datetime


class WpsSpider(scrapy.Spider):
    name = 'wps'
    allowed_domains = ['wps.cn']
    start_urls = ['http://pc.wps.cn/',
                  'https://mac.wps.cn/', 'https://linux.wps.cn/']

    def parse_pc(self, response):
        tmp = response.xpath(
            '//div[@class="banner_txt"]/p[@class="verson_txt"]/text()').get().split('/')
        version = tmp[0]
        version_date = datetime.strptime(tmp[1], '%Y.%m.%d')
        datestr = version_date.strftime('%Y-%m-%d')
        down_url = response.xpath(
            '//div[@class="banner_txt"]/p[@class="verson_txt"]/preceding-sibling::a/@href').get()

        item = AppMonitorItem()
        item['name'] = 'WPS(PC)'
        item['version'] = version
        item['date'] = datestr
        item['notes'] = ''
        item['id'] = 'wps-pc'
        item['download_url'] = down_url
        return item

    def parse_mac(self, response):
        tmp = response.xpath(
            '//div[@class="banner"]/p[@class="banner_txt"]/text()').get().split('/')
        version = tmp[0]
        version_date = datetime.strptime(tmp[1], '%Y.%m.%d')
        datestr = version_date.strftime('%Y-%m-%d')
        down_url = response.xpath(
            '//div[@class="banner"]/p[@class="banner_txt"]/preceding-sibling::a/@data-href').get()

        item = AppMonitorItem()
        item['name'] = 'WPS(MAC)'
        item['version'] = version
        item['date'] = datestr
        item['notes'] = ''
        item['id'] = 'wps-mac'
        item['download_url'] = down_url
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
        item['download_url'] = response.xpath('//div[@class="box"]//a[contains(@href, "amd64.deb")]/@href').get()
        return item

    def parse(self, response):
        platform = response.url.split('//')[1].split('.')[0]
        if platform == 'pc':
            return self.parse_pc(response)
        elif platform == 'mac':
            return self.parse_mac(response)
        else:
            return self.parse_linux(response)
