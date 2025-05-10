from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from models.user import User
    from models.category import BlogCategory

# Vazební tabulka mezi články a kategoriemi
class ArticleCategory(SQLModel, table=True):
    article_id: Optional[int] = Field(default=None, foreign_key="article.id", primary_key=True)
    category_id: Optional[int] = Field(default=None, foreign_key="blogcategory.id", primary_key=True)

# Vazební tabulka mezi články a tagy
class ArticleTag(SQLModel, table=True):
    article_id: Optional[int] = Field(default=None, foreign_key="article.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

# Třída Category byla přesunuta do models/category.py

class TagBase(SQLModel):
    name: str = Field(unique=True, index=True)
    url_friendly: str = Field(unique=True, index=True)

class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Relationships
    articles: List["Article"] = Relationship(back_populates="tags", link_model=ArticleTag)

class ArticleBase(SQLModel):
    title: str
    content: str
    short_description: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[str] = None
    url_friendly: str = Field(unique=True, index=True)
    is_published: bool = False
    publish_date: Optional[datetime] = None

class Article(ArticleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)  
    # Relationships
    author: "User" = Relationship(back_populates="articles", sa_relationship_kwargs={"lazy": "selectin"})
    categories: List["BlogCategory"] = Relationship(link_model=ArticleCategory, sa_relationship_kwargs={"lazy": "selectin"})
    tags: List[Tag] = Relationship(back_populates="articles", link_model=ArticleTag, sa_relationship_kwargs={"lazy": "selectin"})
    comments: List["Comment"] = Relationship(back_populates="article", sa_relationship_kwargs={"lazy": "selectin"})

class CommentBase(SQLModel):
    content: str
    is_approved: bool = False

class Comment(CommentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    article_id: int = Field(foreign_key="article.id")
    author_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Relationships
    article: Article = Relationship(back_populates="comments")
    author: "User" = Relationship(back_populates="comments")
