import time
from urllib.parse import urljoin

import scrapy
from scrapy_splash import SplashRequest

class Prime_content(scrapy.Spider):
    name = 'Prime_actor'
    start_url = []
    for i in range(1989,1947, -1):
        url = f'https://www.imdb.com/event/ev0000223/{i}/1/?ref_=ev_eh'
        start_url.append(url)

    def start_requests(self):
      for url in self.start_url:
          yield SplashRequest(url=url,
                              callback=self.parse,
                              args={'wait': 0.5, 'viewport': '1024x2480', 'timeout': 90, 'images': 0,
                                    'resource_timeout': 10},
                              )

    def parse(self, response, **kwargs):
        movies = response.css('.event-widgets__primary-nominees a').css('::attr(href)').extract()
        for movie in movies:

            if 'name' in movie:
                url_2 = response.urljoin(movie)
                yield scrapy.Request(url=url_2, callback=self.parse_men )

    # for only people.
    def parse_men(self, response):
        awards_record = response.css('.split_0 .subnav_item_main:nth-child(2) .link').css(
            '::attr(href)').extract_first()
        url = response.urljoin(awards_record)
        yield scrapy.Request(url=url, callback=self.parse_award_info)

    # for only people.
    def parse_award_info(self, response):
        finalist = response.css('.parent a').css('::text').extract_first()
        for item in response.css('#main > div:nth-child(2) > div > table'):
            years = item.css('.award_year a').css('::text').extract_first()
            winner_Nominee = item.css('b').css('::text').extract_first()
            item_award = item.css('.award_category').css('::text').extract_first()
            award_description = item.css('.award_description').css('::text').extract_first()
            yield {
                'finalist': finalist,
                'year': years.strip(),
                'winner_Nominee': winner_Nominee,
                'item_award': item_award,
                'award_description': award_description.strip()}