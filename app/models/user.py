from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
