from .__init__ import *
from ..models.recipes import RecipeInput, RecipeCreate, RecipeIngredientCreate, RecipeOutput, IngredientList
from ..models.tables import Ingredient, User, Recipe, RecipeIngredient


router = APIRouter(
    prefix='/recipes',
    tags=['recipes'],
)


@router.post('/', response_model=RecipeOutput)
def post_recipe(recipe: RecipeInput, session: SessionDep):

    # Search the recipe name in the Recipe table to see if its exists
    db_recipe = session.exec(select(Recipe).where(Recipe.name == recipe.name)).first()
    if db_recipe:
        raise HTTPException(status_code=409, detail="Recipe already exists.")

    for ingredient in recipe.ingredients:
        db_ingredient = session.exec(select(Ingredient).where(Ingredient.name == ingredient.name)).first()
        if db_ingredient is None:
            raise HTTPException(status_code=404, detail="Ingredient not found.")
    
    db_recipe = RecipeCreate.model_validate(recipe)
    db_recipe = Recipe.model_validate(db_recipe)

    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)

    for ingredient in recipe.ingredients:
        db_ingredient = session.exec(select(Ingredient).where(Ingredient.name == ingredient.name)).first()
        recipe_ingredient = RecipeIngredientCreate(
            id_recipe = db_recipe.id,
            id_ingredient = db_ingredient.id,
            quantity = ingredient.quantity,
            unit = ingredient.unit
        )

        db_recipe_ingredient = RecipeIngredient.model_validate(recipe_ingredient)
        session.add(db_recipe_ingredient)

    session.commit()
    session.refresh(db_recipe_ingredient)

    recipe_output = RecipeOutput(
        id = db_recipe.id,
        name = recipe.name,
        description = recipe.description,
        ingredients = recipe.ingredients,
    )
    print(recipe_output)
    return recipe_output

@router.get('/', response_model=list[RecipeOutput])
def get_recipe(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):

    recipes = session.exec(select(Recipe).offset(offset).limit(limit).order_by(Recipe.id)).all()
    recipes_output = []
    for recipe in recipes:
        ingredients = []
        for ingredient in recipe.ingredients:
            ingredients.append(
                IngredientList(
                    name = ingredient.ingredient.name,
                    quantity = ingredient.quantity,
                    unit = ingredient.unit
                )
            )

        recipes_output.append(
            RecipeOutput(
                id = recipe.id,
                name = recipe.name,
                description = recipe.description,
                ingredients = ingredients
            )
        )
    
    return recipes_output