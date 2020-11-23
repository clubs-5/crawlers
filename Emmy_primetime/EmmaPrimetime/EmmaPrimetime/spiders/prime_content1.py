import time
from urllib.parse import urljoin

import scrapy
from scrapy_splash import SplashRequest

class Prime_content(scrapy.Spider):
    name = 'Prime_content1'
    start_url = []
    for i in range(2020,2009, -1):
        url = f'https://www.imdb.com/event/ev0000223/{i}/1/?ref_=ev_eh'
        start_url.append(url)

    def start_requests(self):
      for url in self.start_url:
            yield SplashRequest(url=url, callback=self.parse, args={'wait':5})

    def parse(self, response, **kwargs):
        time.sleep(2)
        movies = response.css('.event-widgets__primary-nominees a').css('::attr(href)').extract()
        for movie in movies:
            if 'title' in movie:
                url = response.urljoin(movie)
                yield SplashRequest(url=url, callback=self.parse_movie)

            elif 'name' in movie:
                url_2 = response.urljoin(movie)
                yield scrapy.Request(url=url_2, callback=self.parse_men )



    # about movie awarded
    def parse_movie(self, response):
        time.sleep(2)
        rating_total = response.xpath(
            '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/a/span/text()').get()
        rating_avg = response.xpath(
            '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()').get()
        movies_description = response.css('.summary_text').css('::text').extract_first()
        finalist = response.css('title::text').extract_first()
        cast = response.css('.primary_photo+ td a').css('::text').extract()
        language = response.xpath('//*[@id="titleDetails"]/div[2]/a/text()').extract_first()
        country = response.css('.txt-block:nth-child(4) a').css('::text').get()
        film_location = response.css('.txt-block:nth-child(8) .inline+ a').css('::text').get()
        company = response.css('.subheading+ .txt-block a').css('::text').get()

        # genres have many html style so set if come to handle this pro.
        style_list = []
        style1 = response.css('.txt-block~ .canwrap .inline+ a').css('::text').get()
        if style1 is None:

            style1 = response.css('.see-more.canwrap~ .canwrap .inline+ a').css('::text').get()
            if style1 is None:
                style1 = response.css('.canwrap a').css('::text').get()

        style2 = response.css('.txt-block~ .canwrap a:nth-child(4)').css('::text').get()
        if style2 is None:
            style2 = response.css('.canwrap span+ a').css('::text').get()

        style3 = response.css('.txt-block~ .canwrap a:nth-child(6)').css('::text').get()
        if style3 is None:
            style3 = response.css('.see-more.canwrap~ .canwrap a:nth-child(6)').css('::text').get()

        style4 = response.css('.see-more.canwrap~ .canwrap a:nth-child(8)').css('::text').get()

        style5 = response.css('.see-more.canwrap~ .canwrap a:nth-child(10)').css('::text').get()

        style_list.append(style1)
        style_list.append(style2)
        style_list.append(style3)
        style_list.append(style4)
        style_list.append(style5)


        yield {
            'rating_total': rating_total,
            'rating_avg': rating_avg,
            'finalist': finalist,
            'movie_description': movies_description,
            'cast': cast,
            'language': language,
            'style': style_list,
            'country': country,
            'company': company,
            'film_location': film_location

        }

    # for only people.
    def parse_men(self, response):
        time.sleep(2)
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
                'finalist': finalist,
                'year': years.strip(),
                'winner_Nominee': winner_Nominee,
                'item_award': item_award,
                'award_description': award_description.strip()}

