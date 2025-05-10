from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from datetime import datetime

from database.database import init_db, get_session
from routers import user
from models.user import User, UserRole
from models.category import PageCategory
from models.page import Page
from security.utility_auth import get_password_hash

# Vytvoření FastAPI aplikace
app = FastAPI(title="FastAPI CMS", description="Jednoduchý CMS systém postavený na FastAPI a SQLModel")

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


# Vytvoření administrátora při prvním spuštění
def create_admin_if_not_exists(db: Session):
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin"),  # V produkci použít silné heslo
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            is_active=True,
        )
        db.add(admin_user)
        db.commit()
        print("Admin uživatel vytvořen")


# Funkce pro získání kategorií stránek
def get_page_categories(db: Session):
    return db.exec(select(PageCategory).where(PageCategory.is_active).order_by(PageCategory.name)).all()

# Funkce pro vytvoření výchozích kategorií
def create_default_categories_if_not_exist(db: Session):
    # Kontrola, zda již existují nějaké kategorie
    categories_count = db.exec(select(PageCategory)).all()
    if not categories_count:
        # Vytvoření výchozích kategorií
        default_categories = [
            PageCategory(
                name="Hlavní stránky",
                description="Hlavní stránky webu",
                url_friendly="hlavni-stranky",
                is_active=True
            ),
            PageCategory(
                name="O nás",
                description="Informace o nás",
                url_friendly="o-nas",
                is_active=True
            ),
            PageCategory(
                name="Služby",
                description="Naše služby",
                url_friendly="sluzby",
                is_active=True
            ),
            PageCategory(
                name="Kontakt",
                description="Kontaktní informace",
                url_friendly="kontakt",
                is_active=True
            ),
        ]
        
        for category in default_categories:
            db.add(category)
        
        db.commit()
        print("Výchozí kategorie vytvořeny")

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


# Inicializace aplikace
@app.on_event("startup")
def on_startup():
    # Inicializace databáze
    init_db()
    
    # Vytvoření administrátora a výchozích kategorií
    db = next(get_session())
    create_admin_if_not_exists(db)
    create_default_categories_if_not_exist(db)


# Spuštění aplikace
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
