# Зависимости сервисного слоя

Модуль `dependencies` предоставляет фабрики и провайдеры зависимостей для сервисного слоя приложения, используя паттерн внедрения зависимостей.

## Особенности

- Кэширование часто используемых зависимостей
- Асинхронная загрузка зависимостей
- Поддержка единицы работы (Unit of Work)
- Интеграция с репозиториями и сервисами
- Управление жизненным циклом зависимостей

## Документация API

### get_settings

Фабрика для получения настроек приложения с кэшированием.

::: src.service_layer.dependencies.get_settings
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_root_heading: false
      show_root_toc_entry: false
