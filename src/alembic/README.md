# Миграции с помощью Alembic

---

## 1. Инициализировать Alembic в проекте(должены использовать асинхронный шаблон)

  - ```bash
    poetry run alembic init --template async alembic
    ```

## 2. В `alembic/` создать `versions`

  ### 2.1 При первом запуске указать нулевое состояние базы

    - ```bash
      poetry run alembic stamp head
      ```

  ### 2.2 Создать миграции, если внесены изменения в `/models`

    - ```bash
      poetry run alembic revision --autogenerate -m "Your commit"
      ```

## 3. Применить миграции

  - ```bash
    poetry run alembic upgrade head
    ```