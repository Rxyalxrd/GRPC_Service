# Демо проект FastAPI-gRPC

---

Этот проект демонстрирует интеграцию `FastAPI` с `gRPC` для обработки запросов, а также использование `Pydantic` для валидации настроек. Проект включает настройки сервера, обработку `gRPC`-запросов и взаимодействие с клиентом.

---

## Стек технологий

- **Python 3.10-3.13+**
- **FastAPI** — для создания `API`.
- **gRPC** — для реализации `RPC`.
- **Pydantic** — для валидации настроек с помощью `Pydantic Settings`.
- **SQLALchemy** - для ORM моделей
- **PostgreSQL** - База данных

---

## Струкртура проекта
    
    ├── protos
    └── src
        ├── alembic
        │   └── versions
        └── app
            └── internal
                ├── api
                │   └── v1
                ├── auth
                ├── core
                ├── models
                ├── schemas
                ├── servicer
                └── stubs

## Установка

1. Клонируйте репозиторий:

    ```bash
    git@github.com:Rxyalxrd/GRPC_Service.git
    cd GRPC_Service
    
    ```

2. Установите зависимости:

    Используйте `poetry` для установки зависимостей:

    ```bash
    poetry install

    ```

3. Заполните `.env` как указано в `.env.example`

---

## Запуск
### Запуск `FastAPI` приложения
    - Чтобы запустить, выполните:
        ```bash
        make run
        ```

`FastAPI` будет доступен по адресу: `http://127.0.0.1:8000`.

---


---

