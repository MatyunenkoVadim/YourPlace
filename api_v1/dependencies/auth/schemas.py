"""
Этот модуль определяет схемы данных для работы с пользователями, включая чтение,
создание, регистрацию и обновление пользователей.

Классы:
- UserRead: Схема для чтения данных пользователя.
- UserCreate: Схема для создания нового пользователя.
- UserRegister: Схема для регистрации нового пользователя.
- UserUpdate: Схема для обновления данных пользователя.

Зависимости:
- Использует FastAPI Users для базовых схем пользователей.

Контекст:
Этот файл является частью системы управления пользователями и используется для
определения схем данных, которые используются в API для работы с пользователями.
"""

from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """
    Схема для чтения данных пользователя.

    Атрибуты:
    - is_admin: Флаг, указывающий, является ли пользователь администратором.
    - phone: Номер телефона пользователя.
    - fullname: Полное имя пользователя.
    """
    is_admin: Optional[bool] = False
    phone: str | None
    fullname: str | None


class UserCreate(schemas.BaseUserCreate):
    """
    Схема для создания нового пользователя.

    Атрибуты:
    - is_admin: Флаг, указывающий, является ли пользователь администратором.
    - phone: Номер телефона пользователя.
    - fullname: Полное имя пользователя.
    """
    is_admin: Optional[bool] = False
    phone: Optional[str] = None
    fullname: Optional[str] = None


class UserRegister(schemas.BaseUserCreate):
    """
    Схема для регистрации нового пользователя.
    """
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """
    Схема для обновления данных пользователя.

    Атрибуты:
    - is_admin: Флаг, указывающий, является ли пользователь администратором.
    - phone: Номер телефона пользователя.
    - fullname: Полное имя пользователя.
    """
    is_admin: Optional[bool] = False
    phone: Optional[str] = None
    fullname: Optional[str] = None
