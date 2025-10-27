# Инициализация приложения

## Обзор

Модуль `bootstrap` отвечает за начальную загрузку и конфигурацию приложения. Это первая точка входа, которая подготавливает все необходимые компоненты перед запуском основного функционала.

## Основные компоненты

### Функция `bootstrap()`

Центральная функция, которая инициализирует все системные компоненты в правильном порядке.

::: src.bootstrap.bootstrap
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false

## Процесс загрузки

1. **Настройка логирования**
   - Инициализирует систему логирования
   - Настраивает форматы вывода и уровни логирования

2. **Загрузка настроек**
   - Загружает конфигурацию из переменных окружения
   - Валидирует настройки с помощью Pydantic

3. **Инициализация базы данных**
   - Создаёт соединение с базой данных
   - Проверяет доступность БД

4. **Завершение инициализации**
   - Логирует успешное завершение загрузки
   - Возвращает объект настроек для использования в приложении

## Обработка ошибок

В случае возникновения ошибок на любом этапе:

- Записывает полный стектрейс в лог
- Генерирует исключение `BootstrapInitializationError`
- Завершает работу приложения с ненулевым кодом возврата

::: src.exceptions.BootstrapInitializationError
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false

## Пример использования

```python
from src.bootstrap import bootstrap

async def main():
    try:
        settings = await bootstrap()
        # Запуск приложения с загруженными настройками
        await run_app(settings)
    except BootstrapInitializationError as e:
        print(f"Ошибка инициализации: {e}")
        return 1
    return 0
```
