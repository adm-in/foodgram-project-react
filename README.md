# Проект:  Foodgram
![workflow](https://github.com/adm-in/foodgram-project-react/actions/workflows/foodgram_workflow.yaml/badge.svg)

# Описание проекта:
Приложение «Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

# Команды для запуска приложения:
1. Устанавливаем docker командой sudo apt install ```sudo apt install docker.io ``` .
2. Устанавливаем docker-compose используя [официальную](https://docs.docker.com/compose/install/) документацию.
3. Клонируем репозиторий ```https://github.com/adm-in/foodgram-project-react``` и переходим в него.
3. Далее собираем образ и запускаем docker-compose командой ```docker-compose up -d --build```.
4. Делаем миграции, загружаем ингредиенты командой ```python manage.py load_data```, создаем суперюзера.   
5. Заходим на http://127.0.0.1/admin/ и убеждаемся, что страница отображается полностью: статика подгрузилась и вы можете залогиниться под суперпользователем которого только что создали. 

- [admin](http://djangoproject.gq/admin)

### Технологии:
- [Django 3.0.5](https://www.djangoproject.com)
- [DjangoRestFramework 3.11.0](https://www.django-rest-framework.org)
- [Docker 20.10.6](https://www.docker.com)
- [Gunicorn 20.0.4](https://gunicorn.org)
- [Postgres 12.4](https://www.postgresql.org)
- [Python 3.8](https://www.python.org)
- [Nginx 1.19.3](https://nginx.org)

### Проект разработан: 
https://github.com/adm-in/
- [Licensed under the Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)