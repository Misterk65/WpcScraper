# -*- coding: utf-8 -*-
import scrapy

from scrapy import Selector


class AmazondespiderSpider(scrapy.Spider):
    name = 'amazonDEspider'
    # allowed_domains = ['amazon.de']
    page_number = 2
    start_urls = [
        'https://www.amazon.de/s/ref=nb_sb_noss?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=qi&rh=i%3Aaps%2Ck%3Aqi'
        # Page 2 https://www.amazon.de/s/ref=sr_pg_2?fst=as%3Aon&rh=k%3Aqi%2Cn%3A562066%2Cn%3A1384526031%2Cn%3A364918031%2Cn%3A364929031%2Cn%3A1385091031&page=2&keywords=qi&ie=UTF8&qid=1553174833
    ]


    def parse(self, response):
        for item in response.css('.s-item-container'):
            yield {
                'website': 'Amazon Germany',
                'prod_brand': item.css('.a-color-secondary+ .a-color-secondary').css('::text').get(),
                'prod_description': item.css('.s-access-title::text').get(),
                'prod_price': item.css('.s-price::text').get(),
                'prod_asin': item.css('.result_0+ .div+ div.a-row.a-spacing-none+ .span').css('::name').get(),
                'prod_image': item.css('.cfMarker::attr(src)').get()
            }