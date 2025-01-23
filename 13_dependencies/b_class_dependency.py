from typing import Annotated

from fastapi import FastAPI, Depends

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(common: Annotated[CommonQueryParams, Depends()]):
    response = {}
    if common.q:
        response.update({"q": common.q})
    items = fake_items_db[common.skip: (common.skip + common.limit)]
    response.update({"items": items})
    return response
