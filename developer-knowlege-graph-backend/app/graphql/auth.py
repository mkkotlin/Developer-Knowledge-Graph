from fastapi import Request
from jose import JWTError, jwt

from app.core.config import JWT_SECRET_KEY
from app.graphql.errors import AuthenticationError

ALGORITHM = "HS256"


def get_current_user_id(request: Request) -> int | None:
    authorization = request.headers.get("Authorization")

    if not authorization:
        return None

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise AuthenticationError("Invalid authorization header")

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise AuthenticationError("Invalid token")

        return int(user_id)

    except (JWTError, ValueError):
        raise AuthenticationError("Invalid or expired token")


def require_user(info) -> int:
    user_id = info.context.current_user_id

    if user_id is None:
        raise AuthenticationError("Authentication required")

    return user_id


