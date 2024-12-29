from .__init__ import *


class RecipeList(SQLModel):
    name : str
    quantity : float


class DietInput(SQLModel):
    name: str
    user : str
    recipes : list[RecipeList]

class DietOutput(DietInput):
    id : int

class DietCreate(SQLModel):
    id : int | None = Field(primary_key=True, default=None) 
    id_user : int = Field(foreign_key='user.id')  
    name : str
    create_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class DietRecipeCreate(SQLModel):  
    id_diet : int = Field(foreign_key='diet.id', primary_key=True)
    id_recipe : int = Field(foreign_key='recipe.id', primary_key=True)
    quantity: float
    create_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)



    