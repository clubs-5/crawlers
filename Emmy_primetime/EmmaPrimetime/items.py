# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EmmaprimetimeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    years = scrapy.Field()
    winner = scrapy.Field()
    awards = scrapy.Field()
    finalist_movie = scrapy.Field()
    about_movie = scrapy.Field()

    pass
