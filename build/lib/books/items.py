# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags

# Utility function to remove whitespaces.
def remove_whitespaces(value):
    return value.strip()

# Utility function to clean and format img url.    
def clean_and_format_image(value):
    return value.replace("../../../..", "http://books.toscrape.com")

# Utility function to clean and format book url.   
def clean_and_format_book_url(value):
    return value.replace("../../..", "http://books.toscrape.com/catalogue")
    
   


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    book = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespaces),
        output_processor=TakeFirst()
    )

    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespaces),
        output_processor=TakeFirst()
    )
    
    image_url = scrapy.Field(
        input_processor=MapCompose(clean_and_format_image),
        output_processor=TakeFirst()
    )
    
    book_url = scrapy.Field(
        input_processor=MapCompose(clean_and_format_book_url),
        output_processor=TakeFirst()
    )
