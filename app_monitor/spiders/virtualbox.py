import scrapy

from app_monitor.items import AppMonitorItem


class VirtualboxSpider(scrapy.Spider):
    name = 'virtualbox'
    allowed_domains = ['virtualbox.org']
    start_urls = ['https://www.virtualbox.org/wiki/Downloads/']

    def parse(self, response):
        version = response.xpath(
            '//h3[contains(@id, "platformpackages")]/text()').get().strip().split(' ')[0]
        item = AppMonitorItem()
        item['name'] = 'VirtualBox'
        item['version'] = version
        item['date'] = None
        item['notes'] = ''
        item['id'] = 'virtualbox'

        urls = []
        urls.append(response.xpath('//a[@class="ext-link"][contains(text(), "Windows hosts")]/@href').get())
        urls.append(response.xpath('//a[@class="ext-link"][contains(text(), "OS X hosts")]/@href').get())
        urls.append('https://www.virtualbox.org/wiki/Linux_Downloads')
        item['download_url'] = urls
        return item
