from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from datetime import datetime

from database.database import init_db, get_session
from routers import user, admin
from models.category import PageCategory
from models.page import Page
from db_init import create_admin_if_not_exists, create_default_categories_if_not_exist, create_sample_pages_if_not_exist, create_sample_user

# Vytvoření FastAPI aplikace
app = FastAPI(title="FastAPI CMS", description="Jednoduchý CMS systém postavený na FastAPI a SQLModel")

# Inicializace aplikace
@app.on_event("startup")
def on_startup():
    # Inicializace databáze
    init_db()
    
    # -------Sample data-------
    db = next(get_session())
    create_admin_if_not_exists(db)
    create_sample_user(db)
    create_default_categories_if_not_exist(db)
    create_sample_pages_if_not_exist(db)

# Přidání CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # V produkci by mělo být omezeno na konkrétní domény
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nastavení statických souborů
app.mount("/static", StaticFiles(directory="static"), name="static")

# Nastavení šablon
templates = Jinja2Templates(directory="templates")

# Přidání routerů
app.include_router(user.router)
app.include_router(admin.router)


# Funkce pro získání kategorií stránek
def get_page_categories(db: Session):
    return db.exec(select(PageCategory).where(PageCategory.is_active).order_by(PageCategory.name)).all()

# Hlavní stránka
@app.get("/", tags=["pages"])
async def home(request: Request, db: Session = Depends(get_session)):
    # Získání kategorií stránek pro menu
    categories = get_page_categories(db)
    
    # Získání aktuálního roku pro šablonu
    current_year = datetime.now().year
    
    return templates.TemplateResponse("base.html", {
        "request": request, 
        "categories": categories,
        "current_year": current_year
    })

# Zobrazení stránek podle kategorie
@app.get("/category/{url_friendly}", tags=["pages"])
async def category_pages(request: Request, url_friendly: str, db: Session = Depends(get_session)):
    # Získání kategorií stránek pro menu
    categories = get_page_categories(db)
    
    # Získání konkrétní kategorie podle URL
    category = db.exec(select(PageCategory).where(PageCategory.url_friendly == url_friendly)).first()
    
    # Získání stránek v dané kategorii
    pages = []
    if category:
        pages = db.exec(select(Page).where(Page.category_id == category.id, Page.is_published)).all()
    
    # Získání aktuálního roku pro šablonu
    current_year = datetime.now().year
    
    return templates.TemplateResponse(
        "category.html", 
        {
            "request": request, 
            "categories": categories, 
            "category": category, 
            "pages": pages,
            "current_year": current_year
        }
    )


# Spuštění aplikace
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
