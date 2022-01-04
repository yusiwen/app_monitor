import requests
import scrapy
from scrapy import Request
from packaging import version as v


from app_monitor.items import AppMonitorItem


class DockerhubSpider(scrapy.Spider):
    name = 'dockerhub'
    allowed_domains = ['docker.io']
    repos = ['dreamacro/clash-premium',
             'codercom/code-server',
             'jetbrains/upsource',
             'minio/minio',
             'bitnami/rabbitmq',
             'atlassian/confluence-server',
             'mysql/mysql-server',
             'library/consul',
             'library/sonarqube',
             'library/elasticsearch',
             'library/redis'
             ]
    login_url = 'https://auth.docker.io/token'
    query_url = 'https://registry-1.docker.io/v2/{name}/tags/list'
    token = ''

    def start_requests(self):
        scope_list = []
        for e in self.repos:
            scope_list.append('repository:' + e + ':pull')
        p = {
            'service': 'registry.docker.io',
            'scope': scope_list
        }
        r = requests.get(self.login_url, params=p)
        print(r.url)
        if r.status_code == 200:
            json = r.json()
            self.token = json['token']
        else:
            raise Exception('login failed')

        headers = {
            'Authorization': 'Bearer ' + self.token
        }
        print(headers)
        for repo in self.repos:
            url = self.query_url.format(name=repo)
            print(url)
            yield Request(
                url, headers=headers,
                cb_kwargs={'repo': repo}
            )

    def parse(self, response, **kwargs):
        json = response.json()
        tags = json['tags']
        for n, e in enumerate(tags):
            tags[n] = v.parse(e.split('/')[0])
        version = max(tags)

        item = AppMonitorItem()
        item['name'] = kwargs.get('repo')
        item['version'] = str(version)

        item['date'] = None
        item['notes'] = None
        item['category'] = 'docker'
        item['id'] = kwargs.get('repo')
        item['download_url'] = kwargs.get('repo') + ':' + str(version)
        return item