# Интерфейсы адаптеров

## Обзор

Модуль `interfaces` определяет контракты (интерфейсы) для взаимодействия с внешними системами. Эти интерфейсы обеспечивают гибкость и лёгкость замены реализаций без изменения кода, который их использует.

## Основные интерфейсы

### ISecretsProvider

Абстракция для работы с хранилищами секретов (например, HashiCorp Vault, AWS Secrets Manager).

::: src.adapters.interfaces.ISecretsProvider
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false

## Принципы работы

### Инверсия зависимостей

Все адаптеры зависят от абстракций (интерфейсов), а не от конкретных реализаций. Это позволяет:

- Легко заменять реализации
- Упрощать тестирование
- Снижать связанность компонентов

### Ленивая загрузка

Реализации адаптеров загружаются только при первом обращении, что ускоряет запуск приложения.

## Примеры использования

### Получение секрета

```python
from src.adapters.interfaces import ISecretsProvider

class MyService:
    def __init__(self, secrets_provider: ISecretsProvider):
        self.secrets = secrets_provider

    async def get_database_credentials(self):
        return await self.secrets.get_secret("database/prod", "credentials")
```
