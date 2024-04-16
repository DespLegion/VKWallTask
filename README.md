# VkWallTask README
Создание ВК бота для проведения опросов на стенке (под постом) и динамического изменения шапки группы на основе результатов опросов
----------
## Пример шапки

![](https://i.ibb.co/PjC8yyN/Vk-wall-cover.jpg)

___________
## Требования

1) `Python 3.10` и старше
2) `Redis` - в качестве брокера сообщений для `Celery`
3) `PostgreSQL`

___________

## Конфигурация и запуск

1) Необходимо клонировать репозиторий
2) Развернуть виртуальное окружение python
3) Находясь в виртуальном окружении установить зависимости проекта
    1) `pip install -r requirements.txt`
4) Сконфигурировать переменные окружения
    1) Переименовать файла `.env_example` в `.env`
    2) Заполнить `.env` файл 
5) Подготовить Django к работе
    1) Подготовить миграции: `python manage.py makemigrations`
    2) Произвести миграции: `python manage.py migrate`
    3) Произвести сбор статических файлов `python manage.py collectstatic`
    4) Создать супер-пользователя `python manage.py createsuperuser`
6) Запустить сервер Django 
    1) `python manage.py runserver`
7) Сконфигурировать проект в административном интерфейсе `Django`
    1) Добавить новый `Bot Config`
    2) Добавить новый `Testings Config`
    3) Добавить вопросы `Questions`
    4) Добавить новую обложку для шапки группы `Covers`
    5) Добавить новую периодическую задачу `periodictask`
       1) Добавить новый интервал `intervalschedule` (или `Crontab` запись)
       2) Добавить новую задачу `Update cover task` используя созданный ранее интервал
8) Запустить в отдельном потоке `VK Бота`
    1) `python manage.py run_bot`
9) Запустить в отдельном потоке `celery worker`
    1) `celery -A djangoVKWall worker -E -l INFO --pool=solo` (`--pool=solo` - если запускаете под `Windows`)
10) Запустить в отдельном потоке `celery beat`
    1) `celery -A djangoVKWall beat -l INFO`
11) При необходимости (если необходимо в реальном времени отслеживать выполнение задач `Celery`) запустить в отдельном потоке `Celery Flower`
    1) `celery -A djangoVKWall.celery.app flower`
12) Done :)

___________


CREATED AT 11.04.2024 BY Desp IN PyCharm
