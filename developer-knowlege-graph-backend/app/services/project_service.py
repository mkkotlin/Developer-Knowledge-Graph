from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.graphql.errors import ValidationError


class ProjectService:

    def __init__(self, db: AsyncSession):
        self.repository = ProjectRepository(db)

    async def get_project(
        self,
        project_id: int,
    ) -> Project | None:

        return await self.repository.find_by_id(
            project_id
        )

    async def find_by_technology(
        self,
        technology_name: str,
    ) -> list[Project]:

        if not technology_name.strip():
            return []

        return await self.repository.find_by_technology(
            technology_name.strip()
        )

    async def find_by_skill(
        self,
        skill_name: str,
    ) -> list[Project]:

        if not skill_name.strip():
            return []

        return await self.repository.find_by_skill(
            skill_name.strip()
        )

    async def list_projects(
        self,
        first: int = 20,
        after_id: int | None = None,
    ) -> list[Project]:
        return await self.repository.list_projects(
            first=first,
            after_id=after_id,
        )

    async def search(
        self,
        first: int,
        after_id: int | None = None,
        technology: str | None = None,
        skill: str | None = None,
    ) -> list[Project]:

        if first < 1 or first > 100:
            raise ValidationError(
                "first must be between 1 and 100"
            )

        return await self.repository.search(
            first=first,
            after_id=after_id,
            technology=technology,
            skill=skill,
        )



