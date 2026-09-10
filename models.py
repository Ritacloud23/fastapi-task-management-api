from sqlmodel import Field, SQLModel



class UserBase(SQLModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    id: int




class TaskBase(SQLModel):
    title: str
    description: str | None = None
    status: str = "todo"


class TaskCreate(TaskBase):
    user_id: int


class TaskPublic(TaskBase):
    id: int
    user_id: int


class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None



class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")