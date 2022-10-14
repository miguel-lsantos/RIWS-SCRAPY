from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

@app.get("/")
def form_post(request: Request):
    result = "Type a query"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.post("/")
def form_post(request: Request, query: list[str] = Form(...)):
    results = ["Hola"]
    results += query
    results += query
    results += query
    results.append("Adios")
    return templates.TemplateResponse('form.html', context={'request': request, 'results': results})