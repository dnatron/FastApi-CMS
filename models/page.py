from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from models.user import User

from models.category import PageCategory, BlockCategory

class PageRole(str, Enum):
    FOR_ALL = "for_all"
    FOR_REGISTRED = "for_registred"
    FOR_ADMIN = "for_admin"

class PageBase(SQLModel):
    title: str
    content: str = Field(default="Stránka není vytvořena")
    page_template: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[str] = None
    url_friendly: str = Field(unique=True, index=True)
    is_published: bool = True
    role: PageRole = Field(default=PageRole.FOR_ALL)
    
class Page(PageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    category_id: Optional[int] = Field(default=None, foreign_key="pagecategory.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship(back_populates="pages", sa_relationship_kwargs={"lazy": "selectin"})
    category: Optional["PageCategory"] = Relationship(back_populates="pages", sa_relationship_kwargs={"lazy": "selectin"})
    bloks: List["PageBloks"] = Relationship(back_populates="page", sa_relationship_kwargs={"lazy": "selectin"})

# Třída Category byla přesunuta do models/category.py

class BloksBase(SQLModel):
    name: str
    content: str

class PageBloks(BloksBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page_id: int = Field(foreign_key="page.id")
    position: int
    # Relationships
    page: "Page" = Relationship(back_populates="bloks", sa_relationship_kwargs={"lazy": "selectin"})

class Block(BloksBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: Optional[int] = Field(default=None, foreign_key="blockcategory.id")
    # Relationships
    category: "BlockCategory" = Relationship(back_populates="blocks", sa_relationship_kwargs={"lazy": "selectin"})

class CategoryBloks(SQLModel, table=True):
    category_id: Optional[int] = Field(default=None, foreign_key="blockcategory.id", primary_key=True)
    block_id: Optional[int] = Field(default=None, foreign_key="block.id", primary_key=True)

