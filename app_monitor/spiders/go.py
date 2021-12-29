from string import Template

import scrapy

from app_monitor.items import AppMonitorItem


class GoSpider(scrapy.Spider):
    name = 'go'
    allowed_domains = ['golang.org']
    start_urls = ['https://golang.org/dl/']

    def parse(self, response, **kwargs):
        version = response.xpath('//h2[@id="stable"]/following-sibling::div[1]/@id').get().split(' ')[0].replace('go',
                                                                                                                 '')
        down_urls = []
        down_url_prefix = 'https://golang.org'
        path_templ = Template('//h2[@id="stable"]/following-sibling::div[1]//table//a[contains(text(), "$arch")]/@href')
        down_urls.append(down_url_prefix + response.xpath(path_templ.substitute(arch='linux-amd64.tar.gz')).get())
        down_urls.append(down_url_prefix + response.xpath(path_templ.substitute(arch='darwin-amd64.pkg')).get())
        down_urls.append(down_url_prefix + response.xpath(path_templ.substitute(arch='windows-amd64.msi')).get())
        down_urls.append(down_url_prefix + response.xpath(path_templ.substitute(arch='windows-amd64.zip')).get())

        item = AppMonitorItem()
        item['name'] = 'Golang'
        item['version'] = version
        item['date'] = None
        item['notes'] = ''
        item['id'] = 'go'
        item['download_url'] = down_urls
        return item
