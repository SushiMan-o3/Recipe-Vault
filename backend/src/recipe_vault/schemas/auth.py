from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    user: str
    token: str


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    user: str
    password: str