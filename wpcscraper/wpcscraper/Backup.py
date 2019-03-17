import scrapy

from ..items import WpcscraperItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    page_number = 2 #added for pagination
    start_urls = [

        # 'http://quotes.toscrape.com/'
        'http://quotes.toscrape.com/page/1'
    ]

    def parse(self, response):

        items = WpcscraperItem()

        all_div_quotes = response.css('div.quote').extract()

        for quotes in all_div_quotes:
            title = response.css('span.text::text').extract()
            author = response.css('.author::text').extract()
            tag = response.css('.tag::text').extract()

        items['title'] = title
        items['author'] = author
        items['tag'] = tag

        yield items

# Fpllowing Link Strategy

        # next_page =  response.css('li.next a::attr(href)').get()

        # if next_page is not None:
            # yield response.follow(next_page, callback = self.parse)

# Pagination Strategy

        next_page = 'http://quotes.toscrape.com/page/' + str(QuoteSpider.page_number) + '/'

        if QuoteSpider.page_number < 11:
            yield response.follow(next_page, callback=self.parse)
            QuoteSpider.page_number += 1

#Login using Scrapy

