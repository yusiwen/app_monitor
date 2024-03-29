# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AppMonitorItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    version = scrapy.Field()
    date = scrapy.Field()
    project_url = scrapy.Field()
    release_url = scrapy.Field()
    notes = scrapy.Field()
    download_url = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    last_check_time = scrapy.Field()
    last_check_status = scrapy.Field()
    last_check_exception = scrapy.Field()
