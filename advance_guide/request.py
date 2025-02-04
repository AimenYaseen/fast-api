"""
Use the request object directly instead of using pydantic
But it has a side effect as it will not validate the upcoming data
"""

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/items/{item_id}")
def read_root(item_id: int, request: Request):
    client_host = request.client.host
    return {
        "client_host": client_host,
        "item_id": item_id,
    }
