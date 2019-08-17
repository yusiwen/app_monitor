# -*- coding: utf-8 -*-
import scrapy

from app_monitor.items import AppMonitorItem

class ArtifactorySpider(scrapy.Spider):
    name = 'artifactory'
    allowed_domains = ['bintray.com/jfrog/artifactory-debs/jfrog-artifactory-oss-deb']
    start_urls = ['https://bintray.com/jfrog/artifactory-debs/jfrog-artifactory-oss-deb/_latestVersion']

    def parse(self, response):
        version = response.url.rsplit('/', 1)[-1]
        date = response.xpath('//div[@id="versionPublishedDate"]/text()').get()
        date = date.split('Updated',1)[1].strip()

        item = AppMonitorItem()
        item['name'] = 'jfrog-artifactory-oss-deb'
        item['version'] = version
        item['date'] = date
        item['notes'] = ''
        item['id'] = 'artifactory'
        return item
