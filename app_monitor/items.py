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
    notes = scrapy.Field()

