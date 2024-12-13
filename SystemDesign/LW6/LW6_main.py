from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from pymongo import MongoClient
from redis import Redis
from kafka import KafkaProducer
import json
import os

# Конфигурация
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://stud:Zaq123edc@127.0.0.1:47292/t_db")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "kafka:9092")
TOPIC_NAME = "user_creation"

# PostgreSQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)


# MongoDB
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["t_db"]
collection = mongo_db["goals"]

# Redis
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)

# Kafka
producer = KafkaProducer(bootstrap_servers="kafka:9092")  # Заменено с localhost на kafka

# FastAPI
app = FastAPI()


# Зависимость для базы данных PostgreSQL
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API: Создание пользователя (Command)
@app.post("/users/")
def create_user(username: str, name: str, surname: str, email: str, password: str):
    hashed_password = "hashed_" + password  # Простая хеш-функция
    message = {"username": username,"name": name, "surname": surname, "email": email, "hashed_password": hashed_password}
    producer.send(TOPIC_NAME, message)
    return {"message": "User creation event sent to Kafka"}


# API: Получение пользователя (Query)
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    redis_key = f"user:{user_id}"
    cached_user = redis_client.get(redis_key)
    if cached_user:
        return json.loads(cached_user)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = {"id": user.id, "username": user.username, "email": user.email}
    redis_client.set(redis_key, json.dumps(user_data), ex=3600)
    return user_data


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