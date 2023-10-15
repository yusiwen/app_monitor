import scrapy
from packaging import version as v

from app_monitor.items import AppMonitorItem


class ArtifactorySpider(scrapy.Spider):
    name = 'artifactory'
    allowed_domains = ['releases-docker.jfrog.io']
    start_urls = [
        'https://releases-docker.jfrog.io/artifactory/docker/jfrog/artifactory-oss/']

    def parse(self, response, **kwargs):
        vers = list(filter(lambda s: s[0:1].isnumeric(),
                           list(map(lambda s: s.replace('/', ''), response.xpath('.//a[@href]/@href').getall()))))
        for n, i in enumerate(vers):
            vers[n] = v.parse(i)
        version = max(vers)

        item = AppMonitorItem()
        item['name'] = 'Artifactory OSS'
        item['version'] = str(version)

        item['date'] = None
        item['notes'] = None
        item['category'] = 'tool'
        item['tags'] = ['vps', 'maven', 'ci/cd']
        item['id'] = 'artifactory_oss'
        item[
            'download_url'] = 'https://releases.jfrog.io/artifactory/artifactory-debs/pool/jfrog-artifactory-oss' \
                              '/jfrog-artifactory-oss-[RELEASE].deb '

        return item
