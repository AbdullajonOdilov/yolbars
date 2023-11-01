from pydantic import BaseModel, Field


class CreateOrder_for_masters(BaseModel):
    order_id: int
    stage_id: int
    connected_user_id: int
    quantity: float = Field(..., ge=0)


class UpdateOrder_for_masters(BaseModel):
    id: int
    connected_user_id: int
    quantity: float = Field(..., ge=0)

