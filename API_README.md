# Push Analytics API

API для анализа клиентов и генерации персонализированных уведомлений.

## 🚀 Быстрый запуск

### 1. Запуск через Docker Compose

```bash
# Запуск всех сервисов
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d --build
```

### 2. Проверка статуса

```bash
# Проверка логов
docker-compose logs -f

# Проверка статуса контейнеров
docker-compose ps
```

## 📡 API Endpoints

### Базовый URL
- **Локально**: `http://localhost:7778`
- **API**: `http://localhost:7778/api/v1/analytics`

### Swagger документация
- **URL**: `http://localhost:7778/swagger/`

### Доступные эндпоинты

#### 1. Health Check
```http
GET /api/v1/analytics/health
```

**Ответ:**
```json
{
  "status": "healthy",
  "service": "push_analytics"
}
```

#### 2. Анализ клиента (лучшая рекомендация)
```http
POST /api/v1/analytics/analyze
```

**Запрос:**
```json
{
  "client_code": 1,
  "name": "Рамазан",
  "status": "Зарплатный клиент",
  "avg_monthly_balance_KZT": 240000,
  "city": "Алматы",
  "age": 30,
  "transactions": [
    {
      "date": "2025-08-10",
      "category": "Такси",
      "amount": 27400,
      "currency": "KZT"
    }
  ],
  "transfers": [
    {
      "date": "2025-08-01",
      "type": "salary_in",
      "direction": "in",
      "amount": 320000,
      "currency": "KZT"
    }
  ]
}
```

**Ответ:**
```json
{
  "client_code": 1,
  "product": "Карта для путешествий",
  "push_notification": "Привет, Рамазан! За август вы потратили 50 000 ₸ на путешествия. Оформите карту для путешествий и получите 2 000 ₸ кэшбэка!",
  "score": 0.85,
  "expected_benefit": 2000,
  "priority": "high"
}
```

#### 3. Анализ всех продуктов
```http
POST /api/v1/analytics/analyze/all
```

**Ответ:**
```json
{
  "client_code": 1,
  "recommendations": [
    {
      "product": "Карта для путешествий",
      "push_notification": "Привет, Рамазан! За август вы потратили 50 000 ₸ на путешествия. Оформите карту для путешествий и получите 2 000 ₸ кэшбэка!",
      "score": 0.85,
      "expected_benefit": 2000,
      "priority": "high"
    },
    {
      "product": "Премиальная карта",
      "push_notification": "Рамазан, ваш баланс 240 000 ₸ позволяет получить премиальную карту с кэшбэком 4 800 ₸ в месяц!",
      "score": 0.75,
      "expected_benefit": 4800,
      "priority": "medium"
    }
  ]
}
```

## 🧪 Тестирование

### Автоматические тесты
```bash
# Запуск тестового скрипта
python test_api.py
```

### Ручное тестирование с curl

#### Health Check
```bash
curl -X GET http://localhost:7778/api/v1/analytics/health
```

#### Анализ клиента
```bash
curl -X POST http://localhost:7778/api/v1/analytics/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "client_code": 1,
    "name": "Рамазан",
    "status": "Зарплатный клиент",
    "avg_monthly_balance_KZT": 240000
  }'
```

## 🐳 Docker конфигурация

### Порты
- **7777**: Flask приложение (прямой доступ)
- **7778**: Nginx (рекомендуется)

### Сервисы
- **push_analytic**: Flask приложение
- **push_analytic_nginx**: Nginx прокси

### Health Check
Контейнер Flask проверяется каждые 30 секунд через endpoint `/api/v1/analytics/health`.

## 📊 Мониторинг

### Логи
```bash
# Все логи
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f push_analytic
docker-compose logs -f push_analytic_nginx
```

### Статус контейнеров
```bash
docker-compose ps
```

## 🔧 Устранение неполадок

### Проблема: "host not found in upstream"
Это означает, что nginx пытается подключиться к Flask приложению до того, как оно запустится. Решение:
1. Убедитесь, что health check работает
2. Перезапустите контейнеры: `docker-compose restart`

### Проблема: "ImportError: cannot import name 'NotificationPipeline'"
Эта проблема исправлена. Убедитесь, что используете обновленный код.

### Проблема: API не отвечает
1. Проверьте, что контейнеры запущены: `docker-compose ps`
2. Проверьте логи: `docker-compose logs -f push_analytic`
3. Проверьте health check: `curl http://localhost:7778/api/v1/analytics/health`

## 📝 Примеры использования

### JavaScript (fetch)
```javascript
const response = await fetch('http://localhost:7778/api/v1/analytics/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    client_code: 1,
    name: "Рамазан",
    status: "Зарплатный клиент",
    avg_monthly_balance_KZT: 240000
  })
});

const data = await response.json();
console.log(data);
```

### Python (requests)
```python
import requests

response = requests.post(
    'http://localhost:7778/api/v1/analytics/analyze',
    json={
        'client_code': 1,
        'name': 'Рамазан',
        'status': 'Зарплатный клиент',
        'avg_monthly_balance_KZT': 240000
    }
)

print(response.json())
```

## 🎯 Продукты

API анализирует следующие продукты:
- Карта для путешествий
- Премиальная карта
- Кредитная карта
- Обмен валют
- Депозит Мультивалютный
- Депозит Сберегательный
- Депозит Накопительный
- Инвестиции
- Золотые слитки
- Кредит наличными
