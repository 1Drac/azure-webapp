import os
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import URL
from dotenv import load_dotenv
from fastapi import Depends
from typing import Annotated

load_dotenv()

driver_name = os.getenv('DRIVER')
server_name = os.getenv('SERVER_NAME')
database_name = os.getenv('DATABASE_NAME')
database_login = os.getenv('DATABASE_LOGIN')
database_password = os.getenv('DATABASE_PASSWORD')

connection_string = f'Driver={driver_name};Server=tcp:{server_name}.database.windows.net,1433;Database={database_name};Uid={database_login};Pwd={database_password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
# connection_url = 'sqlite:///database.db'
engine = create_engine(connection_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]