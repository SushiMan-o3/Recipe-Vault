from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)

    posts = relationship("Recipe", back_populates="user")

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    durationInMinutes = Column(Integer, nullable=False)
    serving = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    userid = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User", back_populates="recipes")
    ingredients = relationship("Ingredient", back_populates="recipe")
    equipments = relationship("Equipment", back_populates="recipe")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit = Column(String(20), nullable=False)
    recipeid = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    
    recipe = relationship("Recipe", back_populates="ingredients")

class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    recipeid = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    
    recipe = relationship("Recipe", back_populates="equipments")
