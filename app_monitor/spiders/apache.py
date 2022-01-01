import scrapy

from app_monitor.items import AppMonitorItem


class ApacheSpider(scrapy.Spider):
    name = 'apache'
    allowed_domains = ['apache.org']
    start_urls = ['http://maven.apache.org/download.cgi',
                  'https://tomcat.apache.org/download-80.cgi',
                  'https://tomcat.apache.org/download-90.cgi',
                  'http://karaf.apache.org/download.html',
                  'https://felix.apache.org/downloads.cgi']

    def _parse_maven(self, response):
        version = response.xpath(
            '//main/section/h2/text()').get().split(' ')[-1]
        item = AppMonitorItem()
        item['name'] = 'Apache Maven'
        item['version'] = version
        item['date'] = None
        item['notes'] = ''
        item['id'] = 'apache-maven'
        item['category'] = 'develop'
        item['download_url'] = response.xpath(
            '//main/section/section/table//a[contains(text(),"bin.zip")]/@href').get()
        return item

    def _parse_tomcat(self, ver_no, response):
        str_ver_no = str(ver_no)
        version = response.xpath(
            '//main//div[@id="content"]/h3[contains(text(), "' + str_ver_no + '.")]/text()').get()
        item = AppMonitorItem()
        item['name'] = 'Apache Tomcat ' + str_ver_no
        item['version'] = version
        item['date'] = None
        item['notes'] = ''
        item['category'] = 'develop'
        item['id'] = 'apache-tomcat' + str_ver_no

        down_urls = [response.xpath(
            '//main//div[@id="content"]//li[contains(text(), "Core")]/ul/li/a[text()[re:test(., "^zip$")]]/@href').get(),
                     response.xpath(
                         '//main//div[@id="content"]//li[contains(text(), "documentation")]/ul/li/a/@href').get(),
                     response.xpath(
                         '//main//div[@id="content"]//li[contains(text(), "Deployer")]/ul/li/a[text()[re:test(., '
                         '"^zip$")]]/@href').get()]
        item['download_url'] = down_urls
        return item

    def _parse_karaf(self, response):
        core_version = response.xpath(
            '//main//h3[contains(text(), "Karaf Runtime")]/span/text()').get()

        item = AppMonitorItem()
        item['name'] = 'Apache Karaf Runtime'
        item['version'] = core_version
        item['date'] = None
        item['notes'] = ''
        item['category'] = 'develop'
        item['id'] = 'apache-karaf-runtime'
        item['download_url'] = response.xpath(
            '//main//h3[contains(text(), "Karaf Runtime")]//following-sibling::p[contains(text(), '
            '"Binary Distribution")]/a[contains(text(), "zip")]/@href').get()
        yield item

        cellar_version = response.xpath(
            '//main//h3[contains(text(), "Karaf Cellar")]/span/text()').get()
        item = AppMonitorItem()
        item['name'] = 'Apache Karaf Cellar'
        item['version'] = cellar_version
        item['date'] = None
        item['notes'] = ''
        item['category'] = 'develop'
        item['id'] = 'apache-karaf-cellar'
        item['download_url'] = 'http://karaf.apache.org/download.html#cellar-installation'
        yield item

        cave_version = response.xpath(
            '//main//h3[contains(text(), "Karaf Cave")]/span/text()').get()
        item = AppMonitorItem()
        item['name'] = 'Apache Karaf Cave'
        item['version'] = cave_version
        item['date'] = None
        item['notes'] = ''
        item['category'] = 'develop'
        item['id'] = 'apache-karaf-cave'
        item['download_url'] = 'http://karaf.apache.org/download.html#cave-installation'
        yield item

        decanter_version = response.xpath(
            '//main//h3[contains(text(), "Karaf Decanter")]/span/text()').get()
        item = AppMonitorItem()
        item['name'] = 'Apache Karaf Decanter'
        item['version'] = decanter_version
        item['date'] = None
        item['notes'] = ''
        item['category'] = 'develop'
        item['id'] = 'apache-karaf-decanter'
        item['download_url'] = 'http://karaf.apache.org/download.html#decanter-installation'
        yield item

    def _parse_felix(self, response):
        base_path = '//div[@class="main"]//table[@class="table"]/tbody/tr/td[contains(text(), "Felix Framework ' \
                    'Distribution")] '
        version = response.xpath(
            base_path + '/following-sibling::td[1]/text()').get().split(' ')[0]

        item = AppMonitorItem()
        item['name'] = 'Apache Felix'
        item['version'] = version
        item['date'] = None
        item['notes'] = 'Changelog: ' + response.xpath(base_path +
                                                       '/following-sibling::td[1]/a/@href').get()
        item['id'] = 'apache-felix'
        item['category'] = 'develop'
        item['download_url'] = response.xpath(base_path +
                                              '/following-sibling::td[2]/a[contains(text(), "zip")]/@href').get()
        return item

    def parse(self, response, **kwargs):
        unit = response.url.split('//')[-1].split('.')[0]
        if unit == 'maven':
            return self._parse_maven(response)
        elif unit == 'tomcat':
            title = response.xpath('//title/text()').get().find("Tomcat 8")
            if title > 0:
                return self._parse_tomcat(8, response)
            else:
                return self._parse_tomcat(9, response)
        elif unit == 'karaf':
            return self._parse_karaf(response)
        elif unit == 'felix':
            return self._parse_felix(response)
        else:
            return None
