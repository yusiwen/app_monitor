# -*- coding: utf-8 -*-
from datetime import datetime

import lxml.html
import scrapy

from app_monitor.items import AppMonitorItem


class CalibreSpider(scrapy.Spider):
    name = 'calibre'
    allowed_domains = ['calibre-ebook.com']
    start_urls = ['https://calibre-ebook.com/whats-new']

    def _check_version(self, ver):
        if len(ver.split('.')) == 2:
            ver = ver + '.0'
        return ver

    def parse(self, response, **kwargs):
        tmp = response.xpath('//div[@id="release-pane"]/div').extract_first()
        doc = lxml.html.fromstring(tmp)
        tmp = doc.xpath('//h2/text()')[0]
        version = tmp.split()[1]
        date = tmp.split('[')[1]
        date = date.replace(']', '')
        dateobj = datetime.strptime(date, '%d %b, %Y')
        datestr = dateobj.strftime('%Y-%m-%d')

        item = AppMonitorItem()
        item['name'] = 'Calibre'
        item['version'] = version

        item['date'] = datestr

        notes = ''
        notes = notes.join(response.xpath(
            '(//div[@id="content"]//h2)[1]/following-sibling::ul').extract())
        item['notes'] = notes
        item['id'] = 'calibre'
        item['category'] = 'tool'

        down_urls = []
        ver = self._check_version(version)
        base_url = 'https://download.calibre-ebook.com/'
        down_urls.append(base_url + ver +
                         '/calibre-portable-installer-' + ver + '.exe')
        down_urls.append(base_url + ver + '/calibre-' + ver + '.dmg')
        down_urls.append(base_url + ver + '/calibre-' + ver + '-x86_64.txz')

        item['download_url'] = down_urls
        return item
