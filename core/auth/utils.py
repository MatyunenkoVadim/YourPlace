"""
Этот модуль предоставляет функции для кодирования и декодирования JWT токенов.

Функции:
- encode_jwt: Кодирует полезную нагрузку в JWT токен с заданными параметрами.
- decode_jwt: Декодирует JWT токен, используя публичный ключ и алгоритм.

Зависимости:
- Использует библиотеку PyJWT для работы с JWT токенами.
- Использует настройки из core.config для получения ключей и алгоритмов.

Контекст:
Этот файл является частью системы аутентификации и используется для создания и проверки JWT токенов.
"""

from datetime import timedelta, datetime
import jwt
from core.config import settings

def encode_jwt(
    payload: dict,
    secret_key: str = settings.auth_jwt.secret_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    """
    Кодирует полезную нагрузку в JWT токен.

    Параметры:
    - payload: Словарь с данными, которые нужно закодировать в токен.
    - secret_key: Секретный ключ для подписи токена.
    - algorithm: Алгоритм, используемый для подписи токена.
    - expire_minutes: Время жизни токена в минутах.
    - expire_timedelta: Альтернативное время жизни токена в виде timedelta.

    Возвращает:
    - Закодированный JWT токен.
    """
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode = payload.copy()
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        payload=to_encode,
        key=secret_key,
        algorithm=algorithm,
    )
    return encoded

def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    """
    Декодирует JWT токен.

    Параметры:
    - token: JWT токен, который нужно декодировать.
    - public_key: Публичный ключ для проверки подписи токена.
    - algorithm: Алгоритм, используемый для проверки подписи токена.

    Возвращает:
    - Декодированную полезную нагрузку токена.
    """
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded