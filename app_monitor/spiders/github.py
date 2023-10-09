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
        {'repo': 'adobe-fonts/source-han-sans', 'category': 'font', 'tags': ['font']},
        {'repo': 'adoptium/temurin8-binaries', 'category': 'develop', 'tags': ['java', 'jdk', 'jdk8']},
        {'repo': 'adoptium/temurin11-binaries', 'category': 'develop', 'tags': ['java', 'jdk', 'jdk11']},
        {'repo': 'adoptium/temurin17-binaries', 'category': 'develop', 'tags': ['java', 'jdk', 'jdk17']},
        {'repo': 'adoptium/temurin18-binaries', 'category': 'develop', 'tags': ['java', 'jdk', 'jdk18']},
        {'repo': 'Alexey-T/CudaText', 'category': 'tool', 'tags': ['editor']},
        {'repo': 'alexkulya/pandaria_5.4.8', 'category': 'game', 'tags': ['wow', 'pandaria']},
        {'repo': 'alibaba/arthas', 'category': 'develop', 'tags': ['java', 'debug', 'diagnostic']},
        {'repo': 'alibaba/jetcache', 'category': 'develop', 'tags': ['java', 'library', 'cache']},
        {'repo': 'alibaba/nacos', 'category': 'develop', 'tags': ['java', 'service discovery',
                                                                  'configuration management', 'microservice']},
        {'repo': 'alibaba/Sentinel', 'category': 'develop', 'tags': ['java', 'flow control', 'microservice']},
        {'repo': 'ankitects/anki', 'category': 'tool', 'tags': ['notetaking']},
        {'repo': 'audacity/audacity', 'category': 'tool', 'tags': ['audio']},
        {'repo': 'beekeeper-studio/beekeeper-studio', 'category': 'develop', 'tags': ['database']},
        {'repo': 'be5invis/Iosevka', 'category': 'font', 'tags': ['font']},
        {'repo': 'be5invis/Sarasa-Gothic', 'category': 'font', 'tags': ['font']},
        {'repo': 'derailed/k9s', 'category': 'tool', 'tags': ['cloud computing', 'kubernetes']},
        {'repo': 'cdr/code-server', 'category': 'tool', 'tags': ['vps', 'ide']},
        {'repo': 'cilium/cilium', 'category': 'tool', 'tags': ['cloud computing', 'kubernetes', 'cni']},
        {'repo': 'cilium/cilium-cli', 'category': 'tool', 'tags': ['cloud computing', 'kubernetes', 'cni']},
        {'repo': 'cilium/hubble', 'category': 'tool', 'tags': ['cloud computing', 'kubernetes', 'cni']},
        {'repo': 'cmderdev/cmder', 'category': 'tool', 'tags': ['terminal']},
        {'repo': 'containerd/containerd', 'category': 'tool', 'tags': ['container', 'cloud computing']},
        {'repo': 'containerd/nerdctl', 'category': 'tool', 'tags': ['container', 'cloud computing']},
        {'repo': 'CopyTranslator/CopyTranslator', 'category': 'tool', 'tags': ['language', 'translator']},
        {'repo': 'dandavison/delta', 'category': 'tools', 'tags': ['cli', 'pager']},
        {'repo': 'dbeaver/cloudbeaver', 'category': 'develop', 'tags': ['cloud computing', 'database']},
        {'repo': 'dbeaver/dbeaver', 'category': 'develop', 'tags': ['database']},
        {'repo': 'docker/compose', 'category': 'develop', 'tags': ['container']},
        {'repo': 'dzikoysk/reposilite', 'category': 'develop', 'tags': ['maven']},
        {'repo': 'Dreamacro/clash', 'category': 'tool', 'tags': ['gfw']},
        {'repo': 'elastic/elasticsearch', 'category': 'develop', 'tags': ['middleware']},
        {'repo': 'elastic/kibana', 'category': 'develop', 'tags': ['middleware']},
        {'repo': 'elastic/logstash', 'category': 'develop', 'tags': ['middleware']},
        {'repo': 'etcd-io/etcd', 'category': 'develop', 'tags': ['k8s', 'etcd']},
        {'repo': 'Eugeny/tabby', 'category': 'tool', 'tags': ['terminal']},
        {'repo': 'flannel-io/flannel', 'category': 'develop', 'tags': ['k8s', 'cni']},
        {'repo': 'Fndroid/clash_for_windows_pkg', 'category': 'tool', 'tags': ['gfw']},
        {'repo': 'FredrikNoren/ungit', 'category': 'develop', 'tags': ['git', 'vcs']},
        {'repo': 'gchudov/cuetools.net', 'category': 'tools', 'tags': ['media', 'cue']},
        {'repo': 'git-for-windows/git', 'category': 'develop', 'tags': ['git', 'vcs']},
        {'repo': 'gitahead/gitahead', 'category': 'develop', 'tags': ['git', 'vcs']},
        {'repo': 'gitextensions/gitextensions', 'category': 'develop', 'tags': ['git', 'vcs']},
        {'repo': 'go-gitea/gitea', 'category': 'tool', 'tags': ['git', 'vcs', 'vps']},
        {'repo': 'goharbor/harbor', 'category': 'tool', 'tags': ['vps', 'docker']},
        {'repo': 'graalvm/graalvm-ce-builds', 'category': 'develop', 'tags': ['java', 'jdk']},
        {'repo': 'gradle/gradle', 'category': 'develop', 'tags': ['java', 'build']},
        {'repo': 'grafana/grafana', 'category': 'develop', 'tags': ['middleware', 'monitoring']},
        {'repo': 'harness/drone', 'category': 'tool', 'tags': ['vps', 'ci/cd', 'devops']},
        {'repo': 'hashicorp/consul', 'category': 'develop', 'tags': ['java', 'service discovery',
                                                                     'configuration management', 'microservice']},
        {'repo': 'hashicorp/vagrant', 'category': 'tool', 'tags': ['virtualization']},
        {'repo': 'HeidiSQL/HeidiSQL', 'category': 'develop', 'tags': ['database']},
        {'repo': 'henrypp/memreduct', 'category': 'tool', 'tags': ['windows', 'memory']},
        {'repo': 'henrypp/simplewall', 'category': 'tool',
         'tags': ['windows', 'security', 'firewall', 'administration']},
        {'repo': 'IrineSistiana/mosdns', 'category': 'tool', 'tags': ['network', 'dns', 'gfw']},
        {'repo': 'IrineSistiana/mosdns-cn', 'category': 'tool', 'tags': ['network', 'dns', 'gfw']},
        {'repo': 'janeczku/calibre-web', 'category': 'tool', 'tags': ['vps', 'book', 'reading']},
        {'repo': 'jenkinsci/jenkins', 'category': 'tool', 'tags': ['vps', 'ci/cd']},
        {'repo': 'jgraph/drawio-desktop', 'category': 'tool', 'tags': ['chart', 'design']},
        {'repo': 'jonz94/Sarasa-Gothic-Nerd-Fonts', 'category': 'font', 'tags': ['font', 'nerd font']},
        {'repo': 'junegunn/fzf', 'category': 'tool', 'tags': ['cli', 'search', 'filter']},
        {'repo': 'keeweb/keeweb', 'category': 'tool', 'tags': ['security', 'password manager']},
        {'repo': 'koalaman/shellcheck', 'category': 'tool', 'tags': ['shell', 'analyzer']},
        {'repo': 'kubeedge/kubeedge', 'category': 'develop',
         'tags': ['cloud computing', 'kubernetes', 'edge computing']},
        {'repo': 'kubernetes-sigs/kind', 'category': 'develop', 'tags': ['cloud computing', 'kubernetes']},
        {'repo': 'kubernetes/kubernetes', 'category': 'develop', 'tags': ['cloud computing', 'kubernetes']},
        {'repo': 'kubernetes/minikube', 'category': 'develop', 'tags': ['cloud computing', 'kubernetes']},
        {'repo': 'laurent22/joplin', 'category': 'tool', 'tags': ['notetaking']},
        {'repo': 'lensapp/lens', 'category': 'tool', 'tags': ['cloud computing', 'kubernetes']},
        {'repo': 'lxgw/LxgwWenKai', 'category': 'font', 'tags': ['font']},
        {'repo': 'marktext/marktext', 'category': 'tool', 'tags': ['markdown', 'editor']},
        {'repo': 'medcl/elasticsearch-analysis-ik', 'category': 'develop', 'tags': ['middleware', 'plugin']},
        {'repo': 'metallb/metallb', 'category': 'develop', 'tags': ['k8s', 'lb']},
        {'repo': 'microsoft/cascadia-code', 'category': 'font', 'tags': ['font']},
        {'repo': 'microsoft/terminal', 'category': 'tool', 'tags': ['terminal']},
        {'repo': 'microsoft/vscode', 'category': 'tool', 'tags': ['ide']},
        {'repo': 'minio/minio', 'category': 'tool', 'tags': ['vps', 'oss']},
        {'repo': 'nvm-sh/nvm', 'category': 'tool', 'tags': ['nodejs']},
        {'repo': 'obsidianmd/obsidian-releases', 'category': 'tool', 'tags': ['notetaking', 'markdown']},
        {'repo': 'ogham/exa', 'category': 'tool', 'tags': ['cli', 'file-system']},
        {'repo': 'PowerShell/Win32-OpenSSH', 'category': 'tool', 'tags': ['network', 'ssh']},
        {'repo': 'prometheus/node_exporter', 'category': 'develop', 'tags': ['middleware', 'monitoring']},
        {'repo': 'prometheus/prometheus', 'category': 'develop', 'tags': ['middleware', 'monitoring']},
        {'repo': 'prometheus/pushgateway', 'category': 'develop', 'tags': ['middleware', 'monitoring']},
        {'repo': 'qishibo/AnotherRedisDesktopManager', 'category': 'tool', 'tags': ['cache']},
        {'repo': 'redis/redis', 'category': 'develop', 'tags': ['middleware', 'cache']},
        {'repo': 'Requarks/wiki', 'category': 'tool', 'tags': ['vps', 'wiki']},
        {'repo': 'rootless-containers/rootlesskit', 'category': 'tool', 'tags': ['container', 'cloud computing']},
        {'repo': 'rootless-containers/slirp4netns', 'category': 'tool', 'tags': ['container', 'cloud computing']},
        {'repo': 'rust-lang/rust', 'category': 'develop', 'tags': ['rust']},
        {'repo': 'shadowsocks/ShadowsocksX-NG', 'category': 'tool', 'tags': ['gfw']},
        {'repo': 'shadowsocks/shadowsocks-windows', 'category': 'tool', 'tags': ['gfw']},
        {'repo': 'ShareX/ShareX', 'category': 'tool', 'tags': ['screenshot', 'ocr']},
        {'repo': 'sharkdp/bat', 'category': 'tool', 'tags': ['cli']},
        {'repo': 'sumatrapdfreader/sumatrapdf', 'category': 'tool', 'tags': ['pdf']},
        {'repo': 'tmux/tmux', 'category': 'tool', 'tags': ['terminal']},
        {'repo': 'tonsky/FiraCode', 'category': 'font', 'tags': ['font']},
        {'repo': 'traefik/traefik', 'category': 'develop', 'tags': ['k8s', 'cloud native', 'gateway']},
        {'repo': 'visualfc/liteide', 'category': 'develop', 'tags': ['go', 'ide']},
        {'repo': 'wez/wezterm', 'category': 'tool', 'tags': ['terminal', 'desktop']},
        {'repo': 'wagoodman/dive', 'category': 'tool', 'tags': ['docker', 'cloud', 'container']},
        {'repo': 'zealdocs/zeal', 'category': 'tool', 'tags': ['reference', 'document', 'reading']},
    ]
    http_user = settings.GITHUB_USER
    http_pass = settings.GITHUB_ACCESS_TOKEN

    def start_requests(self):
        for repo in self.repos:
            url = self.template_url.format(repo_name=repo['repo'])
            self.logger.info("Send request to %s", url)
            yield Request(
                url,
                cb_kwargs=repo
            )

    def parse(self, response, **kwargs):
        self.logger.info("Parse response on %s", response.url)
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
        item['tags'] = kwargs['tags']
        item['download_url'] = json_dict['html_url']
        return item
