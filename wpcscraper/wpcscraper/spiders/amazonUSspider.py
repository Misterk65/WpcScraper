# -*- coding: utf-8 -*-
import scrapy

from scrapy import Selector


class AmazondespiderSpider(scrapy.Spider):
    name = 'amazonUSspider'
    # allowed_domains = ['amazon.de']
    page_number = 2
    start_urls = [
        # 'https://www.amazon.de/s/ref=nb_sb_noss_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=qi&rh=i%3Aaps%2Ck%3Aqi+wireless'
        'https://www.amazon.com/s?k=qi&ref=nb_sb_noss'
        # Amazon DE
        # 'https://www.amazon.de/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Aqi+wireless&page=2&keywords=qi+wireless&ie=UTF8&qid=1552828737' Amazon DE 2. page
        # 'https://www.amazon.com/s?k=qi+wireless+charger&crid=3JWK6SF4GYSTA&sprefix=qi+wirele%2Caps%2C349&ref=nb_sb_ss_i_1_9' # Amazon US
        # 'http://quotes.toscrape.com/tag/humor/'
    ]


    def parse(self, response):
        for item in response.css('.s-item-container'):
            yield {
                #'prod_brand': item.css('.a-color-secondary+ .a-color-secondary').css('::text').get(),
                #'prod_description': item.css('.s-access-title::text').get(),
                'prod_price': item.css('.a-price span::text').get(),
                #'prod_asin': item.css('.a-row .a-spacing-none').get(),
                #'prod_image': item.css('.cfMarker::attr(src)').css('::name').get()
            }