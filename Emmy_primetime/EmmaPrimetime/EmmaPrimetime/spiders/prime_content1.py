import time
from urllib.parse import urljoin

import scrapy
from scrapy_splash import SplashRequest


class Prime_content(scrapy.Spider):
    name = 'Prime_content1'
    allowed_domains = ['imdb.com']
    start_url = ['https://www.imdb.com/event/ev0000223/2020/1/?ref_=ev_eh']

    def start_requests(self):
        for url in self.start_url:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 5})

    def parse(self, response, **kwargs):
        movies = response.css('.event-widgets__primary-nominees a').css('::attr(href)').extract()
        for movie in movies:
            if 'title' in movie:
                url = response.urljoin(movie)
                yield SplashRequest(url=url, callback=self.parse_movie)

            elif 'name' in movie:
                url_2 = response.urljoin(movie)
                yield scrapy.Request(url=url_2, callback=self.parse_men)

    # about movie awarded
    def parse_movie(self, response):
        time.sleep(2)
        rating_total = response.xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/a/span/text()').get()
        rating_avg = response.xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()').get()
        moive_description = response.css('.summary_text').css('::text').extract_first()
        finalist = response.css('title::text').extract_first()
        cast = response.css('.primary_photo+ td a').css('::text').extract()
        language = response.xpath('//*[@id="titleDetails"]/div[2]/a/text()').extract_first()
        style = response.xpath('//*[@id="titleStoryLine"]/div[3]/text()').extract()
        yield {
            'rating_total':rating_total,
            'rating_avg': rating_avg,
            'finalist': finalist,
            'movie_description':moive_description.strip(),
            'cast':cast,
            'language':language,
            'style':style

        }

# for only people.
    def parse_men(self, response):
        awards_record = response.css('.split_0 .subnav_item_main:nth-child(2) .link').css(
            '::attr(href)').extract_first()
        url = response.urljoin(awards_record)
        yield scrapy.Request(url=url, callback=self.parse_award_info)


# for only people.
    def parse_award_info(self, response):
        time.sleep(2)
        finalist = response.css('.parent a').css('::text').extract_first()
        for item in response.css('#main > div:nth-child(2) > div > table'):
            years = item.css('.award_year a').css('::text').extract_first()
            winner_Nominee = item.css('b').css('::text').extract_first()
            item_award = item.css('.award_category').css('::text').extract_first()
            award_description = item.css('.award_description').css('::text').extract_first()
            yield {
                            'finalist':finalist,
                            'year':years.strip(),
                            'winner_Nominee':winner_Nominee,
                            'item_award':item_award,
                            'award_description':award_description.strip() }





