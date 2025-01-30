from typing import Annotated

from fastapi import FastAPI, Depends, Cookie

app = FastAPI()


def query_extractor(q: str | None = None):
    return q


def query_cookie_extractor(
        q: Annotated[str, Depends(query_extractor)],
        last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
        query: Annotated[str, Depends(query_cookie_extractor)],
):
    return {
        "query_or_cookie": query,
    }
