import scrapy

from RIWS.items import QuoteItem


class ChollometroSpider(scrapy.Spider):
    name = 'chollometro'
    allowed_domains = ['chollometro.com']
    start_urls = ['https://www.chollometro.com/ofertas']
    min_pages = 1
    max_pagex = 20

    def start_requests(self):
        for url in self.start_urls:
            for i in range(self.min_pages, self.max_pagex):
                yield scrapy.Request(url + f"?page={i}/", self.parse)

    def parse(self, response):
        # // means to search in the scope of the whole document.
        # @class in square brackets means to select by class name of
        # the HTML element.
        for quote_selector in response.xpath('//article'):
            # ./ means to search in the context of the current selector.
            # text() means to select the text of the HTML element.
            inner_div = quote_selector.xpath('./div')
            title_div = inner_div.xpath('./div[contains(@class, "threadGrid-title")]')
            value_title = title_div.xpath('./strong/a/@title').get()
            value_empresa = title_div.xpath('./span/a/span/span/text()').get()
            # Remove the special quotes.
            value_descripcion = inner_div.xpath(
                './div[contains(@class, "threadGrid-body")]/div/div/text()'
            ).get()
            quote_item = QuoteItem(author=value_title, quote=value_empresa, tags=value_descripcion)
            yield quote_item

        # if next_page_url := response.xpath(
        #         '//li[@class="next"]/a/@href'
        # ).get():
        #     # With response.follow() we can scrape the next page with
        #     # the same parse function, recursively.
        #     yield response.follow(next_page_url, self.parse)
