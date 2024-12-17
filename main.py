from enum import Enum

from fastapi import FastAPI

from schemas import Item

app = FastAPI()


@app.get("/")
def health_check():
    return {"detail": "Working Great!"}


# -------------- PATH & Query PARAMETERS ---------------------
@app.get("/items/{item_id}")
def read_item(
        item_id: int,  # path parameter with its type
        needy: bool,  # required query parameter
        q: str | None = None,  # optional query Parameter
        limit: int = 1,  # query parameter with default value
):
    return {
        "item_id": item_id,
        "q": q,
        "needy": needy,
        "limit": limit,
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
@app.post("/items/")
def create_item(item: Item):
    """
    Item Pydantic schema as Request Body

    :param item:
    :return: Item with price_with_tax is is_offered
    """
    item_dict = item.model_dump()  # item.dict() => dict is going to be deprecated
    if item.is_offered:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, q: str | None = None):
    """
    Request Body with Path & Query Parameters

    :param item_id:
    :param item:
    :param q:
    :return: Item with q (query parameter)
    """
    result = {
        "item_id": item_id,
        **item.model_dump(),
    }
    if q:
        result.update({"q": q})
    return result
