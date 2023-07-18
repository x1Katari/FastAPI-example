# FastAPI проект

Реализация API с использованием FastAPI Poetry Tortoise Aerich Postgres Docker

## Требования

- Docker
- docker-compose

## Запуск проекта локально

1. Склонируйте репозиторий на ваш локальный компьютер:

git clone https://github.com/x1Katari/SMIT.git

2. Перейдите в каталог проекта:

cd SMIT

3. Переименуйте файл .env.dist в .env

4. Используйте Docker Compose для сборки и запуска приложения:

docker-compose up

Сервер FastAPI работает на http://localhost:8000

Для взаимодействия с API http://localhost:8000/docs

## Примечание

Ниже приведен список реализованных конечных точек:

- POST /upload_cargo_rates Загружает тарифы на груз из файла JSON.
- GET /cargos Получает список всех грузов.
- GET /cargo/{cargo_id} Получает детали конкретного груза по его ID.
- GET /insurance_cost Возвращает (объявленную стоимость * rate) предоставленного типа груза, объявленной стоимости, и даты (%Y-%m-%d).
- GET /cargo_history/{cargo_type} Возвращает историю тарифов (%Y-%m-%d) конкретного груза
