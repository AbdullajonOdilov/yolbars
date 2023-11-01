from pydantic import BaseModel, Field


class UpdateWarehouse_products(BaseModel):
    id: int
    category_detail_id: int
    quantity: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    currency_id: int
