"""
Fastapi also provides dataclasses besides pydantic
it is actually achieved in the same way underneath, using Pydantic.
The dataclass will be automatically converted to a Pydantic dataclass.
"""

from dataclasses import dataclass, field
from typing import Union, List

from fastapi import FastAPI

app = FastAPI()


@dataclass
class Item:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    description: Union[str, None] = None
    tax: Union[float, None] = None
