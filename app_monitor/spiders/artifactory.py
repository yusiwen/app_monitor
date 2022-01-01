import scrapy

from app_monitor.items import AppMonitorItem
from packaging import version as v


class ArtifactorySpider(scrapy.Spider):
    name = 'artifactory'
    allowed_domains = ['releases.jfrog.io']
    start_urls = [
        'https://releases.jfrog.io/artifactory/bintray-artifactory/org/artifactory/oss/jfrog-artifactory-oss/']

    def parse(self, response, **kwargs):
        vers = response.xpath('/html/body/pre[2]/a/text()').getall()
        for n, e in enumerate(vers):
            vers[n] = v.parse(e.split('/')[0])
        version = max(vers)

        item = AppMonitorItem()
        item['name'] = 'Artifactory OSS'
        item['version'] = str(version)

        item['date'] = None
        item['notes'] = None
        item['category'] = 'develop'
        item['id'] = 'artifactory_oss'
        item[
            'download_url'] = 'https://releases.jfrog.io/artifactory/artifactory-debs/pool/jfrog-artifactory-oss/jfrog-artifactory-oss-[RELEASE].deb'

        return item
