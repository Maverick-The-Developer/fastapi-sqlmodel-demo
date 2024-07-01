from sqlmodel import Field, SQLModel
from datetime import datetime

class PostBase(SQLModel):
    title: str
    content: str | None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase, table=True):
    __tablename__ = "post"
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now())

class PostListResponse(SQLModel):
    posts: list[Post]
    total: int