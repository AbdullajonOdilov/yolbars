from pydantic import BaseModel
from typing import List
from schemes.phones import CreatePhone, UpdatePhone


class CreateClient(BaseModel):
    name: str
    comment: str
    phones: List[CreatePhone]


class UpdateClient(BaseModel):
    id: int
    name: str
    comment: str
    phones: List[UpdatePhone]
