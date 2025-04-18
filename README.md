# Flask Superset

Сервис для визуализации данных и работы с базой данных

## Установка

### Локальный запуск
1. Создать виртуальное окружение
2. Установить зависимости: `pip install -r requirements.txt`
3. Создать файл .env с переменными окружения
4. Выполнить миграции: `alembic upgrade head`
5. Загрузить тестовые данные в базу данных из директории  `src/db`:  `python3 seed.py`
6. Запустить приложение из директории `src`: `python3 main.py`

### Запуск через Docker
1. Запустить команду `docker-compose up --build` из проекта
2. Приложение будет доступно по адресу `http://127.0.0.1:8000`

### Эндпоинты
1. `GET /api/products`: Получить список всех продуктов.
2. `POST /api/products`: Создать новый продукт.
3. `PUT /api/products/<id>`: Обновить продукт по ID.
4. `DELETE /api/products/<id>`: Удалить продукт по ID.
5. `GET /api/sales/total`: Возвращает общую сумму продаж за указанный период (параметры: start_date, end_date).
Пример запроса: `/api/sales/total?start_date=2025-02-03&end_date=2025-03-12`
6. `GET /api/sales/top-products`: Возвращает топ-N самых продаваемых товаров за указанный период (параметры: start_date, end_date, limit).
Пример запроса: `/api/sales/top-products?start_date=2025-02-03&end_date=2025-03-12&limit=10`
7. `GET /api/categories`: Возвращает список всех категорий.
8. `POST /api/categories`: Создать новую категорию.
9. `DELETE /api/categories/<id>`: Удалить категорию по ID.



