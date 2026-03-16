from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str = "pending"


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


class TaskOut(TaskBase):
    id: int

    class Config:
        from_attributes = True