import scrapy

from app_monitor.items import AppMonitorItem


class AllwaysyncSpider(scrapy.Spider):
    name = 'allwaysync'
    allowed_domains = ['allwaysync.com']
    start_urls = ['https://allwaysync.com/download']

    def parse(self, response, **kwargs):
        version = response.xpath('//section//div[@class="panel-body"]/p/strong/text()').get()
        down_urls = [response.xpath('//a[@id="desktop-download-primary"]/@href').get(),
                     response.xpath('//a[@id="desktop-download-secondary"]/@href').get()]

        item = AppMonitorItem()
        item['name'] = 'Allway Sync'
        item['version'] = version
        item['date'] = None
        item['notes'] = ''
        item['id'] = 'allwaysync'
        item['category'] = 'tool'
        item['tags'] = ['sync']
        item['download_url'] = down_urls
        return item
