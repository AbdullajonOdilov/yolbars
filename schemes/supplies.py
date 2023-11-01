from pydantic import BaseModel, Field
from typing import Optional, List


class SuppliesCreate(BaseModel):
    category_detail_id: int
    quantity: float = Field(..., ge=0.1)
    price: float = Field(..., ge=0.1)
    supplier_id: int
    currency_id: int


class SuppliesUpdate(BaseModel):
    id: int
    category_detail_id: int
    quantity: float = Field(..., ge=0.1)
    price: float = Field(..., ge=0.1)
    supplier_id: int
    currency_id: int


class SuppliesConfirm(BaseModel):
    id: int