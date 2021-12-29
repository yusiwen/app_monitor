# -*- coding: utf-8 -*-
import json
from datetime import datetime

import scrapy

from app_monitor.items import AppMonitorItem


class ChromeSpider(scrapy.Spider):
    name = 'chrome'
    allowed_domains = ['omahaproxy.appspot.com']
    start_urls = ['http://omahaproxy.appspot.com/all.json']

    def parse(self, response):
        json_dict = json.loads(response.text)
        filtered_dict = [x for x in json_dict if x['os'] == 'win64']
        versions = filtered_dict[0]['versions']
        output = [x for x in versions if x['channel'] == 'stable']
        version = '{current_version}'.format(**output[0])
        date = datetime.strptime('{current_reldate}'.format(**output[0]), '%m/%d/%y')
        datestr = date.strftime('%Y-%m-%d')

        previous_version = '{previous_version}'.format(**output[0])

        item = AppMonitorItem()
        item['name'] = 'google-chrome-browser'
        item['version'] = version
        item['date'] = datestr
        item[
            'notes'] = '<a href="https://chromium.googlesource.com/chromium/src/+log/{}..{}?pretty=fuller&n=10000">Changelog</a>'.format(
            previous_version, version)
        item['id'] = 'chrome'
        item['download_url'] = 'https://www.google.com/intl/en/chrome/browser/desktop/index.html?standalone=1'
        return item
