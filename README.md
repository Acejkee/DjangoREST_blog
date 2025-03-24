# Django REST Blog (Пример)

Этот проект представляет собой пример блога, построенного с использованием Django REST Framework в качестве бэкенда.

## Технологии

* Backend: Django REST Framework, Python
* База данных: PostgreSQL
* Веб-сервер: Nginx
* WSGI-сервер: Gunicorn
* Очередь задач: Celery
* Брокер сообщений: Redis
* Контейнеризация: Docker, Docker Compose


## Запуск:

1. `git clone https://github.com/Acejkee/DjangoREST_blog.git`
2. `cd <your_repository_name>`
3. `cp .env.example .env` (заполните `.env`)
4. `docker-compose up -d --build`
5. `docker-compose run --rm web python manage.py migrate`
6. `docker-compose run --rm web python manage.py collectstatic --noinput`
7. `docker-compose run --rm web python manage.py createsuperuser` (опционально)

Приложение доступно по адресу: `http://localhost:8080/`

