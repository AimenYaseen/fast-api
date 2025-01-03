from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {
        "username": username,
    }


# -------------------- FORM PYDANTIC MODELS -------------------------------------

class FormData(BaseModel):
    username: str
    password: str

    model_config = {
        "extra": "forbid",
    }


@app.post("/login-model/")
async def login_model(data: Annotated[FormData, Form()]):
    return data
