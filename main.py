from enum import Enum
from typing import Union

from fastapi import FastAPI

from schemas import Item

app = FastAPI()


@app.get("/")
def health_check():
    return {"detail": "Working Great!"}


# -------------- PATH PARAMETERS ---------------------
@app.get("/items/{item_id}")
def read_item(
        item_id: int,  # path parameter with its type
        q: Union[str, None] = None  # optional argument
):
    return {
        "item_id": item_id,
        "q": q
    }


# ------------------- PREDEFINED VALUES ------------------
class ModelName(str, Enum):
    test = "test"
    staging = "staging"
    live = "live"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    models = {
        ModelName.test: {"model_name": ModelName.test, "message": "implement and test locally!"},
        ModelName.staging: {"model_name": ModelName.staging, "message": "deployed on a server and test it"},
        ModelName.live: {"model_name": ModelName.live, "message": "deployed to production server and make it available"
                                                                  "to users"},
    }
    return models.get(model_name)


# -------------------- PYDANTIC SCHEMAS -------------------------
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {
        "item_id": item_id,
        "item_name": item.name,
        "item_price": item.price,
        "is_offer": item.is_offer,
    }
