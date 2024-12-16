from typing import Union

from fastapi import FastAPI

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
