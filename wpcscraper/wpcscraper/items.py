# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WpcscraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()


class amazonItems(scrapy.Item):
    prod_brand = scrapy.Field()
    prod_description = scrapy.Field()
    prod_price = scrapy.Field()
    # prod_asin = scrapy.Field()
    prod_image = scrapy.Field()


class amazonProductItems(scrapy.Item):
    Index = scrapy.Field()
    # Asin = scrapy.Field()
    Brand = scrapy.Field()
    Description = scrapy.Field()
    Price = scrapy.Field()
    Img_Link = scrapy.Field()

class amazonDEcrawler(scrapy.Item):
    prod_url_de = scrapy.Field()
