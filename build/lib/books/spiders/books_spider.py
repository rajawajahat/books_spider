import scrapy
from books.items import BooksItem
from scrapy.loader import ItemLoader


class BooksSpiderSpider(scrapy.Spider):
    name = 'books_spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        
        # Exctracting all categories urls from home page.
        categories = response.css('div.side_categories a ::attr(href)')[1:].extract()
        
        for category in categories:
            yield scrapy.Request(response.urljoin(category), callback=self.category_parse)
            
            
        
    def category_parse(self, response):
        
        # Extracting data of each book from the page.
        for book in response.xpath("//section/div/ol[@class='row']/li"):
            loader = ItemLoader(item=BooksItem(), selector=book)
            loader.add_xpath('book', ".//article[@class='product_pod']/h3/a/@title")
            loader.add_xpath('price', ".//article[@class='product_pod']/div[@class='product_price']/p[""@class='price_color']/text()")
            loader.add_xpath('image_url', ".//div[@class='image_container']//img//@src")
            loader.add_xpath('book_url', ".//div[@class='image_container']//a//@href")
                        
            yield loader.load_item()
            
        # Navigating to next page if it exists.
        next_page = response.xpath("//section/div/div//ul[@class='pager']/li[@class='next']/a/@href").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.category_parse)
