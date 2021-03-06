# -*- coding: utf-8 -*-
import scrapy

from app_monitor.items import AppMonitorItem
from datetime import datetime


class ArtifactorySpider(scrapy.Spider):
    name = 'artifactory'
    allowed_domains = ['bintray.com/jfrog']
    start_urls = [
        'https://bintray.com/jfrog/artifactory-debs/jfrog-artifactory-oss/_latestVersion']

    def parse(self, response):
        version = response.url.rsplit('/', 1)[-1]
        date = response.xpath('//div[@id="versionPublishedDate"]/text()').get()
        date = datetime.strptime(date.split('Updated in', 1)[1].strip(), '%b %d, %Y')
        datestr = date.strftime('%Y-%m-%d')


        item = AppMonitorItem()
        item['name'] = 'jfrog-artifactory-oss'
        item['version'] = version
        item['date'] = datestr
        item['notes'] = ''
        item['id'] = 'artifactory'
        item['download_url'] = 'https://bintray.com' + response.xpath(
            '//div[@id="main-content"]//div[@class="nodeDetails"]/a/@href').get()
        return item
