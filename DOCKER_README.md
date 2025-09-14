# Push Analytic - Docker Setup

Сервис обработки и подбора пуш-уведомлений на порту 7777.

## Архитектура

- **push_analytic** (порт 7777) - Flask API для аналитики и генерации пуш-уведомлений
- **push_analytic_nginx** (порт 7778) - Nginx прокси для API
- **База данных** - Удаленная Neon PostgreSQL

## Порты

- `7777` - Flask приложение push_analytic
- `7778` - Nginx для push_analytic
- `5555` - Frontend (отдельный проект)
- `6666` - Backend API (отдельный проект)

## Быстрый запуск

### Windows
```bash
start_docker.bat
```

### Linux/Mac
```bash
chmod +x start_docker.sh
./start_docker.sh
```

### Ручной запуск
```bash
# Создать .env файл
cp env.example .env

# Запустить контейнеры
docker-compose up --build -d

# Инициализировать базу данных
docker-compose exec push_analytic python init_database.py
```

## API Endpoints

- `POST /analyze` - Анализ одного клиента и генерация пуш-уведомления
- `POST /analyze/all` - Анализ всех клиентов
- `GET /health` - Проверка здоровья сервиса
- `GET /` - Веб-интерфейс с аналитикой

## Пример запроса

```bash
curl -X POST http://188.244.115.175:7778/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "client_code": "12345",
    "name": "Рамазан",
    "status": "Зарплатный клиент",
    "avg_monthly_balance_KZT": 240000,
    "transactions": [
      {"date": "2025-08-10", "category": "Такси", "amount": 27400, "currency": "KZT"}
    ],
    "transfers": [
      {"date": "2025-08-01", "type": "salary_in", "direction": "in", "amount": 320000, "currency": "KZT"}
    ]
  }'
```

## Управление

```bash
# Остановить
docker-compose down

# Перезапустить
docker-compose restart

# Посмотреть логи
docker-compose logs -f push_analytic

# Войти в контейнер
docker-compose exec push_analytic bash
```

## Переменные окружения

Скопируйте `env.example` в `.env` и настройте:

```env
# Flask настройки
FLASK_APP=src/api/notification_api.py
FLASK_ENV=production
FLASK_PORT=5000

# Подключение к Neon DB
PGHOST=ep-little-tree-agjwpa12-pooler.c-2.eu-central-1.aws.neon.tech
PGDATABASE=neondb
PGUSER=neondb_owner
PGPASSWORD=npg_PJH1k4RZXAux
PGSSLMODE=require
PGCHANNELBINDING=require
```

## Структура проекта

```
push_analytic/
├── src/
│   ├── api/           # REST API (notification_api.py)
│   ├── products/      # Сценарии продуктов
│   ├── notifications/ # Генерация уведомлений
│   └── config/        # Конфигурация БД
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
├── run_app.py         # Скрипт запуска
├── init_database.py   # Инициализация БД
├── env.example        # Пример переменных окружения
└── requirements.txt   # Зависимости Python
```
