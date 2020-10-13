import scrapy
from app_monitor.items import AppMonitorItem


class GoSpider(scrapy.Spider):
    name = 'go'
    allowed_domains = ['golang.org']
    start_urls = ['https://golang.org/dl/']

    def parse(self, response):
        version = response.xpath('//h3[@id="stable"]/following-sibling::div[1]//h2[1]/text()').get().split(' ')[0].replace('go', '')
        down_url = response.xpath('//h3[@id="stable"]/following-sibling::div[1]//table//a[contains(text(), "linux-amd64")]/@href').get()

        item = AppMonitorItem()
        item['name'] = 'Golang'
        item['version'] = version
        item['date'] = ''
        item['notes'] = ''
        item['id'] = 'go'
        item['download_url'] = 'https://golang.org' + down_url
        return item
