from pydantic import BaseModel, Field


class CreateStage(BaseModel):
    name: str
    comment: str
    kpi: float = Field(..., ge=0.1)
    measure_id: int
    category_id: int


class UpdateStage(BaseModel):
    id: int
    name: str
    comment: str
    status: bool
    number: int
    kpi: float = Field(..., ge=0.1)
    measure_id: int
    category_id: int

