# -*- coding: utf-8 -*-
import scrapy

# from wpcscraper.wpcscraper.items import amazonItems

from ..items import amazonItems
from ..items import amazonProductItems


class AmazondespiderSpider(scrapy.Spider):
    name = 'amazonDEspider'
    # allowed_domains = ['amazon.de']
    page_number = 2
    start_urls = [
        # 'https://www.amazon.de/s/ref=nb_sb_noss_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=qi&rh=i%3Aaps%2Ck%3Aqi+wireless'
        'https://www.amazon.de/s/ref=sr_st_date-desc-rank?__mk_de_DE=%C3%85M%C3%85Z%C3%95%C3%91&keywords=qi&fst=as%3Aon&rh=k%3Aqi%2Cn%3A562066%2Cn%3A1384526031%2Cn%3A364918031%2Cn%3A364929031%2Cn%3A1385091031&qid=1553086802&sort=date-desc-rank'
        # Amazon DE
        # 'https://www.amazon.de/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Aqi+wireless&page=2&keywords=qi+wireless&ie=UTF8&qid=1552828737' Amazon DE 2. page
        # 'https://www.amazon.com/s?k=qi+wireless+charger&crid=3JWK6SF4GYSTA&sprefix=qi+wirele%2Caps%2C349&ref=nb_sb_ss_i_1_9' # Amazon US
    ]

    def parse(self, response):

        items = amazonItems()
        oItems = amazonProductItems()

        prod_brand = response.css('.a-color-secondary+ .a-color-secondary').css('::text').extract()
        prod_description = response.css('.s-access-title::text').extract()
        prod_price = response.css('.s-price::text').extract()
        prod_asin = response.css('.div::attr(data-asin)').css('::text').extract()
        prod_image = response.css('.cfMarker::attr(src)').extract()

        print(prod_brand)
        print(prod_price)


        for index in range(1, len(prod_brand)):
            if (prod_price and prod_image and prod_description and prod_brand) is not None:
                oItems['Index'] = str(index)
                # oItems['Asin'] = prod_asin[index]
                oItems['Brand'] = prod_brand[index]
                oItems['Description'] = prod_description[index]
                oItems['Price'] = prod_price[index]
                oItems['Img_Link'] = prod_image[index]
                yield oItems

                next_page = 'https://www.amazon.de/s/ref=sr_pg_2?fst=as%3Aon&rh=k%3Aqi%2Cn%3A562066%2Cn%3A1384526031%2Cn%3A364918031%2Cn%3A364929031%2Cn%3A1385091031&' + str(
                    AmazondespiderSpider.page_number) + 'page=2&sort=date-desc-rank&keywords=qi&ie=UTF8&qid=1553086812'
                AmazondespiderSpider.page_number += 1
                yield response.follow(next_page, callback=self.parse)
            else:
                print("Error in scraping")




"""
        #items['prod_asin'] = prod_asin
        items['prod_brand'] = prod_brand
        items['prod_description'] = prod_description
        items['prod_price'] = prod_price
        items['prod_image'] = prod_image


        
        print('#####Length' + str(len(prod_brand)))

        yield items

        if prod_price is not None:
            for index in range(len(prod_brand)):

                print(str(index))
                #oItems['Asin'] = prod_asin[index]
                oItems['Brand'] = prod_brand[index]
                oItems['Description'] = prod_description[index]
                oItems['Price'] = prod_price[index]
                oItems['Img_Link'] = prod_image[index]
                yield oItems
        else:
            print("Error in scraping")
"""


