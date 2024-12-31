from typing import Annotated

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Cookies(BaseModel):
    # It will not receive any other cookie than what is defined.
    model_config = {
        "extra": "forbid",
    }

    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


@app.get("/items/")
async def read_items(
        cookies: Annotated[Cookies, Cookie()] = None,
        ads_id: Annotated[str | None, Cookie()] = None,
):
    # It will return None because  the docs UI works with JavaScript,
    # the cookies won't be sent, and you will see an error message as
    # if you didn't write any values if it is required.
    return {
        "ads_id": ads_id,
        "cookies": cookies,
    }
