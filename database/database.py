from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path

# Definice cesty k databázi
BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/db.db"

# Vytvoření engine pro SQLModel
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# Funkce pro inicializaci databáze
def init_db():
    SQLModel.metadata.create_all(engine)

# Funkce pro získání session
def get_session():
    with Session(engine) as session:
        yield session
