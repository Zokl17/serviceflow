# ServiceFlow

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Django](https://img.shields.io/badge/Django-6.1-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

Веб-сервис для оформления и управления заявками на выездное обслуживание.

Собственный pet-проект на **Django + PostgreSQL**, в котором реализован базовый сценарий работы с заявкой: от создания клиентом до назначения исполнителя и отслеживания статусов.

## Возможности

- создание заявки клиентом через веб-форму;
- категории услуг и неисправностей;
- данные клиента и адрес выезда;
- выбор даты и временного интервала;
- автоматическая генерация номера заявки;
- назначение исполнителя;
- статусы заявок;
- история изменения статусов;
- административная панель;
- хранение данных в PostgreSQL;
- Docker Compose для локальной базы данных;
- адаптивный веб-интерфейс.

## Технологии

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Infrastructure:** Docker, Docker Compose
- **Frontend:** Django Templates, HTML, CSS
- **Tools:** Git

## Структура проекта

```text
serviceflow/
├── catalog/        # категории и неисправности
├── orders/         # заявки, формы и клиентская часть
├── workers/        # исполнители
├── config/         # настройки Django
├── docker-compose.yml
├── requirements.txt
└── manage.py
