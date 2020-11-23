import scrapy
from ..items import OmdbItem

class OmdbNameSpider(scrapy.Spider):
    name = 'omdb_name'
    start_urls = ['https://www.imdb.com/search/title/?title_type=tv_series&explore=title_type,genres&ref_=adv_prv']

    def parse(self, response):
        for all_item in response.css('.mode-advanced'):
            name = all_item.css('.lister-item-header a').css('::text').extract_first()

            yield {
                'name':name
             }

        next_page = response.css('.next-page').css('::attr(href)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)


'''
'https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=sci-fi&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=horror&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=romance&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=action&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=thriller&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=drama&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=mystery&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=crime&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=animation&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=adventure&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=fantasy&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=comedy,romance&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=action,comedy&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs',
                  'https://www.imdb.com/search/title/?genres=superhero&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs']
'''

