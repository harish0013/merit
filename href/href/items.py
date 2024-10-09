# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class HtmlContentItem(scrapy.Item):
    url = scrapy.Field()     # The URL of the page
    header = scrapy.Field()  # The header text (if applicable)
    body = scrapy.Field()    # The full HTML content of the page

