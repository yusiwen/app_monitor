import scrapy

from app_monitor.items import AppMonitorItem


class RubySpider(scrapy.Spider):
    name = 'ruby'
    allowed_domains = ['rubyinstaller.org']
    start_urls = ['https://rubyinstaller.org/downloads/']

    def parse(self, response, **kwargs):
        url = response.xpath('//h3[contains(text(), "with Devkit")]/following-sibling::ul/li[1]/a[1]/@href').get()
        version = url.rsplit('/', 2)[1].split('-', 1)[1]

        item = AppMonitorItem()
        item['name'] = 'Ruby'
        item['version'] = version

        item['date'] = None
        item['notes'] = None
        item['id'] = 'ruby'
        item['category'] = 'develop'
        item['tags'] = ['ruby', 'sdk']
        item['download_url'] = url

        return item
