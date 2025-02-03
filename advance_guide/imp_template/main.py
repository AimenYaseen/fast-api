from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="advance_guide/imp_template/static"), name="static")

templates = Jinja2Templates(directory="advance_guide/imp_template/templates")


@app.get("/items/{_id}", response_class=HTMLResponse)
async def read_item(request: Request, _id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": _id}
    )
