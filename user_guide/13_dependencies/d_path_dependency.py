"""
It will be used when you don't want any return value from
dependency
"""

from typing import Annotated

from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-token":
        raise HTTPException(status_code=400, detail="X-Token Header Invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-key":
        raise HTTPException(status_code=400, detail="X-Key Header Invalid")


@app.get("/items/", dependencies=[Depends(verify_key), Depends(verify_token)])
async def read_items():
    return [
        {
            "item": "Foo",
        },
        {
            "item": "Bar",
        },
    ]
