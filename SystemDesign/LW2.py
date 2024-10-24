from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Секретный ключ для подписи JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Модель данных для пользователя
class User(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    email: str
    hashed_password: str

# Модель цели
class Goal(BaseModel):
    id: int
    name: str
    description: str
    status: str

# Модель задачи
class Task(BaseModel):
    id: int
    name: str
    description: str
    goal_id: int
    status: bool

# Временные базы данных
users_db = []
goals_db = []
tasks_db = []

# Псевдо-база данных пользователей
client_db = {
    "admin":  "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # hashed "secret"
}

# Настройка паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройка OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Зависимости для получения текущего пользователя
async def get_current_client(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        else:
            return username
    except JWTError:
        raise credentials_exception
    
# Создание и проверка JWT токенов
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Аутентификация пользователя по JWT токену
async def get_current_client(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# Маршрут для получения токена
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    password_check = False
    if form_data.username in client_db:
        password = client_db[form_data.username]
        if pwd_context.verify(form_data.password, password):
            password_check = True

    if password_check:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Создание исполнителя
@app.post("/users", response_model=User)
def create_user(user: User, current_user: str = Depends(get_current_client)):
    for u in users_db:
        if u.id == user.id:
            raise HTTPException(status_code=404, detail="User already exists")
    users_db.append(user)
    return user

# Поиск пользователя по логину
@app.get("/users/{username}", response_model=User)
def get_by_login(username: str, current_user: str = Depends(get_current_client)):
    for user in users_db:
        if user.username == username:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Поиск пользователя по маске имени и фамилии
@app.get("/users", response_model=List[User])
def get_by_name(name: str, surname: str, current_user: str = Depends(get_current_client)):
    matching_users = [
        user
        for user in users_db
        if name.lower() in user.name.lower()
        and surname.lower() in user.surname.lower()
    ]
    return matching_users

# Создание новой цели
@app.post("/goals", response_model=Goal)
def create_goal(goal: Goal, current_user: str = Depends(get_current_client)):
    goals_db.append(goal)
    return goal

# Получение списка целей
@app.get("/goals", response_model=List[Goal])
def get_goals():
    return goals_db

# Создание новой задачи на пути к цели
@app.post("/tasks", response_model=Task)
def create_task_for_goal(task: Task, current_user: str = Depends(get_current_client)):
    tasks_db.append(task)
    return task

# Получение всех задач цели
@app.get("/tasks", response_model=List[Task])
def get_all_tasks_for_goal(task: Task, current_user: str = Depends(get_current_client)):
    all_for_goal = [
        t
    for t in tasks_db
    if t.goal_id == task.goal_id
    ]
    return all_for_goal

# Изменение статуса задачи в цели
@app.put("/tasks/{id}", response_model=Task)
def change_task_status(id: int, updated_status: Task, current_user: str = Depends(get_current_client)):
    for index, t in enumerate(tasks_db):
        if t.id == id:
            tasks_db[index] = updated_status
    return updated_status

# Запуск сервера
# http://localhost:8000/openapi.json swagger
# http://localhost:8000/docs портал документации

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)