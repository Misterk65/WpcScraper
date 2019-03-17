# -*- coding: utf-8 -*-
import scrapy

# from wpcscraper.wpcscraper.items import amazonItems

from..items import amazonItems

class AmazondespiderSpider(scrapy.Spider):
    name = 'amazonDEspider'
    #allowed_domains = ['amazon.de']
    page_number = 2
    start_urls = [
        'https://www.amazon.de/s/ref=nb_sb_noss_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=qi+wireless&rh=i%3Aaps%2Ck%3Aqi+wireless' # Amazon DE
        # 'https://www.amazon.de/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Aqi+wireless&page=2&keywords=qi+wireless&ie=UTF8&qid=1552828737' Amazon DE 2. page
        #'https://www.amazon.com/s?k=qi+wireless+charger&crid=3JWK6SF4GYSTA&sprefix=qi+wirele%2Caps%2C349&ref=nb_sb_ss_i_1_9' # Amazon US
    ]

    def parse(self, response):

        items = amazonItems()

        prod_brand = response.css('.a-color-secondary+ .a-color-secondary').css('::text').extract()
        prod_description = response.css('.s-access-title::text').extract()
        prod_price = response.css('.s-price::text').extract()
        prod_score = response.css('.a-spacing-none > span+ .a-text-normal').css('::text').extract()
        prod_image = response.css('.cfMarker::attr(src)').extract()

        items['prod_brand'] = prod_brand
        items['prod_description'] = prod_description
        items['prod_price'] = prod_price
        items['prod_score'] = prod_score
        items['prod_image'] = prod_image

        yield items

        next_page = 'https://www.amazon.de/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Aqi+wireless&page=' + str(AmazondespiderSpider.page_number) + '&keywords=qi+wireless&ie=UTF8&qid=1552828737'
        AmazondespiderSpider.page_number += 1
        yield response.follow(next_page, callback = self.parse)