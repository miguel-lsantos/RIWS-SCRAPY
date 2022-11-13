import scrapy


class ChollometroItem(scrapy.Item):
    """Define the Item fields that will be scraped.
    Field() is used to specify the meta data for the Item field, such
    as the serializer. Most of the time we don't need to specify any
    meta data for the Item field.
    """
    article = scrapy.Field()
    seller = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
