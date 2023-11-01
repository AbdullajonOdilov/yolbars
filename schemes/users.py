from typing import List
from pydantic import BaseModel
from schemes.phones import CreatePhone, UpdatePhone


class CreateUser(BaseModel):
    name: str
    username: str
    password_hash: str
    role: str
    salary: float
    phones: List[CreatePhone]


class UpdateUser(BaseModel):
    id: int
    name: str
    username: str
    password_hash: str
    role: str
    status: bool
    salary: float
    phones: List[UpdatePhone]


class TokenUser(BaseModel):
    id: int
    username: str
    role: str
    token: str


class UserCurrent(BaseModel):
    id: int
    name: str
    username: str
    password_hash: str
    role: str
    status: bool

