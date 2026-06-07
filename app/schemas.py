from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Decimal = Field(..., ge=0)
    quantity: int = Field(..., ge=0)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[Decimal] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, ge=0)


class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
