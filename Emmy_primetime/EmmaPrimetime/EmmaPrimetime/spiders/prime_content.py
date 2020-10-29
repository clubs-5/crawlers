import scrapy
import time
from scrapy_splash import SplashRequest
import re



class Prime_content(scrapy.Spider):
    name = 'Prime_content'
    start_url = ['https://www.imdb.com/event/ev0000223/2020/1/?ref_=ev_eh']


    def start_requests(self):
        for url in self.start_url:
            yield SplashRequest(url=url,callback=self.parse,args={'wait':5})



    def parse(self, response):
        all_movies = response.css('.event-widgets__primary-nominees a').css('::attr(href)').extract()
        for movie in all_movies:
            link = response.urljoin(movie)

            yield scrapy.Request(url=link,callback=self.parse2)



    def parse2(self,response,url):
        rating_avg = response.css('.strong span').css('::text').extract_first()
        finalist = response.css('title::text').extract_first()
        time.sleep(3)
        yield {
               'rating_avg':rating_avg,
                'finalist':finalist
            }


