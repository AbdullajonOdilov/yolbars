from pydantic import BaseModel, Field
from typing import Optional


class CurrenciesCreate(BaseModel):
    name: str
    money: float = Field(..., ge=0.1)


class CurrenciesUpdate(BaseModel):
    id: int
    name: str
    money: float = Field(..., ge=0.1)

