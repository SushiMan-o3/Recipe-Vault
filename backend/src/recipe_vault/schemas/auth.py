from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    user: str
    token: str


class UserCreate(BaseModel):
    pass


class UserLogin(BaseModel):
    pass