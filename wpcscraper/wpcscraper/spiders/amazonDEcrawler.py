# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import *
from scrapy import selector

import json
import os

class AmazondespiderSpider(scrapy.Spider):

    # Class declarations

    name = 'amazonDEcrawler'
    # allowed_domains = ['amazon.de']
    page_number = 2
    urlList = []
    start_urls = [
        'https://www.amazon.de/s/ref=nb_sb_noss?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=qi&rh=i%3Aaps%2Ck%3Aqi'
    # Page 2 https://www.amazon.de/s/ref=sr_pg_2?fst=as%3Aon&rh=k%3Aqi%2Cn%3A562066%2Cn%3A1384526031%2Cn%3A364918031%2Cn%3A364929031%2Cn%3A1385091031&page=2&keywords=qi&ie=UTF8&qid=1553174833
    ]

    def parse(self, response):
        
        # Declarations 
        base_url = 'https://www.amazon.de'

        
        # Extract the product URL from the initial search page
        prod_urls = response.css('.a-link-normal::attr(href)').getall()
        
        # Parse through the found URLs and parse out the product relevant ones
        for url in prod_urls:
            if url.startswith('/gp/slredirect/'):
                if not url.endswith('#customerReviews'):
                    AmazondespiderSpider.urlList.append(base_url + url) # Add the base URL of the website and append the results to
                                                   # to a list.

            AmazondespiderSpider.urlList = list(dict.fromkeys(AmazondespiderSpider.urlList)) # Remove the duplicates in the list

        for link in AmazondespiderSpider.urlList:
            yield Request(link, callback=self.parse_link)


    def parse_link(self, response):

        prod_Asin = response.selector.xpath('//*[(@id = "detail_bullets_id")]//b[text()[contains(.,"ASIN:")]/li/text()]').get()

        if prod_Asin is None:
            prod_Asin = response.css('.col2 tr:nth-child(1) .value::text').get()

        print(prod_Asin)