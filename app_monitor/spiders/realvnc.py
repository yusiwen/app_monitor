import scrapy

from app_monitor.items import AppMonitorItem


class RealvncSpider(scrapy.Spider):
    name = 'realvnc'
    allowed_domains = ['realvnc.com']
    start_urls = ['https://www.realvnc.com/en/connect/download/vnc/',
                  'https://www.realvnc.com/en/connect/download/viewer/']

    def _parse_realvnc(self, response, name, app_id):
        tmp = response.xpath(
            '//div[contains(@id, "download-link")]/a[contains(@href, ".exe")]/@href').get()
        version = tmp.split('-')[-2]
        down_url = 'https://www.realvnc.com' + tmp

        item = AppMonitorItem()
        item['name'] = name
        item['version'] = version
        item['date'] = None
        item['notes'] = ''
        item['id'] = app_id
        item['download_url'] = down_url
        item['category'] = 'tool'
        item['tags'] = ['vnc', 'network']

        return item

    def parse(self, response, **kwargs):
        if response.request.url.find('viewer'):
            yield self._parse_realvnc(response, 'RealVNC Viewer', 'realvnc-viewer')
        else:
            yield self._parse_realvnc(response, 'RealVNC Server', 'realvnc-server')
