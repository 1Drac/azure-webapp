from .__init__ import *


class IngredientList(SQLModel):
    name: str
    quantity: float
    unit: str

class RecipeInput(SQLModel):
    name : str
    description : str
    ingredients : list[IngredientList]

class RecipeOutput(RecipeInput):
    id : int

class RecipeCreate(SQLModel):
    id : int | None = Field(primary_key=True, default=None)
    name : str
    description : str
    create_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
class RecipeIngredientCreate(SQLModel):
    id_recipe : int = Field(foreign_key='recipe.id', primary_key=True)
    id_ingredient : int = Field(foreign_key='ingredient.id', primary_key=True)
    quantity : float
    unit: str
    create_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)


