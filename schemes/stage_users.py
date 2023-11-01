from pydantic import BaseModel


class CreateStage_user(BaseModel):
    connected_user_id: int


class UpdateStage_user(BaseModel):
    id: int
    connected_user_id: int


