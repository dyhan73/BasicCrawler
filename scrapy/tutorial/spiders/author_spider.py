"""
author spider
"""

import scrapy

class AuthorSpider(scrapy.Spider):
    """Author Spider"""
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow linkds to author pages
        for href in response.css('.author + a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_author)

        # follow pagination links
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_author(self, response):
        """parse author"""
        def extract_with_css(query):
            """extract with css"""
            return response.css(query).extract_first().strip()

        yield {
            'name' : extract_with_css('h3.author-title::text'),
            'birthday' : extract_with_css('.author-born-date::text'),
            'bio' : extract_with_css('.author-description::text'),
        }
