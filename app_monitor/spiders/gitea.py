# -*- coding: utf-8 -*-
import scrapy
import json

from app_monitor.items import AppMonitorItem

class GiteaSpider(scrapy.Spider):
    name = 'gitea'
    allowed_domains = ['api.github.com/repos/go-gitea/gitea/releases']
    start_urls = ['http://api.github.com/repos/go-gitea/gitea/releases']

    def parse(self, response):
        json_dict = json.loads(response.body_as_unicode())
        filtered_dict = json_dict[0]
        version = filtered_dict['tag_name']
        date = filtered_dict['created_at']

        item = AppMonitorItem()
        item['name'] = 'Gitea'
        item['version'] = version
        item['date'] = date
        item['notes'] = ''
        item['id'] = 'gitea'
        return item
