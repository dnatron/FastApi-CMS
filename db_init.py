from sqlmodel import Session, select

from database.database import init_db, get_session
from models.user import User, UserRole
from models.category import PageCategory
from models.page import Page
from security.utility_auth import get_password_hash


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


# Vytvoření ukázkových uživatelů
def create_sample_user(db: Session):
    # Počet ukázkových uživatelů, které chceme vytvořit
    num_users = 4
    
    for i in range(1, num_users + 1):
        username = f"user{i}"
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            user = User(
                username=username,
                email=f"{username}@example.com",
                hashed_password=get_password_hash(username),  # Heslo je stejné jako uživatelské jméno
                first_name=f"User{i}",
                last_name="Sample",
                role=UserRole.USER,
                is_active=True,
            )
            db.add(user)
            print(f"Ukázkový uživatel {username} vytvořen")
    
    # Commit všech změn najednou pro lepší výkon
    db.commit()


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


# Funkce pro vytvoření ukázkových stránek
def create_sample_pages_if_not_exist(db: Session):
    # Kontrola, zda již existují nějaké stránky
    pages_count = db.exec(select(Page)).all()
    if not pages_count:
        # Získání admin uživatele
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("Admin uživatel neexistuje, nelze vytvořit ukázkové stránky")
            return
            
        # Získání kategorií
        categories = {}
        for category in db.exec(select(PageCategory)).all():
            categories[category.url_friendly] = category
        
        # Vytvoření ukázkových stránek
        sample_pages = [
            Page(
                title="Hlavní stránka",
                content="<h1>Vítejte na našem webu</h1><p>Toto je hlavní stránka našeho webu vytvořeného pomocí FastAPI CMS.</p>",
                meta_title="Hlavní stránka | FastAPI CMS",
                meta_description="Vítejte na našem webu vytvořeném pomocí FastAPI CMS",
                keywords="fastapi, cms, hlavní stránka",
                url_friendly="hlavni-stranka",
                is_published=True,
                user_id=admin.id,
                category_id=categories["hlavni-stranky"].id if "hlavni-stranky" in categories else None
            ),
            Page(
                title="O nás",
                content="<h1>O nás</h1><p>Jsme moderní firma zabývající se vývojem webových aplikací.</p>",
                meta_title="O nás | FastAPI CMS",
                meta_description="Informace o naší firmě",
                keywords="fastapi, cms, o nás, firma",
                url_friendly="o-nas",
                is_published=True,
                user_id=admin.id,
                category_id=categories["o-nas"].id if "o-nas" in categories else None
            ),
            Page(
                title="Naše služby",
                content="<h1>Naše služby</h1><p>Nabízíme široké spektrum služeb v oblasti vývoje webových aplikací.</p>",
                meta_title="Naše služby | FastAPI CMS",
                meta_description="Přehled našich služeb",
                keywords="fastapi, cms, služby, vývoj",
                url_friendly="nase-sluzby",
                is_published=True,
                user_id=admin.id,
                category_id=categories["sluzby"].id if "sluzby" in categories else None
            ),
            Page(
                title="Kontakt",
                content="<h1>Kontaktujte nás</h1><p>Email: info@example.com<br>Telefon: +420 123 456 789</p>",
                meta_title="Kontakt | FastAPI CMS",
                meta_description="Kontaktní informace",
                keywords="fastapi, cms, kontakt",
                url_friendly="kontakt",
                is_published=True,
                user_id=admin.id,
                category_id=categories["kontakt"].id if "kontakt" in categories else None
            ),
        ]
        
        for page in sample_pages:
            db.add(page)
        
        db.commit()
        print("Ukázkové stránky vytvořeny")


# Hlavní funkce pro inicializaci databáze
def initialize_database():
    # Inicializace databáze
    init_db()
    
    # Získání databázové relace
    db = next(get_session())
    
    # Vytvoření výchozích dat
    create_admin_if_not_exists(db)
    create_default_categories_if_not_exist(db)
    create_sample_pages_if_not_exist(db)
    
    print("Inicializace databáze dokončena")


# Spuštění inicializace při přímém spuštění souboru
if __name__ == "__main__":
    initialize_database()