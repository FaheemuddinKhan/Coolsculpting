# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CoolsculptingItem(scrapy.Item):
    Id = scrapy.Field()
    Name = scrapy.Field()
    City = scrapy.Field()
    State = scrapy.Field()
    Email = scrapy.Field()
    Telephone = scrapy.Field()
    Website = scrapy.Field()
