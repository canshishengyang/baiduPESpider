# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaidusoftwaresItem(scrapy.Item):
   
    name = scrapy.Field()
    desc = scrapy.Field()
    soft_update_time = scrapy.Field()
    url = scrapy.Field()
    version = scrapy.Field()
   