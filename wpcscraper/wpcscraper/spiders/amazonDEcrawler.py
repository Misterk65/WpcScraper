# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import *

import time

class AmazondespiderSpider(scrapy.Spider):

    # Class declarations

    name = 'amazonDEcrawler'
    # allowed_domains = ['amazon.de']
    page_number = 2
    urlList = []
    current_Link=""
    next_page = ""
    start_urls = [
         #'https://www.amazon.de/s?k=qi&i=electronics&rh=n%3A562066&lo=list&dc&page=350&__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1553674886&rnid=1703609031&ref=sr_pg_102'
        'https://www.amazon.de/s?k=qi&rh=n%3A562066&lo=grid&dc&__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1553672247&rnid=1703609031&ref=sr_nr_n_1'
    # Page 2 https://www.amazon.de/s/ref=sr_pg_2?fst=as%3Aon&rh=k%3Aqi%2Cn%3A562066%2Cn%3A1384526031%2Cn%3A364918031%2Cn%3A364929031%2Cn%3A1385091031&page=2&keywords=qi&ie=UTF8&qid=1553174833
    ]

    def parse(self, response):
        
        # Declarations 
        base_url = 'https://www.amazon.de'

        print('Response: ' + response.url)
        
        # Extract the product URL from the initial search page
        prod_urls = response.css('.a-text-normal::attr(href)').getall()

        #if prod_urls in None:
            #print('Entered')
            #.a-color-base.a-text-normal -link-normal
            #prod_urls = response.css('.a-text-normal::attr(href)').getall()


        # Parse through the found URLs and parse out the product relevant ones
        for url in prod_urls:
            if url.startswith('/gp/slredirect/'):
                if not url.endswith('#customerReviews'):
                    AmazondespiderSpider.urlList.append(base_url + url) # Add the base URL of the website and append the results to
                                                   # to a list.

            AmazondespiderSpider.urlList = list(dict.fromkeys(AmazondespiderSpider.urlList)) # Remove the duplicates in the list


            # Go to second...n page
            AmazondespiderSpider.next_page = response.css('.a-last a::attr(href)').get()
            AmazondespiderSpider.next_page = base_url + AmazondespiderSpider.next_page
            ##print('Link 1: ' + str(AmazondespiderSpider.next_page))
            yield response.follow(AmazondespiderSpider.next_page,
                                  callback=self.parse)  # Call the parse function until the last page is reached


        for link in AmazondespiderSpider.urlList:
            AmazondespiderSpider.current_Link = link
            yield Request(link, callback=self.parse_link)


    def parse_link(self, response):

        prod_Vendor = response.selector.xpath('//*[(@id="bylineInfo")]/text()').get()
        prod_Asin = response.selector.xpath('//li[contains(.,"ASIN:")]/text()').get()
        prod_Vendor_ID = response.selector.xpath('//li[contains(.,"Modellnummer:")]/text()').get()
        prod_at_Seller = response.selector.xpath('//li[contains(.,"Im Angebot von Amazon.de seit:")]/text()').get()
        prod_link = self.current_Link

        if prod_Asin is None:
            prod_Asin = response.css('.col2 tr:nth-child(1) .value::text').get()

        if prod_Vendor is None:
            prod_Vendor = 'Not Available'

        if prod_Vendor_ID is None:
            prod_Vendor_ID = 'Not Available'

        if prod_at_Seller is None:
            prod_at_Seller = 'Not Available'

        #print('Vendor: ' + prod_Vendor)
        #print('Vendor ID: ' + prod_Vendor_ID)
        #print('ASIN: ' + prod_Asin)
        #print('Added to Platform: ' + prod_at_Seller)
        #print('Product Link: ' + prod_link)

        yield {
            'website': 'Amazon Germany',
            'Vendor':  prod_Vendor.strip(),
            'VendorId': prod_Vendor_ID.strip(),
            'ASIN': prod_Asin.strip(),
            'AddedToPlatform':prod_at_Seller.strip(),
            'ProductLink': prod_link.strip(),
            'ScrapedOnUtc': time.time()
        }