import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider

import json
from ..items import  EmmaprimetimeItem
'''
目標：爬取歷年EMMA 獎得獎人以及入圍人從1940年開始爬 -> 欄位設定：
格式為：csv 

'''
class PrimetimeSpider(scrapy.Spider):
    name = 'Primetime'
    allowed_domains = ['imdb.com']
    page_years =2019
    start_urls = ['https://www.imdb.com/event/ev0000223/2020/1/?ref_=ev_eh']



    def start_requests(self):
        for url in self.start_urls:
           yield SplashRequest(url=url,callback=self.parse,args={"wait":2})

    def parse(self, response):


            for big_title in response.css('.event-widgets__award-category'):

                years = response.css('.event-year-header__year').css('::text').extract_first()
                award_title = big_title.css('.event-widgets__award-category-name').css('::text').extract_first()
                for article in big_title.css('.event-widgets__award-nomination'):
                    finalist = article.css('.event-widgets__primary-nominees .event-widgets__nominee-name').css('::text').extract()
                    winner = article.css('.event-widgets__winner-badge').css('::text').extract_first()
                    groups = article.css('.event-widgets__secondary-nominees').css('::text').extract()



                    yield {
                        'award_title':award_title,
                        'years':years,
                        'finalist':finalist,
                        'winner':winner,
                        'groups':groups,

                          }

            next_pages = "https://m.imdb.com/event/ev0000223/"+str(PrimetimeSpider.page_years)+"/1/?ref_=ev_eh"

            if PrimetimeSpider.page_years >=1940:
                    PrimetimeSpider.page_years -=1

            yield SplashRequest(url=next_pages,callback=self.parse,args={"wait":5})



















'''
# have many repeat

    def parse(self, response):
        items= EmmaprimetimeItem()
        for article in response.css('.event-widgets__nomination-details'):

            years = response.css('.event-year-header__year').css('::text').extract_first()
            items['years'] = years
            finalist = article.css('.event-widgets__primary-nominees .event-widgets__nominee-name').css('::text').extract()
            items['finalist'] = finalist
            winner = article.css('.event-widgets__winner-badge').css('::text').extract_first()
            items['winner'] = winner
            items['groups'] =article.css('.event-widgets__secondary-nominees').css('::text').extract()

            if winner is not None:
                for title in response.css('.event-widgets__award-category-name'):
                    items['title'] = title.css('.event-widgets__award-category-name').css('::text').extract()
            yield items

        next_pages = "https://m.imdb.com/event/ev0000223/"+str(PrimetimeSpider.page_years)+"/1/?ref_=ev_eh"
        if PrimetimeSpider.page_years >=1940:
                PrimetimeSpider.page_years -=1
        yield SplashRequest(url=next_pages,callback=self.parse,args={"wait":5})


'''
#
'''
items["years"] = years
items["about_movie"] = about_movie
items["winner"] = winner
items["awards"] = awards
items["finalist_movie"] = finalist_movie '''

'''        inner_pages =response.css('div:nth-child(1) > h3 > div > div > div > a').css('::attr(href)').extract()
        for inner_page in inner_pages:
            link = response.urljoin(inner_page)
          yield SplashRequest(url=link,callback=self.inner_content,args={"wait":5})'''

