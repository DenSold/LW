from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from redis import Redis
from pymongo import MongoClient
import json
import os

# Конфигурации баз данных
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://stud:Zaq123edc@127.0.0.1:47292/t_db")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Инициализация PostgreSQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Инициализация MongoDB
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["t_db"]
collection = mongo_db["goals"]

# Инициализация Redis
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)

# Модель SQLAlchemy
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)

# FastAPI приложение
app = FastAPI()

# Зависимость для PostgreSQL
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ключ для кэша Redis
def get_redis_key_for_user(user_id: int) -> str:
    return f"user:{user_id}"

# API: Получение пользователя с кэшированием (Redis + PostgreSQL)
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    # 1. Проверяем кэш Redis
    redis_key = get_redis_key_for_user(user_id)
    cached_user = redis_client.get(redis_key)
    if cached_user:
        return json.loads(cached_user)

    # 2. Если данных нет в кэше, загружаем из PostgreSQL
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Сохраняем данные в кэш
    user_data = {"id": user.id, "username": user.username, "name": user.name, "surname": user.surname, "email": user.email}
    redis_client.set(redis_key, json.dumps(user_data), ex=3600)  # Кэш на 1 час

    return user_data

# API: Создание пользователя (обновление PostgreSQL + удаление из Redis)
@app.post("/users/")
def create_user(username: str, name: str, surname: str, email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = "hashed_" + password  # Условный хэш
    db_user = User(username=username, name=name, surname=surname, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Удаляем данные из кэша, если они есть
    redis_key = get_redis_key_for_user(db_user.id)
    redis_client.delete(redis_key)

    return {"id": db_user.id, "username": db_user.username,"name": db_user.name, "surname": db_user.surname, "email": db_user.email}

# API: Создание цели в MongoDB
@app.post("/goals/")
def create_goal(name: str, description: str, status: str):
    goal_doc = {"name": name, "description": description, "status": status}
    try:
        collection.insert_one(goal_doc)
    except:
        raise HTTPException(status_code=400, detail="Chat already exists")
    return goal_doc

# API: Создание задачи в MongoDB
collection = mongo_db['tasks']
@app.post("/tasks/")
def create_task(name: str, description: str, status: str):
    task_doc = {"name": name, "description": description, "status": status}
    try:
        collection.insert_one(task_doc)
    except:
        raise HTTPException(status_code=400, detail="Chat already exists")
    return task_doc