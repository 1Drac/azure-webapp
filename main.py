from fastapi import FastAPI
from sqlmodel import SQLModel

from .database import engine
from .routers import diet, ingredient, recipe, user

app = FastAPI()
app.include_router(user.router)
app.include_router(ingredient.router)
app.include_router(recipe.router)
app.include_router(diet.router)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)