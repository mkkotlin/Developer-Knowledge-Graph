import strawberry
from strawberry.types import Info
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.graphql.types.developer import DeveloperType
from app.core.security import hash_password, verify_password, create_access_token
from app.graphql.utils import maybe_await
from app.graphql.errors import ValidationError, AuthenticationError


@strawberry.type
class AuthPayload:
    token: str
    user: DeveloperType


@strawberry.type
class AuthMutation:

    @strawberry.mutation
    async def register(
        self,
        info: Info,
        username: str,
        email: str,
        password: str,
        bio: str | None = None,
    ) -> AuthPayload:
        if not username.strip() or not email.strip() or not password.strip():
            raise ValidationError("Username, email, and password are required")

        db = info.context.db
        hashed_pwd = hash_password(password)

        user = User(
            username=username.strip(),
            email=email.strip().lower(),
            password_hash=hashed_pwd,
            bio=bio,
        )

        db.add(user)

        try:
            await maybe_await(db.commit())
            await maybe_await(db.refresh(user))
        except IntegrityError:
            await maybe_await(db.rollback())
            raise ValidationError("Username or email already exists")

        token = create_access_token(user.id)

        dev_type = DeveloperType(
            id=user.id,
            username=user.username,
            email=user.email,
            bio=user.bio,
        )

        return AuthPayload(token=token, user=dev_type)

    @strawberry.mutation
    async def login(
        self,
        info: Info,
        username_or_email: str,
        password: str,
    ) -> AuthPayload:
        if not username_or_email.strip() or not password.strip():
            raise ValidationError("Username/email and password are required")

        db = info.context.db

        statement = select(User).where(
            or_(
                User.username == username_or_email.strip(),
                User.email == username_or_email.strip().lower(),
            )
        )

        result = await maybe_await(db.execute(statement))
        user = result.scalars().first()

        if user is None or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid username/email or password")

        token = create_access_token(user.id)

        dev_type = DeveloperType(
            id=user.id,
            username=user.username,
            email=user.email,
            bio=user.bio,
        )

        return AuthPayload(token=token, user=dev_type)
