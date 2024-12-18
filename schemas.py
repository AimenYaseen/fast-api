from typing import Literal

from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    description: str | None = None  # optional argument using new syntax
    price: float
    tax: float = 0
    is_offered: bool = True  # made it optional with default value as True


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []
