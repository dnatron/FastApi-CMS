from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from datetime import datetime

from database.database import init_db, get_session
from routers import user
from models.user import User
from models.page import Page
from models.category import PageCategory
from security.utility_auth import get_password_hash

# Vytvoření FastAPI aplikace
app = FastAPI(
    title="FastAPI CMS",
    description="Moderní CMS systém postavený na FastAPI a SQLModel",
    version="0.1.0"
)

# Přidání CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Připojení statických souborů
app.mount("/static", StaticFiles(directory="static"), name="static")

# Připojení šablon
templates = Jinja2Templates(directory="templates")

# Připojení routerů
app.include_router(user.router)


# Funkce pro vytvoření administrátora, pokud neexistuje
def create_admin_if_not_exists(db: Session):
    admin = db.exec(select(User).where(User.username == "admin")).first()
    if not admin:
        admin_user = User(
            username="admin",
            email="admin@example.com",
            full_name="Administrator",
            hashed_password=get_password_hash("admin"),
            is_active=True,
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created")


# Funkce pro získání kategorií stránek
def get_page_categories(db: Session):
    return db.exec(select(PageCategory).where(PageCategory.is_active)).all()


# Funkce pro vytvoření výchozích kategorií
def create_default_categories_if_not_exist(db: Session):
    # Kontrola, zda již existují kategorie
    existing_categories = db.exec(select(PageCategory)).all()
    if existing_categories:
        return
    
    # Vytvoření výchozích kategorií pro stránky
    default_page_categories = [
        PageCategory(
            name="Hlavní stránky",
            description="Hlavní stránky webu",
            url_friendly="hlavni-stranky",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        PageCategory(
            name="O nás",
            description="Informace o nás",
            url_friendly="o-nas",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        PageCategory(
            name="Služby",
            description="Naše služby",
            url_friendly="sluzby",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        PageCategory(
            name="Kontakt",
            description="Kontaktní informace",
            url_friendly="kontakt",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    
    for category in default_page_categories:
        db.add(category)
    
    db.commit()
    print("Default page categories created")


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
