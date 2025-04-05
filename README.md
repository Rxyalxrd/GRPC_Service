# Демо проект FastAPI-gRPC

Этот проект демонстрирует интеграцию `FastAPI` с `gRPC` для обработки запросов, а также использование `Pydantic` для валидации настроек. Проект включает настройки сервера, обработку `gRPC`-запросов и взаимодействие с клиентом.

## Стек технологий

- **Python 3.10-3.13+**
- **FastAPI** — для создания `API`.
- **gRPC** — для реализации `RPC`.
- **Pydantic** — для валидации настроек с помощью `Pydantic Settings`.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/grpc_test.git
    cd grpc_test
    
    ```

2. Установите зависимости:

    Используйте `poetry` для установки зависимостей:

    ```bash
    poetry install

    ```

3. Заполните `.env` как указано в `.env.example`

## Запуск
    ### Запуск `gRPC` сервера
        - Для запуска, выполните:
            ```bash
            make grpc-server
            ```
    ### Запуск `FastAPI` приложения
        - Чтобы запустить, выполните:
            ```bash
            make run
            ```

`FastAPI` будет доступен по адресу: `http://127.0.0.1:8000`.

## Как это работает
    1. `gRPC` сервер: Сервер `gRPC` прослушивает порт `50051` и предоставляет метод `healthz`, который возвращает статус сервера.

    2. `FastAPI`: Приложение FastAPI использует gRPC клиент для запроса статуса с сервера `gRPC` через `HTTP`-метод `/healthz`.

    3. `Pydantic Settings`: Используется для загрузки настроек из `.env` файла, таких как параметры для `FastAPI` и `gRPC`.
