# -*- coding: utf-8 -*-
import scrapy
import datetime

from ..items import amazonDEcrawler



class Amazondespidercrawler(scrapy.Spider):
    name = 'amazonDEcrawler'
    # allowed_domains = ['amazon.de']
    page_number = 2
    start_urls = [
        'https://www.amazon.de/s/ref=nb_sb_noss?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=qi&rh=i%3Aaps%2Ck%3Aqi'
    # Page 2 https://www.amazon.de/s/ref=sr_pg_2?fst=as%3Aon&rh=k%3Aqi%2Cn%3A562066%2Cn%3A1384526031%2Cn%3A364918031%2Cn%3A364929031%2Cn%3A1385091031&page=2&keywords=qi&ie=UTF8&qid=1553174833
    ]

    def parse(self, response):
        
        # Declarations 

        url_items = amazonDEcrawler
        base_url = 'https://www.amazon.de'
        urlList = []
        
        # Extract the product URL from the initial search page
        prod_urls = response.css('.a-link-normal::attr(href)').getall()
        
        # Parse through the found URLs and parse out the product relevant ones
        for url in prod_urls:
            if url.startswith('/gp/slredirect/'):
                urlList.append(base_url + url) # Add the base URL of the website and append the results to
                                               # to a list.
        urlList = list(dict.fromkeys(urlList)) # Remove the duplicates in the list
        print(urlList) # Print the list -> This has to be removed in the released version
        
        # Write to database -> Not needed in the Release at this point.
        for links in urlList: 
            yield {

                "product_link": links,
                "timestamp": datetime.datetime.now()
            }
            
            # Go to second...n page 
            next_page = 'Page 2 https://www.amazon.de/s/ref=sr_pg_2?fst=as%3Aon&rh=k%3Aqi%2Cn%3A562066%2Cn' \
                        '%3A1384526031%2Cn%3A364918031%2Cn%3A364929031%2Cn%3A1385091031&page=' + str(
                AmazondespiderSpider.page_number) + '&keywords=qi&ie=UTF8&qid=1553174833 '
            AmazondespiderSpider.page_number += 1 # Increment the page 
            yield response.follow(next_page, callback=self.parse) # Call the parse function until the last page is reached


        """
        document.querySelector('#result_0 > div > div:nth-child(4) > div.a-row.a-spacing-none.sx-line-clamp-4 > a')
        prod_brand = response.css('.a-color-secondary+ .a-color-secondary').css('::text').extract()
        prod_description = response.css('.s-access-title::text').extract()
        prod_price = response.css('.s-price::text').extract()
        prod_asin = response.css('.div::attr(data-asin)').css('::text').extract()
        prod_image = response.css('.cfMarker::attr(src)').extract()



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


