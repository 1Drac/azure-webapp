from .__init__ import *
from ..models.ingredients import IngredientInput, IngredientCreate, IngredientOutput
from ..models.tables import Ingredient


router = APIRouter(
    prefix='/ingredients',
    tags=['ingredients'],
)

@router.post('/', response_model=IngredientOutput)
def post_ingredient(ingredient: IngredientInput, session: SessionDep):

    # Search the ingredient name in the Ingredient table to see if its exists
    db_ingredient = session.exec(select(Ingredient).where(Ingredient.name == ingredient.name)).first()
    if db_ingredient:
        raise HTTPException(status_code=409, detail="Ingredient already exists.")

    # Insert in the ingredient table the new Ingredient
    db_ingredient = Ingredient.model_validate(ingredient)
    session.add(db_ingredient)
    session.commit()
    session.refresh(db_ingredient)
    return db_ingredient

@router.get('/', response_model=list[IngredientOutput])
def get_ingredients(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):

    # Search all ingredients in the Ingredient table
    db_ingredients = session.exec(select(Ingredient).offset(offset).limit(limit).order_by(Ingredient.id)).all()
    return db_ingredients