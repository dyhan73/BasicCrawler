# coding: utf-8

import scrapy

class Naver01Spider(scrapy.Spider):
    name = 'naver01'


    def start_requests(self):
        url = 'http://finance.naver.com'
        yield scrapy.Request(url, self.parse)


    def parse(self, response):
        els = response.css('.num_quot')
        stock_index = els.css('.num::text').extract()
        inc_index = els.css('.num2::text').extract()
        inc_pct = els.css('.num3::text').extract()
        direct = els.css('.blind::text').extract()
        direct.pop(5)
        direct.pop(3)
        direct.pop(1)
        title = ['코스피', '코스닥', '코스피200']
        for i in range(3):
            print("%s : %s, %s%s, %s%s" % (title[i], stock_index[i], direct[i], inc_index[i], direct[i], inc_pct[i]))
