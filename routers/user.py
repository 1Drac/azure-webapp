from .__init__ import *
from ..models.users import UserInput, UserCreate, UserOutput
from ..models.tables import User

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

@router.post('/', response_model=UserOutput)
def post_user(user: UserInput, session: SessionDep):

    # Search the user name in the User table to see if its exists
    db_user = session.exec(select(User).where(User.name == user.name)).first()
    if db_user:
        raise HTTPException(status_code=409, detail="User already exists.")
    
    # Insert in the User table the new user
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get('/', response_model=list[UserOutput])
def get_users(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):

    # Search all users in the User table
    db_users = session.exec(select(User).offset(offset).limit(limit).order_by(User.id)).all()
    return db_users