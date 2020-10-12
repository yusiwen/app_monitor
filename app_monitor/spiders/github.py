# -*- coding: utf-8 -*-
import scrapy
import json
import re

from app_monitor.items import AppMonitorItem

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['api.github.com']
    start_urls = [
        'https://api.github.com/repos/go-gitea/gitea/releases',
        'https://api.github.com/repos/git-for-windows/git/releases',
        'https://api.github.com/repos/keeweb/keeweb/releases',
        'https://api.github.com/repos/zeit/hyper/releases',
        'https://api.github.com/repos/gitextensions/gitextensions/releases',
        'https://api.github.com/repos/cmderdev/cmder/releases',
        'https://api.github.com/repos/shadowsocks/ShadowsocksX-NG/releases',
        'https://api.github.com/repos/be5invis/Sarasa-Gothic/releases',
    ]

    def _parse_assets(self, app_id, version, **data):
        filtered = data['assets']
        output = []
        if app_id == 'gitea':
            output = [x for x in filtered if x['name'] == 'gitea-' + version[1:] + '-linux-amd64']
        elif app_id == 'keeweb':
            o1 = [x for x in filtered if x['name'] == 'KeeWeb-' + version[1:] + '.win.x64.zip']
            o2 = [x for x in filtered if x['name'] == 'KeeWeb-' + version[1:] + '.linux.x64.deb']
            o3 = [x for x in filtered if x['name'] == 'KeeWeb-' + version[1:] + '.mac.dmg']
            output = o1 + o2 + o3
        elif app_id == 'git':
            output = [x for x in filtered if x['name'] == 'Git-' + version + '-64-bit.exe']

        if len(output) == 1:
            return output[0]['browser_download_url']
        elif len(output) > 1:
            urls = []
            for o in output:
                urls.append(o['browser_download_url'])
            return urls
        else:
            return ''


    def parse(self, response):
        app_id = response.url.rsplit('/', 2)[-2]
        json_dict = json.loads(response.text())
        if app_id == 'git':
            p = re.compile('^Git\sfor\sWindows.*')
            tmp = [x for x in json_dict if p.match(x['name'])]
            filtered_dict = tmp[0]
            version = filtered_dict['name'].replace('Git for Windows ', '').strip()
        else:
            filtered_dict = json_dict[0]
            version = filtered_dict['tag_name']

        date = filtered_dict['created_at']

        item = AppMonitorItem()
        item['name'] = app_id
        item['version'] = version
        item['date'] = date
        item['notes'] = ''
        item['app_id'] = app_id
        item['download_url'] = self._parse_assets(app_id, version, filtered_dict)
        return item

