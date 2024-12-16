from typing import Union

from fastapi import FastAPI

from schemas import Item

app = FastAPI()


@app.get("/")
def health_check():
    return {"detail": "Working Great!"}


@app.get("/items/{item_id}")
def read_item(
        item_id: int,
        q: Union[str, None] = None  # optional argument
):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item_name": item.name}
