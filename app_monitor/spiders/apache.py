import re

import scrapy
from scrapy import Request

from app_monitor.items import AppMonitorItem
from packaging.version import parse


class ApacheSpider(scrapy.Spider):
    name = 'apache'
    allowed_domains = ['apache.org']
    repos = [
        {'repo': 'apache-karaf-runtime', 'name': 'Apache Karaf Runtime', 'url': 'https://dlcdn.apache.org/karaf/',
         'tags': ['java', 'osgi', 'karaf', 'apache']},
        {'repo': 'apache-karaf-cave', 'name': 'Apache Karaf Cave', 'url': 'https://dlcdn.apache.org/karaf/cave/',
         'tags': ['java', 'osgi', 'karaf', 'apache']},
        {'repo': 'apache-karaf-cellar', 'name': 'Apache Karaf Cellar', 'url': 'https://dlcdn.apache.org/karaf/cellar/',
         'tags': ['java', 'osgi', 'karaf', 'apache']},
        {'repo': 'apache-karaf-decanter', 'name': 'Apache Karaf Decanter', 'url': 'https://dlcdn.apache.org/karaf/decanter/',
         'tags': ['java', 'osgi', 'karaf', 'apache']},
        {'repo': 'apache-maven3', 'name': 'Apache Maven 3.x', 'url': 'https://dlcdn.apache.org/maven/maven-3/',
         'tags': ['java', 'build', 'maven', 'apache']},
        {'repo': 'apache-maven4', 'name': 'Apache Maven 4.x', 'url': 'https://dlcdn.apache.org/maven/maven-4/',
         'tags': ['java', 'build', 'maven', 'apache']},
        {'repo': 'apache-tomcat8', 'name': 'Apache Tomcat 8.x', 'url': 'https://dlcdn.apache.org/tomcat/tomcat-8/',
         'tags': ['java', 'tomcat', 'web', 'apache']},
        {'repo': 'apache-tomcat9', 'name': 'Apache Tomcat 9.x', 'url': 'https://dlcdn.apache.org/tomcat/tomcat-9/',
         'tags': ['java', 'tomcat', 'web', 'apache']},
        {'repo': 'apache-tomcat10', 'name': 'Apache Tomcat 10.x', 'url': 'https://dlcdn.apache.org/tomcat/tomcat-10/',
         'tags': ['java', 'tomcat', 'web', 'apache']},
    ]

    def _get_latest_version(self, links):
        reg = re.compile(r'^(\d|v\d).*')
        # list of {original_ver, ver}
        versions = list(map(lambda x: dict(original_ver=x, ver=parse(x)),
                            list(map(lambda x: x.rstrip('/'), list(filter(reg.search, links))))))
        # return the max version compared by 'ver'
        return max(versions, key=lambda x: x['ver'])

    def _parse_latest_version_contents(self, response, version, id, name, tags):
        if len(response.xpath('//a[contains(text(), "binaries")]').getall()) > 0:
            yield scrapy.Request(response.url + "binaries", callback=self._parse_latest_version_contents,
                                 cb_kwargs=dict(version=version, id=id, name=name,
                                                tags=tags))
        elif len(response.xpath('//a[contains(text(), "bin")]').getall()) > 0:
            yield scrapy.Request(response.url + "bin", callback=self._parse_latest_version_contents,
                                 cb_kwargs=dict(version=version, id=id, name=name,
                                                tags=tags))
        else:
            item = AppMonitorItem()
            item['name'] = name
            item['version'] = version
            item['date'] = None
            item['notes'] = ''
            item['category'] = 'develop'
            item['tags'] = tags
            item['id'] = id

            reg = re.compile(r'^apache-.*')
            urls = response.xpath('//a/@href').getall()
            urls = list(map(lambda x: response.url + x, list(filter(reg.search, urls))))
            item['download_url'] = urls
            yield item

    def _parse_repo(self, response, **kwargs):
        core_version = self._get_latest_version(response.xpath('//pre//a/text()').getall())
        url = kwargs['url'] + "{version}/"
        # use 'original_ver' because 'ver' could be converted by packaging.version to semver format.
        # e.g. '4.0.0-alpha-8' to '4.0.0a8'
        url = url.format(version=core_version['original_ver'])
        yield scrapy.Request(url, callback=self._parse_latest_version_contents,
                             cb_kwargs=dict(version=core_version['original_ver'], id=kwargs['repo'],
                                            name=kwargs['name'],
                                            tags=kwargs['tags']))

    def start_requests(self):
        if hasattr(self, 'repo') and len(self.repo) > 0:
            hit = False
            for r in self.repos:
                if r['repo'] == self.repo:
                    self.logger.info("Send request to %s", r['url'])
                    yield Request(
                        r['url'],
                        cb_kwargs=r
                    )
                    hit = True
                    break
            if not hit:
                self.logger.error("Repo %s is not configured", self.repo)
        else:
            for repo in self.repos:
                self.logger.info("Send request to %s", repo['url'])
                yield Request(
                    repo['url'],
                    cb_kwargs=repo
                )

    def parse(self, response, **kwargs):
        return self._parse_repo(response, **kwargs)
