# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import *

import time

class AmazondespiderSpider(scrapy.Spider):

    # Class declarations

    name = 'amazonDEcrawler'
    # allowed_domains = ['amazon.de']
    page_number = 1
    urlList = []
    current_Link=""
    next_page = ""
    start_urls = [
         'https://www.amazon.de/s?k=qi&rh=n%3A562066&lo=grid&dc&__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1553672247&rnid=1703609031&ref=sr_nr_n_1'
    ]

    def parse(self, response):
        
        # Declarations 
        base_url = 'https://www.amazon.de'
        
        # Extract the product URL from the initial search page
        prod_urls = response.css('.a-text-normal::attr(href)').getall()

        # Parse through the found URLs and parse out the product relevant ones
        for url in prod_urls:
            if url.startswith('/gp/slredirect/'):
                if not url.endswith('#customerReviews'):
                    AmazondespiderSpider.urlList.append(base_url + url) # Add the base URL of the website and append the results to
                                                                        # to a list.
            else:
                AmazondespiderSpider.urlList.append(
                    base_url + url)  # Add the base URL of the website and append the results to
                                     # to a list.

            # Remove the duplicates in the list
            AmazondespiderSpider.urlList = list(dict.fromkeys(AmazondespiderSpider.urlList))

            # Go to second...n page
            AmazondespiderSpider.next_page = response.css('.a-last a::attr(href)').get()
            AmazondespiderSpider.next_page = base_url + str(AmazondespiderSpider.next_page)
            # Call the parse function until the last page is reached
            yield response.follow(AmazondespiderSpider.next_page,
                                  callback=self.parse)

        # Call the parse_link Funnction to extract data from product detail page
        for link in AmazondespiderSpider.urlList:
            AmazondespiderSpider.current_Link = link
            yield Request(link, callback=self.parse_link)


    def parse_link(self, response):

        prod_Vendor = response.selector.xpath('//*[(@id="bylineInfo")]/text()').get()
        prod_Asin = response.selector.xpath('//li[contains(.,"ASIN:")]/text()').get()
        prod_Vendor_ID = response.selector.xpath('//li[contains(.,"Modellnummer:")]/text()').get()
        prod_at_Seller = response.selector.xpath('//li[contains(.,"Im Angebot von Amazon.de seit:")]/text()').get()
        prod_link = response.url

        if prod_Asin is None:
            prod_Asin = 'Not Available'

        if prod_Vendor is None:
            prod_Vendor = 'Not Available'

        if prod_Vendor_ID is None:
            prod_Vendor_ID = 'Not Available'

        if prod_at_Seller is None:
            prod_at_Seller = 'Not Available'

        # Before writing to database extract from the product title keywords which are hold in a list.
        # Probably a good idea to read initially from a file/database to be flexible.

        yield {
            'website': 'Amazon Germany',
            'Vendor':  prod_Vendor.strip(),
            'VendorId': prod_Vendor_ID.strip(),
            'ASIN': prod_Asin.strip(),
            'AddedToPlatform':prod_at_Seller.strip(),
            'ProductLink': prod_link.strip(),
            'ScrapedOnUtc': time.time()
        }