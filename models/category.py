from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from models.page import Page, Block

# Základní třída pro kategorie
class CategoryBase(SQLModel):
    name: str
    description: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[str] = None
    url_friendly: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Kategorie pro stránky
class PageCategory(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parent_category_id: Optional[int] = Field(default=None, foreign_key="pagecategory.id")
    
    # Relationships
    parent_category: Optional["PageCategory"] = Relationship(
        sa_relationship_kwargs={"remote_side": "PageCategory.id", "lazy": "selectin"},
        back_populates="child_categories"
    )
    child_categories: List["PageCategory"] = Relationship(back_populates="parent_category", sa_relationship_kwargs={"lazy": "selectin"})
    pages: List["Page"] = Relationship(back_populates="category", sa_relationship_kwargs={"lazy": "selectin"})

# Kategorie pro blog
class BlogCategory(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parent_category_id: Optional[int] = Field(default=None, foreign_key="blogcategory.id")
    
    # Relationships
    parent_category: Optional["BlogCategory"] = Relationship(
        sa_relationship_kwargs={"remote_side": "BlogCategory.id", "lazy": "selectin"},
        back_populates="child_categories"
    )
    child_categories: List["BlogCategory"] = Relationship(back_populates="parent_category", sa_relationship_kwargs={"lazy": "selectin"})

# Kategorie pro bloky obsahu
class BlockCategory(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parent_category_id: Optional[int] = Field(default=None, foreign_key="blockcategory.id")
    
    # Relationships
    parent_category: Optional["BlockCategory"] = Relationship(
        sa_relationship_kwargs={"remote_side": "BlockCategory.id", "lazy": "selectin"},
        back_populates="child_categories"
    )
    child_categories: List["BlockCategory"] = Relationship(back_populates="parent_category", sa_relationship_kwargs={"lazy": "selectin"})
    blocks: List["Block"] = Relationship(back_populates="category", sa_relationship_kwargs={"lazy": "selectin"})
