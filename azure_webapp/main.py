from fastapi import FastAPI, Depends
import urllib
import struct
from typing import Annotated
from sqlmodel import SQLModel, Field, create_engine, Session
from azure.identity import DefaultAzureCredential
from sqlalchemy import event


credential = DefaultAzureCredential()

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

driver_name = '{ODBC Driver 18 for SQL Server}'
server_name = 'drac-webapp'
database_name = 'web-app-database'
user_name = '13f37c78-05fa-419b-bc36-31088c73635f'

connection_string = 'Driver={};Server=tcp:{}.database.windows.net,1433;Database={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'.format(driver_name, server_name, database_name)

params = urllib.parse.quote(connection_string)
url = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(url)

# from https://docs.sqlalchemy.org/en/20/core/engines.html#generating-dynamic-authentication-tokens
@event.listens_for(engine, "do_connect")
def provide_token(dialect, conn_rec, cargs, cparams):
    
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h

    cparams["attrs_before"] = {SQL_COPT_SS_ACCESS_TOKEN: token_struct}


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