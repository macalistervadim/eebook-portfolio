# Загрузчик настроек

Модуль `loader` предоставляет функционал для безопасной загрузки настроек и секретов из защищенного хранилища в переменные окружения приложения. Использует паттерн "Провайдер секретов" для абстракции источника данных.

## Особенности

- Гибкая система загрузки секретов через абстрактный интерфейс `ISecretsProvider`
- Поддержка различных провайдеров секретов (по умолчанию используется Vault)
- Потокобезопасная работа с переменными окружения
- Детальное логирование операций
- Обработка ошибок с конкретными типами исключений

## Документация API

### SettingsLoader

::: src.config.loader.SettingsLoader
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false

## Примеры использования

### Базовое использование с Vault по умолчанию

```python
from src.config.loader import SettingsLoader

# Создание загрузчика с провайдером по умолчанию (Vault)
loader = SettingsLoader()

# Загрузка секретов в переменные окружения
await loader.load()

# Теперь секреты доступны через os.environ
import os
print(os.environ['DATABASE_URL'])  # Пример использования загруженного секрета
```
