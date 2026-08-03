from typing import Optional

from pydantic import BaseModel, Field


class IngredientOut(BaseModel):
    name: str


class EquipmentOut(BaseModel):
    name: str


class AIRecipeOut(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    instructions: Optional[str] = None
    durationInMinutes: Optional[int] = None
    serving: Optional[int] = None
    notes: Optional[str] = None


class AIRecipeParseOut(BaseModel):
    recipe: AIRecipeOut
    ingredients: list[IngredientOut] = []
    equipments: list[EquipmentOut] = []
    unmapped_text: list[str] = []
    
class RecipeCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    instructions: str
    durationInMinutes: int
    serving: int
    notes: Optional[str] = None


class RecipeToDB(BaseModel):
    recipe: RecipeCreate
    ingredients: list[IngredientOut] = []
    equipments: list[EquipmentOut] = []
    
class IngredientDBOut(IngredientOut):
    id: int


class EquipmentDBOut(EquipmentOut):
    id: int


class RecipeDBOut(BaseModel):
    id: int
    user_id: int
    recipe: RecipeCreate
    ingredients: list[IngredientDBOut] = []
    equipments: list[EquipmentDBOut] = []