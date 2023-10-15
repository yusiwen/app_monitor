import scrapy

from app_monitor.items import AppMonitorItem


class NmapSpider(scrapy.Spider):
    name = 'nmap'
    allowed_domains = ['nmap.org']
    start_urls = ['https://nmap.org/download.html']

    def parse(self, response):
        url = response.xpath('//tr/td//b/u[text() = "stable"]/following-sibling::a[1]/text()').get()
        version = url.split('-')[1]

        item = AppMonitorItem()
        item['name'] = 'nmap'
        item['version'] = version

        item['date'] = None
        item['notes'] = None
        item['id'] = 'nmap'
        item['download_url'] = url
        item['category'] = 'tool'
        item['tags'] = ['network', 'nmap']

        return item
