from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from models.page import Page
    from models.blog import Article, Comment

class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    USER = "user"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = Field(default=UserRole.USER)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    pages: List["Page"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    articles: List["Article"] = Relationship(back_populates="author", sa_relationship_kwargs={"lazy": "selectin"})
    comments: List["Comment"] = Relationship(back_populates="author", sa_relationship_kwargs={"lazy": "selectin"})
