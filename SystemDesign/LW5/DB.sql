CREATE DATABASE t_db;

-- Подключение к базе данных
\c t_db;

-- Создание таблицы пользователей с полями для хранения хешированного пароля
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(50) UNIQUE NOT NULL,
    surname VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индекс для быстрого поиска по имени пользователя
CREATE INDEX IF NOT EXISTS idx_username ON users(username);

-- Создание таблицы для целей
CREATE TABLE IF NOT EXISTS goals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Создание таблицы для задач
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    goal_id INT
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Индекс для ускорения поиска принадлежности задач к цели по ID цели
CREATE INDEX IF NOT EXISTS idx_goal_id ON tasks(goal_id);

-- Тестовые данные
INSERT INTO users (username, name, surname, email, hashed_password) VALUES 
('admin', 'Denis', 'Soldatov', 'test@mail.ru', 'iyr567idfYLFLYI&RTIYflrtudotdluyf^')
ON CONFLICT DO NOTHING;

INSERT INTO goals (name, description, status) VALUES ('Main Goal', 'Example', 'In Progress') ON CONFLICT DO NOTHING;
