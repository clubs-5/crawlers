# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EmmaprimetimeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    years = scrapy.Field()
    finalist = scrapy.Field()
    groups = scrapy.Field()
    winner = scrapy.Field()
    title = scrapy.Field()

    pass
