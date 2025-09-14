@echo off

REM Скрипт для запуска push_analytic в Docker (Windows)

echo Запуск push_analytic (порт 7777)...

REM Создаем .env файл если его нет
if not exist .env (
    echo Создание .env файла из env.example...
    copy env.example .env
)

REM Останавливаем существующие контейнеры
echo Остановка существующих контейнеров...
docker-compose down

REM Собираем и запускаем контейнеры
echo Сборка и запуск контейнеров...
docker-compose up --build -d

REM Ждем запуска базы данных
echo Ожидание запуска сервисов...
timeout /t 10 /nobreak > nul

REM Инициализируем базу данных
echo Инициализация базы данных...
docker-compose exec push_analytic python init_database.py

echo push_analytic запущен на порту 7777
echo Nginx доступен на порту 7778
echo API доступно по адресу: http://188.244.115.175:7778

pause
