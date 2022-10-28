from elasticsearch import Elasticsearch
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from scrapy.utils.project import get_project_settings

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

from RIWS.settings import ELASTICSEARCH_SERVER, ELASTICSEARCH_PORT,\
    ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD, \
    ELASTICSEARCH_INDEX
def search(query_string: str):

    uri = f"http://{ELASTICSEARCH_SERVER}:{ELASTICSEARCH_PORT}"
    if (ELASTICSEARCH_USERNAME is None) or (ELASTICSEARCH_USERNAME == ""):
        es = Elasticsearch(hosts=[uri])
    else:
        es = Elasticsearch(hosts=[uri], basic_auth=(ELASTICSEARCH_USERNAME,
                                                         ELASTICSEARCH_PASSWORD))

    query_body = {
        "query": {
            "simple_query_string": {
                "query": query_string,
                "fields": ["*"]
            }
        }
}
    search_result = es.search(index=ELASTICSEARCH_INDEX, body=query_body)
    print(search_result.body["hits"]["hits"])
    for hit in search_result.body["hits"]["hits"]:
        yield hit


@app.get("/")
def form_post(request: Request):
    result = "Type a query"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.post("/")
def form_post(request: Request, query: str = Form(...)):
    results = ["Hola"]
    try:
        for result in search(query):
            results.append(result)
    except Exception as e:
        results.append(e)
    results.append("Adios")
    return templates.TemplateResponse('form.html', context={'request': request, 'results': results})