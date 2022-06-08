# Блог

Блог с возможностью читать и публиковать посты.

В [Техническом задании на разработку](https://github.com/emildzy3/Blog/blob/main/doc/blog_tz.md) описана цель проекта, представленно описание платформ, а также указан стек используемых технологий


## Запуск проекта 
___
1. Клонирование проекта

```
git clone https://github.com/emildzy3/Blog.git
```

2. Создание и активация виртуального окружения 

```
python3 -m venv venv && source venv/bin/activate
```
3. Создайте файл .env в корневой папке проекта , содержащий переменные окружения. Необходимые имена переменных можно взять из файла .env.example
4. Установите необходимые пакеты 
```
pip install -r requirements.txt
```
5. При использовании postgresql
```
sudo -u postgres psql
CREATE DATABASE DB;
CREATE USER user WITH PASSWORD '111';
ALTER ROLE user SET client_encoding TO 'utf8';
ALTER ROLE user SET default_transaction_isolation TO 'read committed';
ALTER ROLE user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE DB TO user;
ALTER DATABASE DB OWNER TO user;

```
6. Производим миграции 
```
python manage.py migrate 
```
7. Создаем суперпользователя 
```
python manage.py createsuperuser
```




