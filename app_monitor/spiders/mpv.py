from datetime import datetime

import scrapy

from app_monitor.items import AppMonitorItem


class MpvSpider(scrapy.Spider):
    name = 'mpv'
    allowed_domains = ['sourceforge.net']
    start_urls = ['https://sourceforge.net/p/mpv-player-windows/activity/feed']

    def parse(self, response):
        ver_str = response.xpath('//channel/item[1]/title/text()').get()
        date_str = response.xpath('//channel/item[1]/pubDate/text()').get()
        version = ver_str.split()[-1].split('/')[-1].split('-')[2]

        d = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        date = d.strftime('%Y-%m-%d')

        item = AppMonitorItem()
        item['name'] = 'mpv'
        item['version'] = version
        item['date'] = date
        item['notes'] = ''
        item['id'] = 'mpv'
        item['category'] = 'tool'
        item['tags'] = ['media', 'player']
        item['download_url'] = response.xpath('//channel/item[1]/guid/text()').get()
        return item
