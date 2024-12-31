from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(
        user_agent: Annotated[str | None, Header()] = None,
        x_token: Annotated[list[str] | None, Header()] = None, # receive duplicate headers as a list
):
    return {
        "User-Agent": user_agent,
        "X-Token": x_token,
    }
