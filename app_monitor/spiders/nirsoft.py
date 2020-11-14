import scrapy
import re

from app_monitor.items import AppMonitorItem


class NirsoftSpider(scrapy.Spider):
    name = 'nirsoft'
    allowed_domains = ['www.nirsoft.net']
    start_urls = [
        'http://www.nirsoft.net/utils/multiple_ping_tool.html',
        'http://www.nirsoft.net/utils/awatch.html',
        'http://www.nirsoft.net/utils/network_route_view.html',
        'http://www.nirsoft.net/utils/full_event_log_view.html',
        'http://www.nirsoft.net/utils/registered_dll_view.html',
        'http://www.nirsoft.net/utils/dll_export_viewer.html',
        'http://www.nirsoft.net/utils/registered_dll_view.html'
    ]

    def parse(self, response):
        title = response.xpath('//table[@class="utilcaption"]//td')[1].xpath('text()').get()
        version = re.search(r'v([\d.]+)', title).group(0)
        app_id = title.split(version)[0].strip()

        r = response.xpath('//a[@class="downloadline"]')
        down_urls = []
        for i in r:
            x = i.xpath('@href').get()
            if not x.startswith('http'):
                x = 'http://www.nirsoft.net/utils/' + x
            down_urls.append(x)

        item = AppMonitorItem()
        item['name'] = app_id
        item['version'] = version
        item['date'] = None
        item['notes'] = ''
        item['id'] = app_id
        item['download_url'] = down_urls
        return item
