# Vault Client

## Обзор

::: src.adapters.vault_client.VaultClient
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Основные возможности

- Безопасное хранение и извлечение секретов
- Поддержка KV Secrets Engine версии 2
- Гибкая настройка аутентификации через токен
- Обработка ошибок и логирование
- Автоматическое разрешение путей к секретам

## Примеры использования

### Инициализация клиента

```python
from src.adapters.vault_client import VaultClient

# Инициализация с явным указанием параметров
vault = VaultClient(
    addr='http://localhost:8200',
    token_file='/path/to/vault/token'
)

# Или с использованием переменных окружения
# export VAULT_ADDR='http://localhost:8200'
# export VAULT_TOKEN_FILE='/path/to/vault/token'
vault = VaultClient()
```

### Работа с секретами

```python
# Получение всего секрета
secret = await vault.get_secret('eebook/users/database')
# {'username': 'admin', 'password': 's3cr3t'}

# Получение конкретного значения из секрета
db_password = await vault.get_secret('eebook/users/database', 'password')
# 's3cr3t'
```

## Обработка ошибок

В модуле определены следующие исключения:

::: src.adapters.exceptions.vault_exceptions
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Требования к окружению

- Python 3.8+
- Пакет `hvac`
- Настроенный и доступный сервер HashiCorp Vault
- Действующий токен доступа с необходимыми разрешениями

## Примечания

- Для работы требуется корректно настроенный сервер Vault
- Токен доступа должен иметь необходимые права на чтение запрашиваемых секретов
- По умолчанию используется KV Secrets Engine версии 2
- Все операции логируются для последующего аудита

## См. также

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [hvac Documentation](https://hvac.readthedocs.io/)
