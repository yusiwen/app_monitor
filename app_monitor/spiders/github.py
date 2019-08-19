# -*- coding: utf-8 -*-
import scrapy
import json

from app_monitor.items import AppMonitorItem

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['api.github.com']
    start_urls = [
        'https://api.github.com/repos/go-gitea/gitea/releases',
        'https://api.github.com/repos/git-for-windows/git/releases',
        'https://api.github.com/repos/keeweb/keeweb/releases',
        'https://api.github.com/repos/zeit/hyper/releases'
    ]

    def parse(self, response):
        json_dict = json.loads(response.body_as_unicode())
        filtered_dict = json_dict[0]
        version = filtered_dict['tag_name']
        date = filtered_dict['created_at']
        name = response.url.rsplit('/', 2)[-2]

        item = AppMonitorItem()
        item['name'] = name
        item['version'] = version
        item['date'] = date
        item['notes'] = ''
        item['id'] = name
        return item
