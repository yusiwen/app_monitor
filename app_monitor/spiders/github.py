# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from app_monitor import settings
from app_monitor.items import AppMonitorItem


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['api.github.com']
    template_url = 'https://api.github.com/repos/{repo_name}/releases/latest'
    repos = [
        ['adobe-fonts/source-han-sans', 'font'],
        ['adoptium/temurin8-binaries', 'develop'],
        ['adoptium/temurin11-binaries', 'develop'],
        ['adoptium/temurin17-binaries', 'develop'],
        ['Alexey-T/CudaText', 'tool'],
        ['alibaba/arthas', 'develop'],
        ['alibaba/Sentinel', 'develop'],
        ['audacity/audacity', 'tool'],
        ['beekeeper-studio/beekeeper-studio', 'develop'],
        ['Dreamacro/clash', 'tool'],
        ['Eugeny/tabby', 'tool'],
        ['Fndroid/clash_for_windows_pkg', 'tool'],
        ['Requarks/wiki', 'tool'],
        ['alibaba/jetcache', 'develop'],
        ['alibaba/nacos', 'develop'],
        ['ankitects/anki', 'tool'],
        ['be5invis/Iosevka', 'font'],
        ['be5invis/Sarasa-Gothic', 'font'],
        ['cdr/code-server', 'develop'],
        ['cmderdev/cmder', 'tool'],
        ['dbeaver/dbeaver', 'develop'],
        ['elastic/elasticsearch', 'develop'],
        ['elastic/kibana', 'develop'],
        ['elastic/logstash', 'develop'],
        ['FredrikNoren/ungit', 'develop'],
        ['git-for-windows/git', 'develop'],
        ['gitahead/gitahead', 'develop'],
        ['gitextensions/gitextensions', 'develop'],
        ['go-gitea/gitea', 'develop'],
        ['goharbor/harbor', 'develop'],
        ['graalvm/graalvm-ce-builds', 'develop'],
        ['gradle/gradle', 'develop'],
        ['grafana/grafana', 'develop'],
        ['harness/drone', 'develop'],
        ['hashicorp/consul', 'develop'],
        ['HeidiSQL/HeidiSQL', 'develop'],
        ['janeczku/calibre-web', 'tool'],
        ['jenkinsci/jenkins', 'develop'],
        ['keeweb/keeweb', 'tool'],
        ['koalaman/shellcheck', 'tool'],
        ['kubeedge/kubeedge', 'develop'],
        ['kubernetes-sigs/kind', 'develop'],
        ['kubernetes/kubernetes', 'develop'],
        ['kubernetes/minikube', 'develop'],
        ['laurent22/joplin', 'tool'],
        ['lxgw/LxgwWenKai', 'font'],
        ['medcl/elasticsearch-analysis-ik', 'develop'],
        ['microsoft/cascadia-code', 'font'],
        ['microsoft/vscode', 'develop'],
        ['minio/minio', 'develop'],
        ['PowerShell/Win32-OpenSSH', 'tool'],
        ['prometheus/node_exporter', 'develop'],
        ['prometheus/prometheus', 'develop'],
        ['prometheus/pushgateway', 'develop'],
        ['qishibo/AnotherRedisDesktopManager', 'develop'],
        ['redis/redis', 'develop'],
        ['rust-lang/rust', 'develop'],
        ['shadowsocks/ShadowsocksX-NG', 'tool'],
        ['shadowsocks/shadowsocks-windows', 'tool'],
        ['tmux/tmux', 'tool'],
        ['tonsky/FiraCode', 'font'],
        ['visualfc/liteide', 'develop'],
        ['zealdocs/zeal' 'tool'],
    ]
    http_user = settings.GITHUB_USER
    http_pass = settings.GITHUB_ACCESS_TOKEN

    def start_requests(self):
        for repo in self.repos:
            url = self.template_url.format(repo_name=repo[0])
            print(url)
            yield Request(
                url,
                cb_kwargs={'repo': repo[0], 'category': repo[1]}
            )

    def parse(self, response, **kwargs):
        json_dict = response.json()
        app_id = kwargs['repo']
        version = json_dict['tag_name']
        date = json_dict['created_at']

        item = AppMonitorItem()
        item['name'] = app_id
        item['version'] = version
        item['date'] = date
        item['notes'] = ''
        item['id'] = app_id
        item['category'] = kwargs['category']
        item['download_url'] = json_dict['html_url']
        return item
