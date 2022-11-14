import scrapy

from RIWS.items import ChollometroItem


class ChollometroSpider(scrapy.Spider):
    name = 'chollometro'
    allowed_domains = ['chollometro.com']
    start_urls = ['https://www.chollometro.com/categorias']
    min_pages = 1
    max_pagex = 2
    categories = []

    def start_requests(self):
        electronica_hub = "/hub/electronica"
        self.categories.append("Electrónica")
        for url in self.start_urls:
            yield scrapy.Request(url + electronica_hub, self.parse_hub)

    def parse(self, response):
        for article_selector in response.xpath('//article'):
            inner_div = article_selector.xpath('./div')
            title_div = inner_div.xpath('./div[contains(@class, "threadGrid-title")]')
            value_title = title_div.xpath('./strong/a/@title').get()
            if value_title is not None:
                value_title = value_title.split('\t')[0]
            value_empresa = title_div.xpath('./span/a/span/span/text()').get()
            if value_empresa is not None:
                value_empresa = value_empresa.split('\t')[0]
            price = title_div.xpath('./span/span[contains(@class, "overflow--wrap-off")]/span/text()').get()
            if price is not None:
                value_price = float(price[:-1].replace(',','.'))
            external_link_a = inner_div.xpath('./div[contains(@class, "threadGrid-footerMeta")]/div/span[contains(@class, "iGrid-item width--all-12 width--fromW3-auto space--l-0 space--fromW3-l-2 space--t-2 space--fromW3-t-0")]/a')
            if value_title is not None:
                if len(external_link_a) > 0:
                    if '"isThreadExpired":false' in external_link_a.attrib['data-show-app-download-message-onclick']:
                        value_link = external_link_a.xpath('./@href').get()
                    else:
                        value_link = None
                else:
                    external_link_a = inner_div.xpath( './div[contains(@class, "threadGrid-body")]/div[1]/div[contains(@class, "width--fromW2-6 space--fromW2-r-1 space--t-1 space--fromW2-t-0")]/a')
                    if len(external_link_a) > 0:
                        if '"isThreadExpired":false' in external_link_a.attrib['data-show-app-download-message-onclick']:
                            value_link = external_link_a.xpath('./@href').get()
                        else:
                            value_link = None
                    else:
                        value_link = None
            else:
                value_link = None
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
            if value_title is not None and value_link is not None:
                chollometro_item = ChollometroItem(article=value_title, seller=value_empresa,
                                                   description=value_descripcion, categories=categories_item, url=value_link, price=value_price)
                yield chollometro_item

    def parse_hub(self, response):
        categories_selectors = response.xpath('//ol[contains(@class, "iGrid bg--color-blackTranslucent bRad--fromW3-a overflow--hidden")]/li')
        for categories_selector in categories_selectors:
            category_path = categories_selector.xpath('./a/@href').get()
            category_name = categories_selector.xpath('./a/div[2]/div/span/text()').get().strip()
            if category_name not in self.categories:
                yield scrapy.Request(category_path, self.parse_subcat)
        categories_selectors2 = response.xpath('//ol[contains(@class, "flex flex--wrap")]/li')
        if not categories_selectors:
            category_path = categories_selectors2.xpath('./a/@href').get()
            yield scrapy.Request(category_path + "?page=1", self.parse)
        else:
            for categories_hub in categories_selectors2:
                category_path = categories_hub.xpath('./a/@href').get()
                category_name = categories_hub.xpath('./a/div[2]/span/text()').get().strip()
                if category_name not in self.categories:
                    yield scrapy.Request(category_path, self.parse_subcat)

    def parse_subcat(self, response):
        category_name = None
        hub = response.url.split('/')[-1]
        for categories_selector in response.xpath('//ul[contains(@class, "cept-breadcrumbsList flex flex--fromW2-wrap size--all-s text--lh-1")]/li'):
            if (categories_selector.xpath('./span[1]/a/text()').get() is not None) and (categories_selector.xpath('./span[1]/a/text()').get().strip() not in self.categories):
                category_name = categories_selector.xpath('./span[1]/a/text()').get().strip()
                hub = categories_selector.xpath('./span[1]/a/@href').get().split('/')[-1]
                break
            elif (categories_selector.xpath('./span/text()').get() is not None) and (categories_selector.xpath('./span/text()').get().strip() not in self.categories):
                category_name = categories_selector.xpath('./span/text()').get().strip()
        if category_name:
            self.categories.append(category_name)
            yield scrapy.Request(self.start_urls[0] + "/hub/" + hub, self.parse_hub)