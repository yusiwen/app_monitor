from urllib.parse import urljoin

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import scrapy
from scrapy import Request

from app_monitor.items import AppMonitorItem


class ChartsSpider(scrapy.Spider):
    name = 'charts'
    allowed_domains = ['helm.sh',
                       'traefik.io',
                       'hashicorp.com',
                       'github.io',
                       'bitnami.com',
                       'min.io',
                       'elastic.co',
                       'k8s-at-home.com'
                       ]
    repos = [
        {'charts': ['nfs-client-provisioner'], 'url': 'https://charts.helm.sh/stable/'},
        {'charts': ['traefik'], 'url': 'https://helm.traefik.io/traefik/'},
        {'charts': ['consul'], 'url': 'https://helm.releases.hashicorp.com/'},
        {'charts': ['portainer'], 'url': 'https://portainer.github.io/k8s/'},
        {'charts': ['ceph-csi-cephfs', 'ceph-csi-rbd'], 'url': 'https://ceph.github.io/csi-charts/'},
        {'charts': ['kube-prometheus-stack'], 'url': 'https://prometheus-community.github.io/helm-charts/'},
        {'charts': ['metrics-server'], 'url': 'https://kubernetes-sigs.github.io/metrics-server/'},
        {'charts': ['nfs-subdir-external-provisioner'], 'url': 'https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/'},
        {'charts': ['mongodb'], 'url': 'https://charts.bitnami.com/bitnami/'},
        {'charts': ['community-operator'], 'url': 'https://mongodb.github.io/helm-charts/'},
        {'charts': ['minio'], 'url': 'https://charts.min.io/'},
        {'charts': ['gocd'], 'url': 'https://gocd.github.io/helm-chart/'},
        {'charts': ['keycloak'], 'url': 'https://codecentric.github.io/helm-charts/'},
        {'charts': ['elasticsearch', 'filebeat', 'kibana', 'logstash', 'metricbeat'], 'url': 'https://helm.elastic.co/'},
        {'charts': ['deluge'], 'url': 'https://k8s-at-home.com/charts/'},
        {'charts': ['metallb'], 'url': 'https://metallb.github.io/metallb/'},
        {'charts': ['erda'], 'url': 'https://charts.erda.cloud/erda/'},
    ]

    def start_requests(self):
        for repo in self.repos:
            url = urljoin(repo['url'], 'index.yaml')
            
            yield Request(
                url,
                cb_kwargs=repo
            )

    def parse(self, response, **kwargs):
        yaml = load(response.text, Loader=Loader)
        charts = kwargs['charts']
        for chart in charts:
            latest_entry = yaml['entries'][chart][0]
            version = latest_entry['version']
            date = latest_entry['created']

            item = AppMonitorItem()
            item['name'] = chart
            item['version'] = version
            item['date'] = date
            item['notes'] = 'appVersion: ' + latest_entry['appVersion']
            item['id'] = chart
            item['category'] = 'helm chart'
            item['tags'] = 'chart'
            item['download_url'] = kwargs['url']
            yield item

