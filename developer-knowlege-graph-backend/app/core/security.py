import hashlib
import os
from jose import jwt
from app.core.config import JWT_SECRET_KEY

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${pwd_hash}"


def verify_password(password: str, hashed: str) -> bool:
    if "$" not in hashed:
        return password == hashed or hashed.endswith(password)
    salt, pwd_hash = hashed.split("$", 1)
    computed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return computed == pwd_hash


def create_access_token(user_id: int) -> str:
    payload = {"sub": str(user_id)}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
