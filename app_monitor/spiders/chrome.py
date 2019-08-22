# -*- coding: utf-8 -*-
import scrapy
import json

from app_monitor.items import AppMonitorItem

class ChromeSpider(scrapy.Spider):
    name = 'chrome'
    allowed_domains = ['omahaproxy.appspot.com']
    start_urls = ['http://omahaproxy.appspot.com/all.json']

    def parse(self, response):
        json_dict = json.loads(response.body_as_unicode())
        filtered_dict = [x for x in json_dict if x['os']=='win64']
        print(json.dumps(filtered_dict))
        versions = filtered_dict[0]['versions']
        output = [x for x in versions if x['channel']=='stable']
        print(json.dumps(output))
        version = '{current_version}'.format(**output[0])
        print(version)
        date = '{current_reldate}'.format(**output[0])
        print(date)

        item = AppMonitorItem()
        item['name'] = 'google-chrome-browser'
        item['version'] = version
        item['date'] = date
        item['notes'] = ''
        item['id'] = 'chrome'
        item['download_url'] = 'https://www.google.com/intl/en/chrome/browser/desktop/index.html?standalone=1'
        return item

