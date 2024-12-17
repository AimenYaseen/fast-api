from typing import Union
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None # optional argument using new syntax
    price: float
    tax: float = 0
    is_offered: bool = True # made it optional with default value as True
