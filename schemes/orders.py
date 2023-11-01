from datetime import date

from pydantic import BaseModel, Field


class CreateOrder(BaseModel):
    client_id: int
    category_id: int
    currency_id: int
    price: float = Field(..., ge=0.1)
    quantity: float = Field(..., ge=0.1)
    production_quantity: float = Field(..., ge=0.1)
    delivery_date: date


class UpdateOrder(BaseModel):
    id: int
    client_id: int
    category_id: int
    currency_id: int
    price: float = Field(..., ge=0.1)
    quantity: float = Field(..., ge=0.1)
    production_quantity: float = Field(..., ge=0.1)
    delivery_date: date


    