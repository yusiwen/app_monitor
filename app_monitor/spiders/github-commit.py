# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from app_monitor import settings
from app_monitor.items import AppMonitorItem


class GithubSpider(scrapy.Spider):
    name = 'github-commit'
    allowed_domains = ['api.github.com']
    template_url = 'https://api.github.com/repos/{repo_name}/commits'
    repos = [
        {'repo': 'alexkulya/pandaria_5.4.8', 'category': 'game', 'tags': ['wow']},
    ]
    http_user = settings.GITHUB_USER
    http_pass = settings.GITHUB_ACCESS_TOKEN

    def start_requests(self):
        for repo in self.repos:
            url = self.template_url.format(repo_name=repo['repo'])
            print(url)
            yield Request(
                url,
                cb_kwargs=repo
            )

    def parse(self, response, **kwargs):
        json_dict = response.json()
        committer = json_dict[0]['commit']['committer']
        tree = json_dict[0]['commit']['tree']
        app_id = kwargs['repo']
        version = tree['sha']
        date = committer['date']

        item = AppMonitorItem()
        item['name'] = app_id
        item['version'] = version
        item['date'] = date
        item['notes'] = ''
        item['id'] = app_id
        item['type'] = 'commit'
        item['category'] = kwargs['category']
        item['tags'] = kwargs['tags']
        item['download_url'] = tree['url']
        return item
