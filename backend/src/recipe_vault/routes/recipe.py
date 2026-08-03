from fastapi import APIRouter, File, HTTPException, UploadFile, status

from database import close_connection, create_connection
from schemas.recipes import AIRecipeParseOut, RecipeDBOut, RecipeToDB

route = APIRouter(prefix="/recipe", tags=["recipe"])


@route.post("/upload_file_to_json", response_model=AIRecipeParseOut)
async def upload_file_to_json(file: UploadFile = File(...)):
    pass


@route.post("/url_to_json", response_model=AIRecipeParseOut)
async def upload_url_to_json(url: str):
    pass

@route.post("/recipe_to_db", response_model=RecipeDBOut)
def recipe_to_db(data: RecipeToDB):
    pass

@route.put("/{recipeid}", response_model=RecipeDBOut)
def update_recipe(recipeid: int, data: RecipeToDB):
    pass

@route.delete("/{recipeid}")
def delete_recipe(recipeid: int):
    pass

@route.get("/{userid}/{recipeid}", response_model=RecipeDBOut)
def get_recipe(userid: int, recipeid: int):
    pass