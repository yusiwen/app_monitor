from datetime import datetime

import scrapy

from app_monitor.items import AppMonitorItem


class SysinternalsSpider(scrapy.Spider):
    name = 'sysinternals'
    allowed_domains = ['microsoft.com']
    start_urls = [
        'https://docs.microsoft.com/zh-cn/sysinternals/downloads/tcpview',
        'https://docs.microsoft.com/zh-cn/sysinternals/downloads/process-explorer',
        'https://docs.microsoft.com/zh-cn/sysinternals/downloads/procmon',
        'https://docs.microsoft.com/zh-cn/sysinternals/downloads/vmmap',
        'https://docs.microsoft.com/zh-cn/sysinternals/downloads/rammap',
        'https://docs.microsoft.com/zh-cn/sysinternals/downloads/sdelete'
    ]

    def parse(self, response, **kwargs):
        app_id = response.request.url.rsplit('/', 3)[-1]
        version = response.xpath('//main/h1')[0].xpath('text()').get().split(' ')[-1]
        date = response.xpath('//main//p[contains(text(), "Published: ")]/text()').get().split(': ')[-1]
        date = datetime.strptime(date, '%B %d, %Y')
        date = datetime.strftime(date, '%Y-%m-%d')
        down_url = response.xpath('//main//a[@data-linktype="external"]/@href').get()

        item = AppMonitorItem()
        item['name'] = app_id
        item['version'] = version
        item['date'] = date
        item['notes'] = ''
        item['id'] = app_id
        item['download_url'] = down_url
        item['category'] = 'tool'
        return item
