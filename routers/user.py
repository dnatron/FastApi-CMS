from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from database.database import get_session
from models.user import User, UserRole
from security.utility_auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_current_admin_user,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

# Vytvoření routeru
router = APIRouter(tags=["users"])

# Nastavení šablon
templates = Jinja2Templates(directory="templates")


# API endpointy
@router.post("/api/auth/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neplatné uživatelské jméno nebo heslo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/api/users/me", response_model=dict)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
    }


@router.get("/api/users", response_model=List[dict])
async def read_users(db: Session = Depends(get_session), current_user: User = Depends(get_current_admin_user)):
    users = db.exec(select(User)).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        }
        for user in users
    ]


@router.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    username: str,
    email: str,
    password: str,
    first_name: str = None,
    last_name: str = None,
    role: UserRole = UserRole.USER,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user),
):
    # Kontrola, zda uživatel již neexistuje
    db_user = db.exec(select(User).where(User.username == username)).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uživatel s tímto uživatelským jménem již existuje",
        )

    db_user = db.exec(select(User).where(User.email == email)).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uživatel s tímto e-mailem již existuje",
        )

    # Vytvoření nového uživatele
    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        role=role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "username": new_user.username}


# Webové stránky
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("user/login.html", {"request": request})


@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_session)):
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse(
            "user/login.html",
            {"request": request, "error": "Neplatné uživatelské jméno nebo heslo"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("user/registration.html", {"request": request})


@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    first_name: str = Form(None),
    last_name: str = Form(None),
    db: Session = Depends(get_session),
):
    # Kontrola, zda hesla souhlasí
    if password != password_confirm:
        return templates.TemplateResponse(
            "user/registration.html",
            {"request": request, "error": "Hesla se neshodují"},
        )

    # Kontrola, zda uživatel již neexistuje
    db_user = db.exec(select(User).where(User.username == username)).first()
    if db_user:
        return templates.TemplateResponse(
            "user/registration.html",
            {"request": request, "error": "Uživatel s tímto uživatelským jménem již existuje"},
        )

    db_user = db.exec(select(User).where(User.email == email)).first()
    if db_user:
        return templates.TemplateResponse(
            "user/registration.html",
            {"request": request, "error": "Uživatel s tímto e-mailem již existuje"},
        )

    # Vytvoření nového uživatele
    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        role=UserRole.USER,  # Noví uživatelé mají vždy roli USER
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Přihlášení uživatele
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )

    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

    return response


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: User = Depends(get_current_active_user)):
    return templates.TemplateResponse(
        "user/dashboard.html",
        {"request": request, "user": current_user},
    )


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response
