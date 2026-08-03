from datetime import date

from pydantic import BaseModel, EmailStr, Field


class Profile(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    first_name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    bio: str | None = None
    birthday: date | None = None
    gender: str | None = Field(default=None, max_length=10)
    country: str | None = Field(default=None, max_length=56)
    profile_picture_url: str | None = None


class UpdateAdditionalInfo(BaseModel):
    first_name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    bio: str | None = None
    birthday: date | None = None
    gender: str | None = Field(default=None, max_length=10)
    country: str | None = Field(default=None, max_length=56)


class UpdateProfilePicture(BaseModel):
    profile_picture_url: str
