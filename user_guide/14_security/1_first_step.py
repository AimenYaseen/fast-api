from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# callable that's why used in Depends
# Bearer Token Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# it returns 401 if it is unable to find Bearer and token
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
