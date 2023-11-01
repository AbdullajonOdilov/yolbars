from pydantic import BaseModel, Field


class CreateIncome(BaseModel):
    money: float = Field(..., ge=0)
    currency_id: int
    source: str
    source_id: int
    comment: str
    kassa_id: int