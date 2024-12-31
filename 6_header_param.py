from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    model_config = {
        "extra": "forbid",
    }

    host: str
    save_data: bool
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(
        headers: Annotated[CommonHeaders, Header()],  # pydantic model as headers
        user_agent: Annotated[str | None, Header()] = None,
        x_token: Annotated[list[str] | None, Header()] = None,  # receive duplicate headers as a list
):
    return {
        "User-Agent": user_agent,
        "X-Token": x_token,
        "Common_Headers": headers,
    }
