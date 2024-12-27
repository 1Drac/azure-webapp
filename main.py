from fastapi import FastAPI, Query, HTTPException
from sqlmodel import SQLModel, select
from typing import Annotated

from .database import engine, SessionDep
from .models import (
    Ingredient, IngredientCreate, IngredientPublic,
    User, UserCreate, UserPublic,
    Recepie, RecepieCreate, RecepiePublic,
    RecepieIngredient, RecepieIngredientCreate,
)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get('/')
def root():
    return {
        'message' : 'Ingredient database'
    }

@app.post('/ingredient/', response_model=IngredientPublic)
def post_ingredient(ingredient: IngredientCreate, session: SessionDep):

    if session.exec(select(Ingredient).where(Ingredient.name == ingredient.name)).first():
        raise HTTPException(status_code=409, detail="Ingredient already exists.")

    db_ingredient = Ingredient.model_validate(ingredient)
    session.add(db_ingredient)
    session.commit()
    session.refresh(db_ingredient)
    return db_ingredient

@app.get('/ingredient/', response_model=list[IngredientPublic])
def get_ingredient(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    ingredients = session.exec(select(Ingredient).offset(offset).limit(limit).order_by(Ingredient.id)).all()
    return ingredients

@app.post('/user/', response_model=UserPublic)
def post_user(user: UserCreate, session: SessionDep):

    if session.exec(select(User).where(User.name == user.name)).first():
        raise HTTPException(status_code=409, detail="User already exists.")
    
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get('/user/', response_model=list[UserPublic])
def get_user(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    users = session.exec(select(User).offset(offset).limit(limit).order_by(User.id)).all()
    return users

@app.post('/recepie/', response_model=RecepiePublic)
def post_recepie(recepie_ingredient: RecepieIngredientCreate, session: SessionDep):

    if session.exec(select(Recepie).where(Recepie.name == recepie_ingredient.recepie)).first():
        raise HTTPException(status_code=409, detail="Recepie already exists.")

    user_validation = session.exec(select(User).where(User.name == recepie_ingredient.user)).first()
    if user_validation is None:
        raise HTTPException(status_code=404, detail="User not found.")

    ingredients_validated = {}
    for ingredients in recepie_ingredient.ingredients:
        ingredient_validation = session.exec(select(Ingredient).where(Ingredient.name == ingredients.ingredient)).first()
        if ingredient_validation is None:
            raise HTTPException(status_code=404, detail="Ingredient not found.")
        ingredients_validated[ingredient_validation.name] = ingredient_validation
        
    recepie = RecepieCreate(
            name=recepie_ingredient.recepie,
            description=recepie_ingredient.description,
        )
    db_recepie = Recepie.model_validate(recepie)

    session.add(db_recepie)
    session.commit()
    session.refresh(db_recepie)

    for ingredients in recepie_ingredient.ingredients:
        recepie_ingredient = RecepieIngredient(
            id_user = user_validation.id,
            id_recepie = db_recepie.id,
            id_ingredient = ingredients_validated[ingredients.ingredient].id,
            quantity = ingredients.quantity,
            unit = ingredients.unit
        )
        db_recepie_ingredient = RecepieIngredient.model_validate(recepie_ingredient)
        session.add(db_recepie_ingredient)

    session.commit()

    return db_recepie

@app.get('/recepie/', response_model=list[RecepiePublic])
def get_recepie(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    recepies = session.exec(select(Recepie).offset(offset).limit(limit)).all()
    return recepies