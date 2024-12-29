from .__init__ import *
from .diet import DietCreate, DietRecipeCreate
from .ingredients import IngredientCreate
from .recipes import RecipeCreate, RecipeIngredientCreate
from .users import UserCreate


class Diet(DietCreate, table=True):
    __tablename__ = 'diet'

    recipes : list['DietRecipe'] = Relationship(back_populates="diet")
    user : 'User' = Relationship(back_populates='diets')

class DietRecipe(DietRecipeCreate, table=True):  
    __tablename__ = 'diet_recipe'

    diet: 'Diet' = Relationship(back_populates="recipes")
    recipe: 'Recipe' = Relationship(back_populates="diets")

class User(UserCreate, table=True):
    __tablename__ = 'user'

    diets : list['Diet'] = Relationship(back_populates="user")

class RecipeIngredient(RecipeIngredientCreate, table=True):
    __tablename__ = 'recipe_ingredients'

    recipe: 'Recipe' = Relationship(back_populates="ingredients")
    ingredient: 'Ingredient' = Relationship(back_populates="recipes")

class Recipe(RecipeCreate, table=True):
    __tablename__ = 'recipe'

    ingredients : list['RecipeIngredient'] = Relationship(back_populates='recipe')
    diets : list['DietRecipe'] = Relationship(back_populates="recipe")

class Ingredient(IngredientCreate, table=True):
    __tablename__ = 'ingredient'

    recipes : list['RecipeIngredient'] = Relationship(back_populates='ingredient')