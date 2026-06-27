from pydantic import BaseModel, Field, EmailStr, ConfigDict

# --- Authentication Schemas ---

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


# --- Recipe Schemas ---

class Ingredient(BaseModel):
    name: str
    quantity: int
    unit: str


class Equipment(BaseModel):
    name: str


class RecipeCreate(BaseModel):
    title: str
    description: str
    durationInMinutes: int
    serving: int
    notes: str
    ingredients: list[Ingredient]
    equipments: list[Equipment]


class RecipeOut(BaseModel): 
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    durationInMinutes: int
    serving: int
    notes: str
    userid: int
    ingredients: list[Ingredient]
    equipments: list[Equipment]
    