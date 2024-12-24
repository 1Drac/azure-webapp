from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy import URL
import os
from dotenv import load_dotenv

load_dotenv()

driver_name = os.getenv('DRIVER')
server_name = os.getenv('SERVER_NAME')
database_name = os.getenv('DATABASE_NAME')
database_login = os.getenv('DATABASE_LOGIN')
database_password = os.getenv('DATABASE_PASSWORD')

connection_string = f'Driver={driver_name};Server=tcp:{server_name}.database.windows.net,1433;Database={database_name};Uid={database_login};Pwd={database_password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

class IngredientBase(SQLModel):

    name : str = Field(index=False)
    carbohydrate : float = Field(index=True)
    protein : float = Field(index=True)
    fat : float = Field(index=True)
    portion : float = Field(index=True)

class Ingredient(IngredientBase, table=True):

    id : int | None = Field(default=None, primary_key=True)

class IngredientPublic(IngredientBase):
    id : int

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get('/')
def root():
    return {
        'message' : 'Ingredient database'
    }

@app.post('/ingredients/', response_model=IngredientPublic)
def create_ingredient(ingredient: IngredientBase, session: SessionDep):
    db_ingredient = Ingredient.model_validate(ingredient)
    session.add(db_ingredient)
    session.commit()
    session.refresh(db_ingredient)
    return db_ingredient