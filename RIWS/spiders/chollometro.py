import scrapy

from RIWS.items import QuoteItem


class ChollometroSpider(scrapy.Spider):
    name = 'chollometro'
    allowed_domains = ['chollometro.com']
    start_urls = ['https://www.chollometro.com/categorias']
    min_pages = 1
    max_pagex = 2
    categories = []

    def start_requests(self):
        for url in self.start_urls:
            for i in range(self.min_pages, self.max_pagex):
                yield scrapy.Request(url, self.parse_cat)

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
            if value_title is not None:
                value_title = value_title.split('\t')
            value_empresa = title_div.xpath('./span/a/span/span/text()').get()
            if value_empresa is not None:
                value_empresa = value_empresa.split('\t')
            value_link = title_div.xpath('./strong/a/@href').get()
            # Remove the special quotes.
            value_descripcion = inner_div.xpath(
                './div[contains(@class, "threadGrid-body")]/div/div/text()'
            ).get()
            categories_item = []
            for categories_selector in response.xpath(
                    '//ul[contains(@class, "cept-breadcrumbsList flex flex--fromW2-wrap size--all-s text--lh-1")]/li'):
                if categories_selector.xpath('./span[1]/a/text()').get() is not None:
                    categories_item.append(categories_selector.xpath('./span[1]/a/text()').get().strip())
                elif len(categories_selector.xpath('./span').getall()) == 1:
                    categories_item.append(categories_selector.xpath('./span/text()').get().strip())
            quote_item = QuoteItem(author=value_title, quote=value_empresa, tags=value_descripcion, categories = categories_item)
            yield quote_item

    def parse_cat(self, response):
        for quote_selector in response.xpath('//div[contains(@class, "page2-center page2-space--h-r")]/div'):
            category = quote_selector.xpath('./h3/text()').get().strip()
            self.categories.append(category)
            hub = quote_selector.xpath('./ol/li[8]/a/@href').get().split('/')[-1]
            if hub == "electronica":
                yield scrapy.Request(self.start_urls[0] + "/hub/" + hub, self.parse_hub)
            self.categories.remove(category)

    def parse_hub(self, response):
        categories_selectors = response.xpath('//ol[contains(@class, "iGrid bg--color-blackTranslucent bRad--fromW3-a overflow--hidden")]/li')
        for categories_selector in categories_selectors:
            category_path = categories_selector.xpath('./a/@href').get()
            category_name = categories_selector.xpath('./a/div[2]/div/span/text()').get().strip()
            if category_name not in self.categories:
                self.categories.append(category_name)
                if scrapy.Request(category_path, self.parse_subcat):
                    hub = category_path.split('/')[-1]
                    yield scrapy.Request(self.start_urls[0] + "/hub/" + hub, self.parse_hub)
                self.categories.remove(category_name)
        categories_selectors2 = response.xpath('//ol[contains(@class, "flex flex--wrap")]/li')
        if not categories_selectors:
            category_path = categories_selectors2.xpath('./a/@href').get()
            for i in range(self.min_pages, self.max_pagex):
                yield scrapy.Request(category_path + "?page=" + str(i), self.parse)
        else:
            for categories_hub in categories_selectors2:
                category_path = categories_hub.xpath('./a/@href').get()
                category_name = categories_hub.xpath('./a/div[2]/span/text()').get().strip()
                if category_name not in self.categories:
                    self.categories.append(category_name)
                    if scrapy.Request(category_path, self.parse_subcat):
                        hub = category_path.split('/')[-1]
                        yield scrapy.Request(self.start_urls[0] + "/hub/" + hub, self.parse_hub)
                    self.categories.remove(category_name)

    def parse_subcat(self, response):
        for categories_selector in response.xpath('//ul[contains(@class, "cept-breadcrumbsList flex flex--fromW2-wrap size--all-s text--lh-1")]/li'):
            if (categories_selector.xpath('./span[1]/a/text()').get() is not None) and (categories_selector.xpath('./span[1]/a/text()').get().split() not in self.categories):
                return False
        return True

