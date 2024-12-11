from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session
from pymongo import MongoClient, ASCENDING
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Generator
import os

# Конфигурация базы данных PostgreSQL
DATABASE_URL = "postgresql://stud:Zaq123edc@127.0.0.1:47292/t_db"

# Инициализация PostgreSQL
engine = create_engine(DATABASE_URL)
SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Инициализация MongoDB
MONGO_URL = "mongodb://localhost:27017"
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["t_db"]
collection = mongo_db["users"]

# Инициализация FastAPI
app = FastAPI()

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Модель пользователя в PostgreSQL
class User(Base):
    __tablename__ = "users"  # Добавлено tablename
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    hashed_password = Column(String)

# Модель чата в PostgreSQL
class Goal(Base):
   __tablename__ = "goals"  # Добавлено tablename
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, unique=True)
   description = Column(String)
   status = Column(String)
   tasks = relationship("Task", secondary="goal_tasks")

class Task(Base):
   __tablename__ = "tasks"  # Добавлено tablename
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, unique=True)
   description = Column(String)
   status = Column(String)
   goals = relationship("Goal", secondary="goal_tasks")

# Таблица связи пользователей и чатов
goal_tasks = Table(
    "goal_tasks", Base.metadata,
    Column("goal_id", Integer, ForeignKey("goals.id")),
    Column("task_id", Integer, ForeignKey("tasks.id"))
)

# Зависимость для сессии PostgreSQL
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MongoDB: Индексы
collection.create_index([("name", ASCENDING)], unique=True)

# Схемы Pydantic для запросов
class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str

class GoalCreate(BaseModel):
    id: int
    name: str
    description: str
    status: str

class TaskCreate(BaseModel):
    id: int
    name: str
    description: str
    status: str

# API: Создание нового пользователя
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# API: Поиск пользователя по фамилии и имени
@app.get("/users/{surname},{name}")
def get_user_by_name(surname: str, name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.surname == surname, User.name == name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# API: Поиск пользователя по логину
@app.get("/users/{username}")
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# API: Создание цели
collection = mongo_db['goals']
@app.post("/goals/")
def create_goal(goal: GoalCreate):
    goal_doc = {"name": goal.name, "description": goal.description, "status": goal.status}
    try:
        collection.insert_one(goal_doc)
    except:
        raise HTTPException(status_code=400, detail="Chat already exists")
    return goal_doc

# API: Создание новой задачи
collection = mongo_db['tasks']
@app.post("/tasks/")
def create_task(task: TaskCreate):
    task_doc = {"name": task.name, "description": task.description, "status": task.status}
    try:
        collection.insert_one(task_doc)
    except:
        raise HTTPException(status_code=400, detail="Chat already exists")
    return task_doc
