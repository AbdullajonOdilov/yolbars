from pydantic import BaseModel, Field


class CreateOrder_done_products(BaseModel):
    barcode_id: int
    worker_id: int
    quantity: float = Field(..., ge=0)


class UpdateOrder_done_products(BaseModel):
    id: int
    worker_id: int
    quantity: float = Field(..., ge=0)
    kpi_money: float = Field(..., ge=0)

