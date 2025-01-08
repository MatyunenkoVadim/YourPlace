"""
Этот модуль предоставляет функции для хеширования паролей и проверки их корректности.

Функции:
- hash_password: Хеширует пароль с использованием bcrypt.
- validate_password: Проверяет, соответствует ли введенный пароль хешу.

Зависимости:
- Использует библиотеку bcrypt для хеширования и проверки паролей.

Контекст:
Этот файл является частью системы безопасности и используется для управления
паролями пользователей, обеспечивая их безопасное хранение и проверку.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Хеширует пароль с использованием bcrypt.

    Параметры:
    - password: Пароль, который нужно захешировать.

    Возвращает:
    - Захешированный пароль в виде байтов.
    """
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    """
    Проверяет, соответствует ли введенный пароль хешу.

    Параметры:
    - password: Пароль, который нужно проверить.
    - hashed_password: Хеш пароля, с которым нужно сравнить.

    Возвращает:
    - True, если пароль соответствует хешу, иначе False.
    """
    return bcrypt.checkpw(
        password.encode(),
        hashed_password=hashed_password,
    )
