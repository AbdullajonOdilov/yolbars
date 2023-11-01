from pydantic import BaseModel, Field


class CreateExpense(BaseModel):
    money: float = Field(..., ge=0)
    currency_id: int
    source: str
    source_id: int
    comment: str
    kassa_id: int


class UpdateExpense(BaseModel):
    id: int
    money: float = Field(..., ge=0)
    currency_id: int
    source: str
    source_id: int
    comment: str
    kassa_id: int

