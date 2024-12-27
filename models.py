from sqlmodel import SQLModel, Field
from datetime import datetime


# Model and schemas for Ingredient table
class IngredientBase(SQLModel):

    name : str
    carbohydrate : float
    protein : float
    fat : float
    portion : float

class Ingredient(IngredientBase, table=True):

    __tablename__ = 'ingredient'

    id : int | None = Field(primary_key=True, default=None)
    create_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class IngredientCreate(IngredientBase):

    pass

class IngredientPublic(IngredientBase):

    id : int
    create_date: datetime

# Model and schemas for User table
class UserBase(SQLModel):

    name : str
    weight : float
    calories : float

class User(UserBase, table=True):

    __tablename__ = 'user'

    id : int | None = Field(primary_key=True, default=None)
    create_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class UserCreate(UserBase):

    pass

class UserPublic(UserBase):

    id : int
    create_date: datetime

# Model and schemas for Recepie table
class RecepieBase(SQLModel):

    name : str
    description : str

class Recepie(RecepieBase, table=True):

    __tablename__ = 'recepie'

    id : int | None = Field(primary_key=True, default=None)
    create_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class RecepieCreate(RecepieBase):

    pass

class RecepiePublic(RecepieBase):

    id : int
    create_date: datetime


# Model and schemas for Recepie_Ingredients table
class IngredientQuantity(SQLModel):

    ingredient: str
    quantity: float
    unit: str

class RecepieIngredient(SQLModel, table=True):

    __tablename__ = 'recepie_ingredients'

    id : int | None = Field(primary_key=True, default=None)
    id_user : int = Field(foreign_key='user.id')
    id_recepie : int = Field(foreign_key='recepie.id')
    id_ingredient : int = Field(foreign_key='ingredient.id')
    quantity : float
    unit: str
    create_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class RecepieIngredientCreate(SQLModel):

    user : str
    recepie : str
    description : str | None = Field(default=None)
    ingredients : list[IngredientQuantity]

