workspace "ЛидерТаск" "Архитектура ЛидерТаск для управления пользователями и списками целей" {

    !identifiers hierarchical

    model {
        User = person "Исполнитель"{
        }
        
        LtSystem = softwareSystem "ЛидерТаск" {
            UserDB = container "User Database"{
            description "База данных для хранения пользователей"
            technology "PostgreSQL"
            tags "Database"
            }
            GoalDB = container "Goal Database" {
            description "База данных для хранения целей"
            technology "PostgreSQL"
            tags "Database"
            }
            TaskDB = container "Task Database" {
            description "База данных для хранения задач"
            technology "PostgreSQL"
            tags "Database"
            -> GoalDB "Привязка задач к целям" "PostgreSQL"
            }
            WebApp = container "Web Application" {
                technology "React, JavaScript"
                description "Веб-приложение для взаимодействия с пользователями"
            }

            APIGateway = container "API Gateway" {
                technology "Spring Cloud Gateway"
                description "API-шлюз для маршрутизации запросов"
            }
             UserService = container "User Service" {
                technology "Java Spring Boot"
                description "Сервис работы с пользователями"
                -> APIGateway "Запросы на работу с пользователями" "HTTPS"
                -> UserDB "Хранение информации о пользователях" "JDBC"
            }
            GoalService = container "Goal Service" {
                technology "Java Spring Boot"
                description "Сервис работы с целями"
                -> APIGateway "Запросы на работу с целями" "HTTPS"
                -> GoalDB "Хранение информации о целях" "JDBC"
            }
            TaskService = container "Task Service" {
                technology "Java Spring Boot"
                description "Сервис работы с задачами"
                -> APIGateway "Запросы на работу с задачами" "HTTPS"
                -> TaskDB "Хранение информации о задачах" "JDBC"
            }
        }

        User -> LtSystem.WebApp "Взаимодействие яерез веб-приложение"
        LtSystem.WebApp -> LtSystem.APIGateway "Передача запросов" "HTTPS"
    }

    views {
        systemContext LtSystem {
            include *
            autolayout lr
        }
        
        container LtSystem {
            include *
            autolayout lr
        }
        
        dynamic LtSystem "CreateUser" "Создание нового пользователя" {
            User -> LtSystem.WebApp "Создание нового пользователя"
            LtSystem.WebApp -> LtSystem.APIGateway "POST /user"
            LtSystem.APIGateway -> LtSystem.UserService "Создает запись в базе данных"
            LtSystem.UserService -> LtSystem.UserDB "INSERT INTO users"
            autolayout lr
        }

        dynamic LtSystem "FindUserByLogin" "Поиск пользователя по логину" {
            User -> LtSystem.WebApp "Поиск пользователя по логину"
            LtSystem.WebApp -> LtSystem.APIGateway "GET /user?login={login}"
            LtSystem.APIGateway -> LtSystem.UserService "Получает пользователя по логину"
            LtSystem.UserService -> LtSystem.UserDB "SELECT * FROM users WHERE login={login}"
            autolayout lr
        }

        dynamic LtSystem "FindUserByName" "Поиск пользователя по маске имени и фамилии" {
            User -> LtSystem.WebApp "Поиск пользователя по имени и фамилии"
            LtSystem.WebApp -> LtSystem.APIGateway "GET /user?name={name}&surname={surname}"
            LtSystem.APIGateway -> LtSystem.UserService "Получает пользователя по имени и фамилии"
            LtSystem.UserService -> LtSystem.UserDB "SELECT * FROM users WHERE name LIKE {name} AND surname LIKE {surname}"
            autolayout lr
        }
        
         dynamic LtSystem "CreateGoal" "Создание новой цели" {
            User -> LtSystem.WebApp "Создание новой цели"
            LtSystem.WebApp -> LtSystem.APIGateway "POST /goal"
            LtSystem.APIGateway -> LtSystem.GoalService "Создает запись в базе данных"
            LtSystem.GoalService -> LtSystem.GoalDB "INSERT INTO goals"
            autolayout lr
        }
        
        dynamic LtSystem "GetGoals" "Получение списка целей" {
            User -> LtSystem.WebApp "Запрашивает список целей"
            LtSystem.WebApp -> LtSystem.APIGateway "GET /goals"
            LtSystem.APIGateway -> LtSystem.GoalService "Возвращает список целей"
            LtSystem.GoalService -> LtSystem.GoalDB "SELECT * FROM goals"
            autolayout lr
        }
        
        dynamic LtSystem "CreateTaskForGoal" "Создание новой задачи на пути к цели" {
            User -> LtSystem.WebApp "Создание новой задачи"
            LtSystem.WebApp -> LtSystem.APIGateway "POST /task"
            LtSystem.APIGateway -> LtSystem.TaskService "Создает запись в базе данных"
            LtSystem.TaskService -> LtSystem.TaskDB "INSERT INTO tasks"
            LtSystem.TaskDB -> LtSystem.GoalDB "Привязка новой задачи к цели"
            autolayout lr
        }
        
        dynamic LtSystem "GetAllTasksForGoal" " Получение всех задач цели" {
            User -> LtSystem.WebApp "Запрашивает список задач"
            LtSystem.WebApp -> LtSystem.APIGateway "GET /tasks"
            LtSystem.APIGateway -> LtSystem.TaskService "Возвращает список задач"
            LtSystem.TaskService -> LtSystem.TaskDB "SELECT * FROM tasks WHERE goal_id={goal_id}"
            autolayout lr
        }
        
        dynamic LtSystem "ChangeStatusForTask" " Изменение статуса задачи в цели"{
            User -> LtSystem.WebApp "Поиск и изменение задачи в нужной цели"
            LtSystem.WebApp -> LtSystem.APIGateway "GET /task?goal_id={goal_id}"
            LtSystem.APIGateway  -> LtSystem.TaskService "Возвращает задачу, привязанную к цели"
            LtSystem.TaskService -> LtSystem.TaskDB "INSERT INTO tasks WHERE goal_id={goal_id}"
            autolayout lr
        }
        theme default
    }

}
