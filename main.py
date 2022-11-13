from elasticsearch import Elasticsearch
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from scrapy.utils.project import get_project_settings

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

from RIWS.settings import ELASTICSEARCH_SERVER, ELASTICSEARCH_PORT,\
    ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD, \
    ELASTICSEARCH_INDEX


def get_category_options():
    uri = f"http://{ELASTICSEARCH_SERVER}:{ELASTICSEARCH_PORT}"
    if (ELASTICSEARCH_USERNAME is None) or (ELASTICSEARCH_USERNAME == ""):
        es = Elasticsearch(hosts=[uri])
    else:
        es = Elasticsearch(hosts=[uri], basic_auth=(ELASTICSEARCH_USERNAME,
                                                    ELASTICSEARCH_PASSWORD))

    # query_body = {
    #     "query": {
    #         "simple_query_string": {
    #             "query": query_string,
    #             "fields": ["*"]
    #         }
    #     }
    # }
    query_body = {
        "aggs": {
            "sellers": {
                "terms": {
                    "field": "seller",
                    "size": 200
                }
            }
        }
    }

    search_result = es.search(index=ELASTICSEARCH_INDEX, body=query_body)
    return [value["key"] for value in search_result.body['aggregations']['sellers']['buckets']]
def search(query_string: str, seller: str):

    uri = f"http://{ELASTICSEARCH_SERVER}:{ELASTICSEARCH_PORT}"
    if (ELASTICSEARCH_USERNAME is None) or (ELASTICSEARCH_USERNAME == ""):
        es = Elasticsearch(hosts=[uri])
    else:
        es = Elasticsearch(hosts=[uri], basic_auth=(ELASTICSEARCH_USERNAME,
                                                         ELASTICSEARCH_PASSWORD))

    # query_body = {
    #     "query": {
    #         "simple_query_string": {
    #             "query": query_string,
    #             "fields": ["*"]
    #         }
    #     }
    # }
    query_body = {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query_string,
                        "fields": ["article", "description", "categories"],
                        "analyzer": "standard",
                        "fuzziness": "AUTO",
                    }
                }
            }
        }
    }

    if seller != "Todos":
        query_body["query"]["bool"]["filter"] = {
                    "term": {
                        "seller": seller
                    }
                }

    search_result = es.search(index=ELASTICSEARCH_INDEX, body=query_body, min_score=0, explain=False, size=1000)
    print(search_result)
    print(search_result.body["hits"]["hits"])
    for hit in search_result.body["hits"]["hits"]:
        yield hit


@app.get("/")
def form_post(request: Request):
    result = "Type a query"
    options = get_category_options()
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result, "options": options})


@app.post("/")
def form_post2(request: Request, query: str = Form(...), seller: str = Form(...)):
    results = ["Hola"]
    options = get_category_options()
    try:
        for result in search(query, seller):
            results.append(result)
    except Exception as e:
        results.append(e)
    results.append("Adios")
    return templates.TemplateResponse('form.html', context={'request': request, 'results': results, "options": options})