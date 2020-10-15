import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
from w3lib.html import remove_tags
from bs4 import BeautifulSoup
import json
from ..items import  EmmaprimetimeItem
'''
目標：爬取歷年EMMA 獎得獎人以及入圍人從1940年開始爬 -> 欄位設定：
格式為：csv 

'''

class PrimetimeSpider(scrapy.Spider):
    name = 'Primetime'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/event/ev0000223/2020/1/?ref_=ev_eh']
    page_year = 2019


    def start_requests(self):
        for url in self.start_urls:
           yield SplashRequest(url=url,callback=self.parse,args={"wait":2})




# have many repeat

    def parse(self, response):
        for article in response.css('.event-widgets__award-category-name+ .event-widgets__award-category-nominations .event-widgets__award-nomination'):
            data = {}

            years = response.css('.event-year-header__year').css('::text').extract()
            data['years'] = years
            data['finalist'] = article.css('.event-widgets__primary-nominees a').css("::text").extract_first()
            data['winner'] = article.css('.event-widgets__winner-badge').css('::text').extract_first()
            data['groups'] =article.css('.event-widgets__secondary-nominees').css('::text').extract()
            if data['winner'] is not None:
               for title in response.css('.event-widgets__award-category-name'):
                   data['title'] = title.css('.event-widgets__award-category-name').css('::text').extract()

            yield data
'''
        next_pages = "https://m.imdb.com/event/ev0000223/"+str(PrimetimeSpider.page_year)+"/1/?ref_=ev_eh"

        if PrimetimeSpider.page_year >=1940:
                PrimetimeSpider.page_year -=1

        yield SplashRequest(url=next_pages,callback=self.parse,args={"wait":5})
        yield response.follow(next_pages, callback=self.parse)

'''

#
'''
items["years"] = years
items["about_movie"] = about_movie
items["winner"] = winner
items["awards"] = awards
items["finalist_movie"] = finalist_movie '''
#