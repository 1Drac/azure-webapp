from .__init__ import *


class IngredientInput(SQLModel):
    name : str
    carbohydrate : float
    protein : float
    fat : float
    portion : float

class IngredientOutput(IngredientInput):
    id : int

class IngredientCreate(IngredientInput):
    id : int | None = Field(primary_key=True, default=None)
    create_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)


