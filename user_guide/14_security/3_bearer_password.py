"""
OAuth2 specifies that when using the "password flow"
(that we are using) the client/user must send a username
and password fields as form data.
Name should be username and password. You can have changed names in database and frontend.
Also, it should be sent as Form Data no Json will be accepted.

Besides username & password, we also have a scope which specifies permissions.
Like, users:read or users:write. For OAuth2 its just strings, you can also send url.
Its implementation specific.
"""

from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": True,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": False,
    },
}


# ------------------------------------ PYDANTIC -------------------------------------
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


# ------------------------------------ UTILITIES -----------------------------------
def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(db, username: str):
    if not username in db:
        return
    user_dict = db[username]
    return UserInDB(**user_dict)


def decode_fake_token(token):
    # This doesn't provide any security at all
    return get_user(fake_users_db, token)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_fake_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# _____________________________________ ENDPOINTS _____________________________________

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Does Not Exist!",
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if hashed_password != user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Password!",
        )
    return {
        "access_token": user.username,
        "token_type": "bearer",
    }


@app.get("/get_user/")
async def get_user_details(
        user: Annotated[User, Depends(get_current_active_user)]
):
    return {
        "user": user
    }
