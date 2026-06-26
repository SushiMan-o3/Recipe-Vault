from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    name: str
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    name: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str
