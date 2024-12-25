from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


# --------------- SCHEMAS ---------------------
class Image(BaseModel):
    name: str
    url: HttpUrl


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None


# deeply nested model
class Offer(BaseModel):
    name: str
    description: str
    price: float
    items: list[Item]


"""
We can also declare body as a list of list of schema in function arguments
Just like lists, we can also declare dict. For example
weights: dict[int, float]
"""


@app.post("/offers/")
async def create_offer(offer: Offer, images: list[Image] = []):
    results = {"offer": offer, "extar_images": images}
    return results


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
