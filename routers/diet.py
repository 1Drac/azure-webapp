from .__init__ import *
from ..models.diet import DietCreate, DietInput, DietOutput, RecipeList, DietRecipeCreate
from ..models.tables import Diet, User, Recipe, DietRecipe

router = APIRouter(
    prefix='/diet',
    tags=['diet'],
)

@router.post('/', response_model=DietOutput)
def post_diet(diet: DietInput, session: SessionDep):

    # Serch the user name in the User table to see if it exist    
    db_user = session.exec(select(User).where(User.name == diet.user)).first()
    if db_user is None:
            raise HTTPException(status_code=404, detail="User not found.")
    
    # Search the diet name in the Diet table to see if its exists for this user
    db_diet = session.exec(select(Diet).where((Diet.name == diet.name) & (Diet.id_user == db_user.id))).first()
    if db_diet:
        raise HTTPException(status_code=409, detail="Diet already exists for this user.")

    for recipe in diet.recipes:
        db_recipe = session.exec(select(Recipe).where(Recipe.name == recipe.name)).first()
        if db_recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found.")
    
    db_diet = DietCreate(
        id_user = db_user.id,
        name = diet.name,
    )

    db_diet = Diet.model_validate(db_diet)

    session.add(db_diet)
    session.commit()
    session.refresh(db_diet)

    for recipe in diet.recipes:
        db_recipe = session.exec(select(Recipe).where(Recipe.name == recipe.name)).first()
        diet_recipe = DietRecipeCreate(
            id_diet = db_diet.id,
            id_recipe = db_recipe.id,
            quantity = recipe.quantity
        )

        db_diet_recipe = DietRecipe.model_validate(diet_recipe)
        session.add(db_diet_recipe)

    session.commit()
    session.refresh(db_diet_recipe)

    diet_output = DietOutput(
        id = db_diet.id,
        user = diet.user,
        name = diet.name,
        recipes = diet.recipes,
    )
    return diet_output

        
@router.get('/', response_model=list[DietOutput])
def get_diet(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    
    diets = session.exec(select(Diet).offset(offset).limit(limit).order_by(Diet.id)).all()
    diets_output = []
    for diet in diets:
        recipes = []
        for recipe in diet.recipes:  
            recipes.append(
                RecipeList(
                    name = recipe.recipe.name,
                    quantity = recipe.quantity
                )
            )

        diets_output.append(
            DietOutput(
                id = diet.id,
                name = diet.name,
                user = diet.user.name,
                recipes = recipes,
            )
        )

    return diets_output