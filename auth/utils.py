from datetime import timedelta

import jwt
from win32ctypes.pywin32.pywintypes import datetime

from core.config import settings


def encode_jwt(
    payload: dict,
    secret_key: str = settings.auth_jwt.secret_key_path.read_text(),
    algorithm: str =settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
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
    algorithm: str =settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded