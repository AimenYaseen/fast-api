"""
it's not completed yet. Because we still have no endpoint /token to
receive username and password and return a token.
"""

from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    fullname: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fake_token_decode",
        email="example.com",
        fullname="Example",
        disabled=False,
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = get_current_user(token)
    return user


@app.get("/get_user/", tags=["User"])
async def get_user(user: Annotated[User, Depends(get_current_user)]):
    return {
        "user": user,
    }
