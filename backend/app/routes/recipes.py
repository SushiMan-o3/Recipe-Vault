from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, Recipe, Ingredient, Equipment
from schemas import RecipeCreate, RecipeOut, Ingredient as IngredientSchema, Equipment as EquipmentSchema
from routes.auth import get_current_user


router = APIRouter(prefix="/recipes", tags=["recipes"])

# --- Recipe Endpoints ---

@router.get("/")
def get_all_recipes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recipes = db.query(Recipe).filter(Recipe.userid == current_user.id).all()
    return recipes


@router.post("/", response_model=RecipeOut)
def create_recipe_manual(recipe: RecipeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        durationInMinutes=recipe.durationInMinutes,
        serving=recipe.serving,
        notes=recipe.notes,
        userid=current_user.id
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    for ingredient in recipe.ingredients:
        new_ingredient = Ingredient(
            name=ingredient.name,
            recipeid=new_recipe.id
        )
        db.add(new_ingredient)

    for equipment in recipe.equipments:
        new_equipment = Equipment(
            name=equipment.name,
            recipeid=new_recipe.id
        )
        db.add(new_equipment)

    db.commit()
    
    return new_recipe


@router.get("/{recipe_id}", response_model=RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.userid == current_user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.userid == current_user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.query(Ingredient).filter(Ingredient.recipeid == recipe_id).delete()
    db.query(Equipment).filter(Equipment.recipeid == recipe_id).delete()
    db.delete(recipe)
    db.commit()
    return {"detail": "Ingredients and equipments deleted successfully"}


@router.patch("/{recipe_id}", response_model=RecipeOut)
def update_recipe(recipe_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.userid == current_user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # figure out how to update the recipe with new data from the request body
    
    return 