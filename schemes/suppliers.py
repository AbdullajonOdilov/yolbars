from pydantic import BaseModel
from typing import Optional, List

from schemes.phones import CreatePhone


class SuppliersCreate(BaseModel):
    name: str
    address: str
    comment: Optional[str] = ''
    phones: List[CreatePhone]


class SuppliersUpdate(BaseModel):
    id: int
    name: str
    address: str
    comment: Optional[str]=''
    phones: List[CreatePhone]


