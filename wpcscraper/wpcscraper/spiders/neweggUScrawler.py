# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import *

import time

class NeweggUSCrawler(scrapy.Spider):

    # Class declarations
    name = 'neweggUScrawler'
    # allowed_domains = ['amazon.de']
    page_number = 0
    urlList = []
    current_Link = ""
    next_page = 2

    start_urls = [
         'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=qi&N=-1&isNodeId=1'
        # https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=-1&IsNodeId=1&Description=qi&bop=And&Page=2&PageSize=36&order=BESTMATCH
    ]

    def parse(self, response):
        
        # Declarations 
        #base_url = 'https://www.newegg.com'

        pagination = response.css('.list-tool-pagination-text strong::text').get()
        pagination = str(pagination).split('/')

        NeweggUSCrawler.page_number = int(pagination[1])
        # print(NeweggUSCrawler.page_number)

        # Extract the product URL from the initial search page
        prod_urls = response.css('.item-title::attr(href)').getall()

        # Parse through the found URLs and parse out the product relevant ones
        for url in prod_urls:
            NeweggUSCrawler.urlList.append(url) # Add the base URL of the website and append the results to

            # Remove the duplicates in the list
            NeweggUSCrawler.urlList = list(dict.fromkeys(NeweggUSCrawler.urlList))

            print(NeweggUSCrawler.urlList)
            # Go to second...n page
            for NeweggUSCrawler.next_page in range(2, NeweggUSCrawler.page_number):
                next_url = 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=-1&IsNodeId=1&Description=qi&bop=And&Page='  + \
                           str(NeweggUSCrawler.next_page) + '&PageSize=36&order=BESTMATCH'
                NeweggUSCrawler.next_page += 1
            # Call the parse function until the last page is reached
                yield response.follow(next_url,
                                  callback=self.parse)

        # Call the parse_link Funnction to extract data from product detail page
        for link in NeweggUSCrawler.urlList:
            NeweggUSCrawler.current_Link = link
            yield Request(link, callback=self.parse_link)


    def parse_link(self, response):

        prod_Vendor = response.selector.xpath('//*[@id="Specs"]/fieldset[1]/dl[1]/dd/text').get()
        prod_NeweggID = response.selector.xpath('//*[@id="baBreadcrumbTop"]/li[6]/em/text()').get()
        prod_Vendor_ID = response.selector.xpath('//*[@id="Specs"]/fieldset[1]/dl[3]/dd/text()').get()
        prod_Seller = response.selector.xpath('//*[@id="synopsis"]/div[4]/div/div[7]/div/p[2]/a[1]/text()').get()
        prod_link = response.url

        if prod_NeweggID is None:
            prod_NeweggID = 'Not Available'

        if prod_Vendor is None:
            prod_Vendor = 'Not Available'

        if prod_Vendor_ID is None:
            prod_Vendor_ID = 'Not Available'

        if prod_Seller is None:
            prod_Seller = 'Not Available'

        # Before writing to database extract from the product title keywords which are hold in a list.
        # Probably a good idea to read initially from a file/database to be flexible.

        yield {
            'website': 'Newegg.com USA',
            'Vendor':  prod_Vendor.strip(),
            'VendorId': prod_Vendor_ID.strip(),
            'NeweggId': prod_NeweggID.strip(),
            'SoldBy':prod_Seller.strip(),
            'ProductLink': prod_link.strip(),
            'ScrapedOnUtc': time.time()
        }