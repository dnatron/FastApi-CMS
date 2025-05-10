from datetime import datetime

from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from database.database import get_session
from models.user import User
from models.page import Page
from models.blog import Article
from security.utility_auth import get_current_admin_user

# Vytvoření routeru
router = APIRouter(tags=["admin"], prefix="/admin")

# Nastavení šablon
templates = Jinja2Templates(directory="templates")


# Admin dashboard
@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    try:
        # Získání aktuálního administrátora s použitím requestu pro přístup ke cookies
        current_user = await get_current_admin_user(request=request)
        
        # Získání statistik
        db = next(get_session())
        
        # Počet stránek
        pages_count = db.exec(select(Page)).count()
        
        # Počet článků
        articles_count = db.exec(select(Article)).count()
        
        # Počet uživatelů
        users_count = db.exec(select(User)).count()
        
        # Vytvoření statistik
        stats = {
            "pages_count": pages_count,
            "articles_count": articles_count,
            "users_count": users_count
        }
        
        # Aktuální datum
        current_date = datetime.now().strftime("%d.%m.%Y")
        
        # Systémové informace
        system_info = {
            "version": "0.1.0",
            "database": "SQLite",
            "python_version": "3.9",
            "fastapi_version": "0.103.1",
            "sqlmodel_version": "0.0.8",
            "last_update": "10.05.2025"
        }
        
        return templates.TemplateResponse(
            "admin/dashboard.html",
            {
                "request": request, 
                "user": current_user,
                "stats": stats,
                "current_date": current_date,
                "system_info": system_info,
                "recent_activities": []  # Prázdný seznam aktivit (bude implementováno později)
            },
        )
    except HTTPException:
        # Přesměrování na přihlašovací stránku v případě chyby autentizace
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


# Správa uživatelů
@router.get("/users", response_class=HTMLResponse)
async def admin_users(request: Request):
    try:
        # Získání aktuálního administrátora s použitím requestu pro přístup ke cookies
        current_user = await get_current_admin_user(request=request)
        
        # Získání seznamu uživatelů
        db = next(get_session())
        users = db.exec(select(User)).all()
        
        # Přidání barvy role pro každého uživatele
        for user in users:
            if user.role == "admin":
                user.role_color = "admin"
            elif user.role == "editor":
                user.role_color = "editor"
            else:
                user.role_color = "user"
        
        return templates.TemplateResponse(
            "admin/usermanager/users.html",
            {"request": request, "user": current_user, "users": users},
        )
    except HTTPException:
        # Přesměrování na přihlašovací stránku v případě chyby autentizace
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
