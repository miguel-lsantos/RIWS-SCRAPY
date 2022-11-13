import sys

import hashlib
from scrapy.utils.project import get_project_settings
import logging
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
from elasticsearch import Elasticsearch

class ElasticSearchPipeline(object):
    def __init__(self):

        self.settings = get_project_settings()

        uri = f"http://{self.settings['ELASTICSEARCH_SERVER']}:{self.settings['ELASTICSEARCH_PORT']}"
        if (self.settings['ELASTICSEARCH_USERNAME'] is None) or (self.settings['ELASTICSEARCH_USERNAME'] == ""):
            self.es = Elasticsearch(hosts=[uri])
        else:
            self.es = Elasticsearch(hosts=[uri], basic_auth=(self.settings['ELASTICSEARCH_USERNAME'],
                                                                self.settings['ELASTICSEARCH_PASSWORD']))

        properties = {
                "article": {
                    "type": "text", # formerly "string"
                    "analyzer": "standard"
                },
                "seller": {
                    "type": "text",
                    "analyzer": "standard"
                },
                "description": {
                    "type": "text",
                    "analyzer": "standard"
                },
                "categories": {
                    "type": "text",
                    "analyzer": "standard"
                }
        }

        if not self.es.indices.exists(index=self.settings["ELASTICSEARCH_INDEX"]):
            self.es.indices.create(
                index=self.settings["ELASTICSEARCH_INDEX"]
            )
        self.es.indices.put_mapping(index=self.settings["ELASTICSEARCH_INDEX"], properties=properties)

    def process_item(self, item, spider):
        if self.__get_uniq_key() is None:
            logger.log(msg="ELASTICSEARCH_UNIQ_KEY is NONE", level=logging.DEBUG)
            self.es.index(dict(item), self.settings['ELASTICSEARCH_INDEX'], self.settings['ELASTICSEARCH_TYPE'],
                          id=item['id'], op_type='create',)
        else:
            self.es.index(document=dict(item), index=self.settings['ELASTICSEARCH_INDEX'],
                          id=self._get_item_key(item))
        logger.log(msg=f"Item send to Elastic Search {self.settings['ELASTICSEARCH_INDEX']}", level=logging.DEBUG)
        return item

    def _get_item_key(self, item):
        uniq_key = self.__get_uniq_key()
        if uniq_key is None:
            return item['article']
        return hashlib.sha1(item[uniq_key][0].encode('utf-8')).hexdigest()

    def __get_uniq_key(self):
        if not self.settings['ELASTICSEARCH_UNIQ_KEY'] or self.settings['ELASTICSEARCH_UNIQ_KEY'] == "":
            return None
        return self.settings['ELASTICSEARCH_UNIQ_KEY']