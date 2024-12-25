from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# --------------- SCHEMAS ---------------------
class Image(BaseModel):
    name: str
    url: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None

"""
EXAMPLE
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
"""
@app.put("/items/{item_id}")
async def update_item(
        item_id: int,
        item: Item
):
    return {
        "item_id": item_id,
        "item": item,
    }
