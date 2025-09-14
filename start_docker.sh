#!/bin/bash

# Скрипт для запуска push_analytic в Docker

echo "Запуск push_analytic (порт 7777)..."

# Создаем .env файл если его нет
if [ ! -f .env ]; then
    echo "Создание .env файла из env.example..."
    cp env.example .env
fi

# Останавливаем существующие контейнеры
echo "Остановка существующих контейнеров..."
docker-compose down

# Собираем и запускаем контейнеры
echo "Сборка и запуск контейнеров..."
docker-compose up --build -d

# Ждем запуска базы данных
echo "Ожидание запуска сервисов..."
sleep 10

# Инициализируем базу данных
echo "Инициализация базы данных..."
docker-compose exec push_analytic python init_database.py

echo "push_analytic запущен на порту 7777"
echo "Nginx доступен на порту 7778"
echo "API доступно по адресу: http://188.244.115.175:7778"
