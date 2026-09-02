from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.project_skill import ProjectSkill
from app.models.project_technology import ProjectTechnology
from app.models.skill import Skill
from app.models.technology import Technology
from app.graphql.utils import maybe_await


class ProjectRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(
        self,
        project_id: int,
    ) -> Project | None:

        return await maybe_await(
            self.db.get(
                Project,
                project_id,
            )
        )

    async def find_by_technology(
        self,
        technology_name: str,
    ) -> list[Project]:

        statement = (
            select(Project)
            .join(ProjectTechnology)
            .join(Technology)
            .where(
                Technology.name.ilike(
                    technology_name
                )
            )
        )

        result = await maybe_await(self.db.execute(statement))

        return result.scalars().unique().all()

    async def find_by_skill(
        self,
        skill_name: str,
    ) -> list[Project]:

        statement = (
            select(Project)
            .join(ProjectSkill)
            .join(Skill)
            .where(
                Skill.name.ilike(skill_name)
            )
        )

        result = await maybe_await(self.db.execute(statement))

        return result.scalars().unique().all()

    async def list_all(self) -> list[Project]:
        statement = select(Project)
        result = await maybe_await(self.db.execute(statement))
        return result.scalars().unique().all()

    async def list_projects(
        self,
        first: int,
        after_id: int | None = None,
    ) -> list[Project]:

        statement = (
            select(Project)
            .order_by(Project.id)
            .limit(first + 1)
        )

        if after_id is not None:
            statement = statement.where(
                Project.id > after_id
            )

        result = await maybe_await(self.db.execute(statement))

        return result.scalars().all()

    async def search(
        self,
        first: int,
        after_id: int | None = None,
        technology: str | None = None,
        skill: str | None = None,
    ) -> list[Project]:

        statement = select(Project)

        if technology:
            statement = (
                statement
                .join(ProjectTechnology)
                .join(Technology)
                .where(
                    Technology.name.ilike(technology)
                )
            )

        if skill:
            statement = (
                statement
                .join(ProjectSkill)
                .join(Skill)
                .where(
                    Skill.name.ilike(skill)
                )
            )

        if after_id is not None:
            statement = statement.where(
                Project.id > after_id
            )

        statement = (
            statement
            .order_by(Project.id)
            .limit(first + 1)
        )

        result = await maybe_await(self.db.execute(statement))

        return result.scalars().unique().all()



