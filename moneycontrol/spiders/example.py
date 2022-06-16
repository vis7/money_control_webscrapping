import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['moneycontrol.com']
    start_urls = ['http://moneycontrol.com/']

    def parse(self, response):
        pass
