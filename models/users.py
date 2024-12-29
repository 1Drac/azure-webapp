from .__init__ import *


class UserInput(SQLModel):
    name : str
    weight : float
    calories : float

class UserOutput(UserInput):
    id : int

class UserCreate(UserInput):
    id : int | None = Field(primary_key=True, default=None)
    create_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)



