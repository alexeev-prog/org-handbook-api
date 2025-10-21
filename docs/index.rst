.. orghandbookapi documentation master file, created by
   sphinx-quickstart on Tue Oct 21 23:07:47 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

orghandbookapi documentation
============================

.. toctree::
   :maxdepth: 4
   :caption: Содержание:

   orghandbookapi

org-handbook-api
================

REST API справочника организаций

**Документация** » https://alexeev-prog.github.io/org-handbook-api/

**Содержание:**
- :ref:`приступая-к-работе`
- :ref:`модели`
- :ref:`маршруты`
- :ref:`разработка`
- `Документация <https://alexeev-prog.github.io/org-handbook-api/>`_
- `Лицензия <https://github.com/alexeev-prog/org-handbook-api/blob/main/LICENSE>`_

.. image:: https://raw.githubusercontent.com/alexeev-prog/org-handbook-api/refs/heads/main/docs/pallet-0.png

Org-Handbook-API - это RESTful API для справочника организаций со следующим функционалом:

1. Модель Организации, Здания и Деятельность
2. Аутентификация через статичный токен
3. CRUD методы для работы с моделями

**Технологии:**

+------------------+-----------------------------------+
| Компонент       | Технологии                       |
+==================+===================================+
| Фреймворк       | FastAPI, Pydantic, SQLAlchemy 2.0|
+------------------+-----------------------------------+
| База данных     | PostgreSQL + SQLAlchemy Async    |
+------------------+-----------------------------------+
| DI контейнер    | Dishka                           |
+------------------+-----------------------------------+
| Миграции        | Alembic                          |
+------------------+-----------------------------------+
| Контейнеризация | Docker, Docker Compose           |
+------------------+-----------------------------------+
| CI/CD           | GitHub Actions                   |
+------------------+-----------------------------------+
| Документация    | Sphinx, Swagger UI               |
+------------------+-----------------------------------+

.. _приступая-к-работе:

Быстрый старт
-------------

**Предварительные требования:**

- Docker & Docker Compose
- Git

**Установка и запуск:**

1. **Клонирование репозитория**

   .. code-block:: bash

      git clone https://github.com/alexeev-prog/org-handbook-api.git
      cd org-handbook-api

2. **Запуск приложения**

   .. code-block:: bash

      docker-compose up -d

3. **Проверка работоспособности**

   .. code-block:: bash

      curl -H "X-API-Key: secret-static-api-key" http://localhost:8000/api/v1/organizations/

.. _модели:

Модели
------

**Организация (Organization)**

.. code-block:: json

   {
       "id": 1,
       "legal_name": "ООО Рога и Копыта",
       "building_id": 1,
       "phonenumbers": ["2-222-222", "3-333-333"],
       "activities": [1, 2]
   }

**Здание (Building)**

.. code-block:: json

   {
       "id": 1,
       "address": "г. Москва, ул. Ленина 1, офис 3",
       "latitude": 55.7558,
       "longitude": 37.6173
   }

**Деятельность (Activity)** - древовидная структура

.. code-block:: json

   {
       "id": 1,
       "name": "Еда",
       "parent_id": null,
       "level": 0,
       "children": [
           {
               "id": 2,
               "name": "Мясная продукция",
               "parent_id": 1,
               "level": 1
           }
       ]
   }

.. _маршруты:

Маршруты
--------

**Организации**

+----------+------------------------------------+----------------------------+
| Метод    | Endpoint                           | Описание                   |
+==========+====================================+============================+
| GET      | /api/v1/organizations/             | Список организаций         |
+----------+------------------------------------+----------------------------+
| GET      | /api/v1/organizations/{id}         | Организация по ID          |
+----------+------------------------------------+----------------------------+
| POST     | /api/v1/organizations/             | Создание организации       |
+----------+------------------------------------+----------------------------+
| PUT      | /api/v1/organizations/{id}         | Обновление организации     |
+----------+------------------------------------+----------------------------+
| DELETE   | /api/v1/organizations/{id}         | Удаление организации       |
+----------+------------------------------------+----------------------------+

**Расширенный поиск**

+----------+--------------------------------------------------+-----------------------------------------+
| Метод    | Endpoint                                         | Параметры                               |
+==========+==================================================+=========================================+
| GET      | /api/v1/organizations/building/{building_id}    | Организации в здании                    |
+----------+--------------------------------------------------+-----------------------------------------+
| GET      | /api/v1/organizations/activity/{activity_id}     | Организации по виду деятельности       |
+----------+--------------------------------------------------+-----------------------------------------+
| GET      | /api/v1/organizations/search/name?name=...       | Поиск по названию                       |
+----------+--------------------------------------------------+-----------------------------------------+
| GET      | /api/v1/organizations/search/radius?lat=...      | Геопоиск в радиусе                      |
+----------+--------------------------------------------------+-----------------------------------------+
| GET      | /api/v1/organizations/search/area?min_lat=...    | Поиск в прямоугольной области           |
+----------+--------------------------------------------------+-----------------------------------------+

**Аутентификация**

Все запросы требуют заголовок:

.. code-block:: http

   X-API-Key: secret-static-api-key

.. _разработка:

Разработка
----------

**Локальная установка**

1. **Установка зависимостей**

   .. code-block:: bash

      pip install uv
      uv sync

2. **Настройка окружения**

   .. code-block:: bash

      # Отредактируйте конфигурационный файл orghandbookapi.toml

3. **Запуск миграций**

   .. code-block:: bash

      alembic upgrade head

4. **Запуск сервера**

   .. code-block:: bash

      uvicorn orghandbookapi.app:app --reload

**Запуск тестов**

.. code-block:: bash

   pytest tests/ -v

Лицензия и поддержка
--------------------

Данный проект лицензирован под **GNU GPL 3** - просмотрите файл лицензии `LICENSE <https://github.com/alexeev-prog/configdoctor/blob/main/LICENSE>`_.

Для коммерческого или прочих вариантов использования напишите на почту `alexeev.dev@mail.ru <mailto:alexeev.dev@mail.ru>`.

**Ссылки:**
- `Документация <https://alexeev-prog.github.io/configdoctor>`_
- `Сообщить об ошибке <https://github.com/alexeev-prog/configdoctor/issues>`_

---
REST API справочника организаций

Copyright © 2025 Alexeev Bronislav.
