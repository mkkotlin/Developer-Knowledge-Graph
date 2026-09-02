from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.developer_repository import (
    DeveloperRepository,
)
from app.graphql.errors import ValidationError


class DeveloperService:

    def __init__(self, db: AsyncSession):
        self.repository = DeveloperRepository(db)

    async def get_developer(
        self,
        developer_id: int,
    ) -> User | None:

        return await self.repository.find_by_id(
            developer_id
        )

    async def find_developers_by_skill(
        self,
        skill_name: str,
        min_proficiency: int | None = None,
    ) -> list[User]:

        if not skill_name.strip():
            return []

        return await self.repository.find_by_skill(
            skill_name.strip(),
            min_proficiency,
        )

    async def list_developers(self) -> list[User]:
        return await self.repository.list_all()

    async def search(
        self,
        first: int,
        after_id: int | None = None,
        skills: list[str] | None = None,
        technologies: list[str] | None = None,
        min_proficiency: int | None = None,
    ) -> list[User]:

        if first < 1 or first > 100:
            raise ValidationError(
                "first must be between 1 and 100"
            )

        if min_proficiency is not None:
            if not 1 <= min_proficiency <= 5:
                raise ValidationError(
                    "minProficiency must be between 1 and 5"
                )

        return await self.repository.search(
            first=first,
            after_id=after_id,
            skills=skills,
            technologies=technologies,
            min_proficiency=min_proficiency,
        )




