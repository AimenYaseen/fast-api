from typing import Any

from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


class Item2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.post("/items/")
def create_post(
        item: Item
) -> Item:
    return item


"""
If you declare both a return type and a response_model, 
the response_model will take priority and be used by FastAPI.
"""


@app.get(
    path="/items/",
    response_model=list[Item]
)
async def read_items() -> Any:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


# UNION RETURN TYPE

@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}


# RESPONSE MODEL EXCLUDE & INCLUDE
@app.get(
    path="/items/{item_id}",
    response_model=Item2,
    response_model_exclude_unset=True,  # exclude the default values if it is not set
    response_model_include={"name", "description"},  # only include these two fields
    response_model_exclude=["tax"], # exclude tax field
)
async def read_item(item_id: str):
    return items[item_id]
