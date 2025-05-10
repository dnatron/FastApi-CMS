from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from database.database import get_session
from models.user import User, UserRole

# Nastavení pro JWT
SECRET_KEY = "tajny_klic_pro_jwt_token_zmenit_v_produkci"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Nastavení pro hashování hesel
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme pro získání tokenu z hlavičky Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def verify_password(plain_password, hashed_password):
    """Ověří, zda se heslo shoduje s hashem."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Vytvoří hash z hesla."""
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    """Získá uživatele podle uživatelského jména."""
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    return user


def authenticate_user(db: Session, username: str, password: str):
    """Ověří uživatele podle uživatelského jména a hesla."""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Vytvoří JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request = None, token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    """Získá aktuálního uživatele z JWT tokenu nebo cookie."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Pokus o získání tokenu z cookie, pokud je request k dispozici
    token_from_cookie = None
    if request:
        token_cookie = request.cookies.get("access_token")
        if token_cookie and token_cookie.startswith("Bearer "):
            token_from_cookie = token_cookie.replace("Bearer ", "")
    
    # Použití tokenu z cookie nebo z OAuth2 scheme
    actual_token = token_from_cookie or token
    
    if not actual_token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(actual_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Získá aktuálního aktivního uživatele."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Neaktivní uživatel")
    return current_user


async def get_current_admin_user(current_user: User = Depends(get_current_active_user)):
    """Získá aktuálního uživatele s rolí admin."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nedostatečná oprávnění",
        )
    return current_user


async def get_current_editor_user(current_user: User = Depends(get_current_active_user)):
    """Získá aktuálního uživatele s rolí editor nebo admin."""
    if current_user.role not in [UserRole.ADMIN, UserRole.EDITOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nedostatečná oprávnění",
        )
    return current_user
