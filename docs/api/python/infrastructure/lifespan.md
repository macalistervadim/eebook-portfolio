# Управление жизненным циклом приложения

Модуль `lifespan` предоставляет функционал для управления жизненным циклом FastAPI приложения, обеспечивая корректную инициализацию и освобождение ресурсов.

## Особенности

- Асинхронное управление жизненным циклом
- Безопасная инициализация и освобождение ресурсов
- Интеграция с системой бутстраппинга
- Обработка ошибок при старте и завершении

## Документация API

### lifespan

Асинхронный контекстный менеджер для управления жизненным циклом приложения.

::: src.infrastructure.lifespan.lifespan
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false

## Примеры использования

### Базовое использование с FastAPI

```python
from fastapi import FastAPI
from src.infrastructure.lifespan import lifespan

# Создание приложения с кастомным жизненным циклом
app = FastAPI(lifespan=lifespan)

# Определение маршрутов...
@app.get("/")
async def root():
    return {"message": "Приложение работает"}
```

### Кастомизация жизненного цикла

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructure.lifespan import lifespan as base_lifespan

@asynccontextmanager
async def custom_lifespan(app: FastAPI):
    # Дополнительная инициализация перед запуском
    print("Выполняется дополнительная инициализация...")
    
    # Использование базового жизненного цикла
    async with base_lifespan(app) as manager:
        # Код выполняется после инициализации приложения
        print("Приложение готово к работе")
        try:
            yield manager
        finally:
            # Дополнительная очистка при завершении
            print("Выполняется дополнительная очистка...")

app = FastAPI(lifespan=custom_lifespan)
```
