from pydantic import BaseModel, Field
from typing import Optional


class Category_detailsCreate(BaseModel):
    name: str
    quantity: float = Field(..., ge=0.1)
    measure_id: int
    category_id: int
    stage_id: int
    comment: Optional[str] = ''


class Category_detailsUpdate(BaseModel):
    id: int
    name: str
    quantity: float = Field(..., ge=0.1)
    measure_id: int
    category_id: int
    stage_id: int
    comment: Optional[str] = ''
    status: bool

