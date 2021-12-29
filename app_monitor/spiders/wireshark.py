import scrapy

from app_monitor.items import AppMonitorItem


class WiresharkSpider(scrapy.Spider):
    name = 'wireshark'
    allowed_domains = ['www.wireshark.org']
    start_urls = ['http://www.wireshark.org/']

    def parse(self, response, **kwargs):
        tmp = response.xpath('//section//a[contains(text(), "Stable Release")]/text()').get()
        version = tmp.split('(')[1].split(')')[0]

        item = AppMonitorItem()
        item['name'] = 'Wireshark'
        item['version'] = version

        item['date'] = None
        item['notes'] = None
        item['id'] = 'wireshark'
        item['download_url'] = response.xpath(
            '//section//a[contains(text(), "Stable Release")]/parent::div/following-sibling::div[1]//li').getall()

        return item
