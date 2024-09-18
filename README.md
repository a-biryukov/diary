  Приложение 'Личный дневник' - позволяет делать записи, просматривать, редактировать, удалять их после прохождения регистрации и авторизациию 
---
**Технологии**

+ Python
+ Django
+ PostgreSQL
+ Redis
+ Docker
+ Docker-compose
___
**Как запустить:**
+ Клонировать репозиторий
+ Заполнить файл .env-sample и переименовать его в .env
+ Для запуска на хостинге в config/settings.py добавить IP-адрес в ALLOWED_HOSTS
  
  **Запуск через Docker:**
  + Установить docker и docker-compose
  + Собрать образы и запустить контейнеры командой:
    + docker-compose up -d —build

  **Запуск вручную**:
  + Добавить виртуальное окружение
    + команда для venv: python -m venv env
    + команда для poetry: poetry init
  + Установить зависимости
    + команда для venv: pip install -r requirements.txt
    + команда для poetry: poetry install
  + Создайте и примените мигации
    + python manage.py migrate 
  + Установите Redis и запустите командой
  + Запустить сервер
    +python manage.py runserver
---
