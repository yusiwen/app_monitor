import scrapy
from app_monitor.items import AppMonitorItem


class FilezillaSpider(scrapy.Spider):
    name = 'filezilla'
    allowed_domains = ['filezilla-project.org']
    start_urls = ['https://filezilla-project.org/download.php?show_all=1']

    def parse(self, response):
        version = response.xpath('//p[contains(text(), "latest stable version")]/text()').get().split(' ')[-1]
        down_urls = []
        down_urls.append(response.xpath('//a[contains(text(), "win64.zip")]/@href').get())
        down_urls.append(response.xpath('//a[contains(text(), "macosx-x86.app.tar.bz2")]/@href').get())
        down_urls.append(response.xpath('//a[contains(text(), "x86_64-linux-gnu.tar.bz2")]/@href').get())

        item = AppMonitorItem()
        item['name'] = 'FileZilla'
        item['version'] = version
        item['date'] = None
        item['notes'] = ''
        item['id'] = 'filezilla'
        item['download_url'] = down_urls
        return item
        pass
