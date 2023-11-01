from pydantic import BaseModel
from typing import Optional


class MeasureCreate(BaseModel):
    name: str


class MeasureUpdate(BaseModel):
    id: int
    name: str

