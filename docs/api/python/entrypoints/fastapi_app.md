# FastAPI Приложение

Модуль `fastapi_app` предоставляет фабрику для создания и настройки экземпляра FastAPI приложения. Это основная точка входа веб-сервиса.

## Особенности

- Фабричный метод для создания приложения
- Централизованная конфигурация
- Поддержка жизненного цикла приложения
- Автоматическая документация API
- Модульная структура

## Документация API

### create_app

Фабричная функция для создания и настройки экземпляра FastAPI.

::: src.entrypoints.fastapi_app.create_app
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false

## Примеры использования

### Создание приложения

```python
from src.entrypoints.fastapi_app import create_app

# Создание экземпляра приложения
app = create_app()

# Запуск с помощью uvicorn (если файл запущен напрямую)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.entrypoints.fastapi_app:app", host="0.0.0.0", port=8000, reload=True)
```

### Конфигурация приложения

При создании приложения можно передать дополнительные параметры:

```python
app = FastAPI(
    title="eebook",
    description="API учета инвестиций eebook",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)
```
