import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from ..items import WpcscraperItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    page_number = 2 #added for pagination
    start_urls = [

        # 'http://quotes.toscrape.com/'
        'http://quotes.toscrape.com/login'
    ]

#Login

    def parse(self, response):

        open_in_browser(response) # Opens the browser to see the login status

        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response, formdata={

            'csrf_token': token,
            'username': 'Skygazer',
            'password': 'Boeing707'

        },callback= self.start_scraping)

    def start_scraping(self, response):

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

        #next_page =  response.css('li.next a::attr(href)').get()

        #if next_page is not None:
        #    yield response.follow(next_page, callback = self.start_scraping)


        # Pagination Strategy

        #next_page = 'http://quotes.toscrape.com/page/' + str(QuoteSpider.page_number) + '/'

        # if QuoteSpider.page_number < 11:
        #    yield response.follow(next_page, callback=self.start_scraping)
        #    QuoteSpider.page_number += 1