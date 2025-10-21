# org-handbook-api

<div align="center">
  <p align="center">
    REST API справочника организаций
    <br />
    <a href="https://alexeev-prog.github.io/org-handbook-api/"><strong>Документация »</strong></a>
    <br />
    <br />
    <a href="#быстрый-старт">Быстрый старт</a>
    ·
    <a href="#модели">Модели</a>
    ·
    <a href="#маршруты">Маршруты</a>
    ·
    <a href="#разработка">Разработка</a>
    .
    <a href="https://alexeev-prog.github.io/org-handbook-api/">Документация</a>
    ·
    <a href="https://github.com/alexeev-prog/org-handbook-api/blob/main/LICENSE">Лицензия</a>
  </p>
</div>
<br>
<p align="center">
    <img src="https://img.shields.io/github/languages/top/alexeev-prog/org-handbook-api?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/count/alexeev-prog/org-handbook-api?style=for-the-badge">
    <img src="https://img.shields.io/github/license/alexeev-prog/org-handbook-api?style=for-the-badge">
    <img src="https://img.shields.io/github/stars/alexeev-prog/org-handbook-api?style=for-the-badge">
    <img src="https://img.shields.io/github/issues/alexeev-prog/org-handbook-api?style=for-the-badge">
    <img src="https://img.shields.io/github/last-commit/alexeev-prog/org-handbook-api?style=for-the-badge">
    <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/alexeev-prog/org-handbook-api?style=for-the-badge">
</p>
<p align="center">
    <img src="https://raw.githubusercontent.com/alexeev-prog/org-handbook-api/refs/heads/main/docs/pallet-0.png">
</p>

Org-Handbook-API - это RESTful API для справочника организаций со следующим функционалом:

1. Модель Организации, Здания и Деятельность;
2. Аутентификация через статичный токен;
3. CRUD методы для работы с моделями;


| Компонент | Технологии |
|-----------|------------|
| **Фреймворк** | FastAPI, Pydantic, SQLAlchemy 2.0 |
| **База данных** | PostgreSQL + SQLAlchemy Async |
| **DI контейнер** | Dishka |
| **Миграции** | Alembic |
| **Контейнеризация** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Документация** | Sphinx, Swagger UI |

## Быстрый старт

### Предварительные требования

- Docker & Docker Compose
- Git

### Установка и запуск

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/alexeev-prog/org-handbook-api.git
   cd org-handbook-api
   ```

2. **Запуск приложения**
   ```bash
   docker-compose up --build -d
   ```

3. **Проверка работоспособности**
   ```bash
   curl -H "X-API-Key: secret-static-api-key" http://localhost:8000/api/v1/organizations/
   ```

## Модели

### Организация (`Organization`)
```python
{
    "id": 1,
    "legal_name": "ООО Рога и Копыта",
    "building_id": 1,
    "phonenumbers": ["2-222-222", "3-333-333"],
    "activities": [1, 2]
}
```

### Здание (`Building`)
```python
{
    "id": 1,
    "address": "г. Москва, ул. Ленина 1, офис 3",
    "latitude": 55.7558,
    "longitude": 37.6173
}
```

### Деятельность (`Activity`) - древовидная структура
```python
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
```

<p align="right">(<a href="#readme-top">наверх</a>)</p>

## Маршруты

### Организации
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/v1/organizations/` | Список организаций |
| `GET` | `/api/v1/organizations/{id}` | Организация по ID |
| `POST` | `/api/v1/organizations/` | Создание организации |
| `PUT` | `/api/v1/organizations/{id}` | Обновление организации |
| `DELETE` | `/api/v1/organizations/{id}` | Удаление организации |

### Расширенный поиск
| Метод | Endpoint | Параметры |
|-------|----------|-----------|
| `GET` | `/api/v1/organizations/building/{building_id}` | Организации в здании |
| `GET` | `/api/v1/organizations/activity/{activity_id}` | Организации по виду деятельности |
| `GET` | `/api/v1/organizations/search/name?name=...` | Поиск по названию |
| `GET` | `/api/v1/organizations/search/radius?lat=...&lon=...&radius_km=...` | Геопоиск в радиусе |
| `GET` | `/api/v1/organizations/search/area?min_lat=...&max_lat=...&min_lon=...&max_lon=...` | Поиск в прямоугольной области |

### Аутентификация
Все запросы требуют заголовок:
```http
X-API-Key: secret-static-api-key
```

<p align="right">(<a href="#readme-top">наверх</a>)</p>

## Разработка

### Локальная установка

1. **Установка зависимостей**
   ```bash
   pip install uv
   uv sync
   ```

2. **Настройка окружения**
   ```bash
   # Отредактируйте конфигурационный файл orghandbookapi.toml
   ```

3. **Запуск миграций**
   ```bash
   alembic upgrade head
   ```

4. **Запуск сервера**
   ```bash
   uvicorn orghandbookapi.app:app --reload
   ```

### Запуск тестов
```bash
pytest tests/ -v
```

<p align="right">(<a href="#readme-top">наверх</a>)</p>

## Лицензия и поддержка

Данный проект лицензирован под **GNU GPL 3** - просмотрите файл лицензии [LICENSE](https://github.com/alexeev-prog/configdoctor/blob/main/LICENSE). Для коммерческого или прочих вариантов использования напишите на почту [alexeev.dev@mail.ru](mailto:alexeev.dev@mail.ru).

[Документация](https://alexeev-prog.github.io/configdoctor) |
[Отправить фидбек об ошибке или улучшении](https://github.com/alexeev-prog/configdoctor/issues)

<p align="right">(<a href="#readme-top">наверх</a>)</p>

---
REST API справочника организаций

Copyright © 2025 Alexeev Bronislav.




