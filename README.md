# org-handbook-api

<div align="center">
  <p align="center">
    Высокопроизводительный REST API для управления справочником организаций
    <br />
    <a href="https://alexeev-prog.github.io/org-handbook-api/"><strong>Изучите документацию »</strong></a>
    <br />
    <br />
    <a href="#быстрый-старт">Быстрый старт</a>
    ·
    <a href="#модели-данных">Модели</a>
    ·
    <a href="#api-маршруты">Маршруты</a>
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

Org-Handbook-API — это современный асинхронный RESTful API для управления справочником организаций с расширенными возможностями поиска и геолокации.

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
   curl -H "X-API-Key: secret-static-api-key" http://localhost:8000/health
   ```

4. **Доступ к документации API**
   Откройте в браузере: `http://localhost:8000/docs`

## Модели данных

### Организация (`Organization`)
```python
{
    "id": 1,
    "legal_name": "ООО Рога и Копыта",
    "building_id": 1,
    "building": {
        "id": 1,
        "address": "г. Москва, ул. Ленина 1",
        "latitude": 55.7558,
        "longitude": 37.6173
    },
    "phonenumbers": [
        {"id": 1, "phone_number": "2-222-222"},
        {"id": 2, "phone_number": "3-333-333"}
    ],
    "activities": [
        {"id": 1, "name": "Молочная продукция"},
        {"id": 2, "name": "Мясная продукция"}
    ]
}
```

### Здание (`Building`)
```python
{
    "id": 1,
    "address": "г. Москва, ул. Ленина 1, офис 3",
    "latitude": 55.7558,
    "longitude": 37.6173,
    "organizations": [
        {
            "id": 1,
            "legal_name": "ООО Рога и Копыта"
        }
    ]
}
```

### Деятельность (`Activity`) - древовидная структура
```python
{
    "id": 1,
    "name": "Еда",
    "parent_id": null,
    "level": 0,
    "parent": null,
    "children": [
        {
            "id": 2,
            "name": "Мясная продукция",
            "parent_id": 1,
            "level": 1,
            "children": []
        }
    ],
    "organizations": [
        {
            "id": 1,
            "legal_name": "ООО Рога и Копыта"
        }
    ]
}
```

## API маршруты

### Основные CRUD операции

#### Организации
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/v1/organizations/` | Получить список организаций |
| `GET` | `/api/v1/organizations/{id}` | Получить организацию по ID |
| `POST` | `/api/v1/organizations/` | Создать новую организацию |
| `PUT` | `/api/v1/organizations/{id}` | Обновить организацию |
| `DELETE` | `/api/v1/organizations/{id}` | Удалить организацию |

#### Здания
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/v1/buildings/` | Список зданий |
| `GET` | `/api/v1/buildings/{id}` | Здание по ID |
| `POST` | `/api/v1/buildings/` | Создать здание |
| `PUT` | `/api/v1/buildings/{id}` | Обновить здание |
| `DELETE` | `/api/v1/buildings/{id}` | Удалить здание |

#### Виды деятельности
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/v1/activity/` | Список видов деятельности |
| `GET` | `/api/v1/activity/{id}` | Вид деятельности по ID |
| `POST` | `/api/v1/activity/` | Создать вид деятельности |
| `PUT` | `/api/v1/activity/{id}` | Обновить вид деятельности |
| `DELETE` | `/api/v1/activity/{id}` | Удалить вид деятельности |
| `GET` | `/api/v1/activity/tree/{parent_id}` | Дерево видов деятельности |

### Расширенный поиск организаций

| Метод | Endpoint | Параметры | Описание |
|-------|----------|-----------|----------|
| `GET` | `/api/v1/organizations/building/{building_id}` | `building_id` | Организации в указанном здании |
| `GET` | `/api/v1/organizations/activity/{activity_id}` | `activity_id` | Организации по виду деятельности (включая дочерние) |
| `GET` | `/api/v1/organizations/search/name` | `name` | Поиск организаций по названию |
| `GET` | `/api/v1/organizations/search/radius` | `lat, lon, radius_km` | Геопоиск организаций в радиусе |
| `GET` | `/api/v1/organizations/search/area` | `min_lat, max_lat, min_lon, max_lon` | Поиск в прямоугольной области |

### Примеры запросов поиска

**Поиск по названию:**
```bash
curl -H "X-API-Key: secret-static-api-key" \
  "http://localhost:8000/api/v1/organizations/search/name?name=Рога"
```

**Геопоиск в радиусе:**
```bash
curl -H "X-API-Key: secret-static-api-key" \
  "http://localhost:8000/api/v1/organizations/search/radius?lat=55.7558&lon=37.6173&radius_km=5"
```

### Аутентификация
Все запросы требуют заголовок API-ключа:
```http
X-API-Key: secret-static-api-key
```

## Разработка

### Локальная установка для разработки

1. **Установка зависимостей**
   ```bash
   pip install uv
   uv sync
   ```

2. **Настройка окружения**
   Создайте или отредактируйте конфигурационный файл `orghandbookapi.toml`:
   ```toml
   [run]
   host = "127.0.0.1"
   port = 8000

   [database]
   host = "localhost"
   port = 5432
   name = "orghandbookapi"
   user = "admin"
   password = "password"

   [security]
   api_key = "your-development-api-key"
   api_key_header = "X-API-Key"

   ```

1. **Запуск миграций базы данных**
   ```bash
   alembic upgrade head
   ```

2. **Запуск сервера для разработки**
   ```bash
   uvicorn orghandbookapi.app:app --reload --host 0.0.0.0 --port 8000
   ```

### Запуск тестов
```bash
# Все тесты
pytest tests/ -v

# С покрытием кода
pytest --cov=orghandbookapi tests/

# С параллельным выполнением
pytest -n auto tests/
```

### Code Quality
```bash
# Линтинг
ruff check .

# Форматирование
ruff format .

# Типизация
mypy orghandbookapi
```

## Технологический стек

| Компонент | Технологии |
|-----------|------------|
| **Фреймворк** | FastAPI, Pydantic, SQLAlchemy 2.0 |
| **База данных** | PostgreSQL + SQLAlchemy Async |
| **Миграции** | Alembic |
| **Контейнеризация** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Документация** | Sphinx, Swagger UI, Redoc |
| **Линтеры** | Ruff, Black, isort |
| **Package Management** | UV |

## 📄 Лицензия и поддержка

Данный проект лицензирован под **GNU GPL 3** - просмотрите файл [LICENSE](https://github.com/alexeev-prog/org-handbook-api/blob/main/LICENSE) для деталей.

Для коммерческого использования или вопросов по сотрудничеству напишите на [alexeev.dev@mail.ru](mailto:alexeev.dev@mail.ru).

[Документация](https://alexeev-prog.github.io/org-handbook-api) |
[Сообщить об ошибке](https://github.com/alexeev-prog/org-handbook-api/issues) |
[Предложить улучшение](https://github.com/alexeev-prog/org-handbook-api/pulls)

---
**REST API справочника организаций**
Copyright © 2025 Alexeev Bronislav. Все права защищены.
