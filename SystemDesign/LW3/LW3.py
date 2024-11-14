from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from passlib.context import CryptContext
from databases import Database
import os

# URL для подключения к базе данных
DATABASE_URL = "postgresql://stud:Zaq123edc@127.0.0.1:47292/t_db"  # Замените на свои учетные данные PostgreSQL

# Инициализация подключения к базе данных PostgreSQL
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Модель пользователя для таблицы users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)


# Зависимость для подключения к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Функция для создания нового пользователя с хешированным паролем
def create_user(db, username: str, name: str, surname: str, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    db_user = User(username=username, name=name, surname=surname, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Конечная точка для регистрации нового пользователя
@app.post("/users/")
async def register_user(username: str, name: str, surname: str, email: str, password: str, db=Depends(get_db)):
    db_user = create_user(db, username, name, surname, email, password)
    return db_user