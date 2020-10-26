import scrapy
import time
from scrapy_splash import SplashRequest
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule



class Prime_content(scrapy.Spider):
    name = 'Prime_content1'
    allowed_domains = ['imdb.com']
    start_url = ['https://www.imdb.com/event/ev0000223/2020/1/?ref_=ev_eh']


    def start_requests(self):
        for url in self.start_url:
            yield SplashRequest(url=url,callback=self.parse,args={'wait':5})


    def parse(self, response):
        movies = response.css('.event-widgets__primary-nominees a').css('::attr(href)').extract()
        for movie in movies:
            if 'title'  in movie:
                url = response.urljoin(movie)
                yield scrapy.Request(url=url,callback=self.parse_movie)

            elif 'name' in movie:
                url_2 = response.urljoin(movie)
                yield scrapy.Request(url=url_2,callback=self.parse_men)






    def parse_movie(self,response):
        rating_avg = response.css('.strong span').css('::text').extract_first()
        finalist = response.css('title::text').extract_first()
        time.sleep(3)
        yield {
                'rating_avg':rating_avg,
                 'finalist':finalist
             }


    def parse_men(self,response):
        awards_record = response.css('.split_0 .subnav_item_main:nth-child(2) .link').css('::attr(href)').extract()
        yield {'url':awards_record}