from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skill import Skill
from app.models.user import User
from app.models.user_skill import UserSkill
from app.models.project import Project
from app.models.project_technology import ProjectTechnology
from app.models.technology import Technology
from app.graphql.utils import maybe_await


class DeveloperRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(
        self,
        developer_id: int,
    ) -> User | None:

        return await maybe_await(
            self.db.get(
                User,
                developer_id,
            )
        )

    async def find_by_skill(
        self,
        skill_name: str,
        min_proficiency: int | None = None,
    ) -> list[User]:

        statement = (
            select(User)
            .join(UserSkill)
            .join(Skill)
            .where(
                Skill.name.ilike(skill_name),
            )
        )

        if hasattr(User, "is_active"):
            statement = statement.where(User.is_active.is_(True))

        if min_proficiency is not None:
            statement = statement.where(
                UserSkill.proficiency >= min_proficiency
            )

        result = await maybe_await(self.db.execute(statement))

        return result.scalars().unique().all()

    async def list_all(self) -> list[User]:
        statement = select(User)
        if hasattr(User, "is_active"):
            statement = statement.where(User.is_active.is_(True))
        result = await maybe_await(self.db.execute(statement))
        return result.scalars().unique().all()

    async def search(
        self,
        first: int,
        after_id: int | None = None,
        skills: list[str] | None = None,
        technologies: list[str] | None = None,
        min_proficiency: int | None = None,
    ) -> list[User]:

        statement = (
            select(User)
        )
        if hasattr(User, "is_active"):
            statement = statement.where(
                User.is_active.is_(True)
            )

        if skills:
            statement = (
                statement
                .join(UserSkill)
                .join(Skill)
                .where(
                    Skill.name.in_(skills)
                )
            )

            if min_proficiency is not None:
                statement = statement.where(
                    UserSkill.proficiency >= min_proficiency
                )

        if technologies:
            statement = (
                statement
                .join(Project)
                .join(ProjectTechnology)
                .join(Technology)
                .where(
                    Technology.name.in_(technologies)
                )
            )

        if after_id is not None:
            statement = statement.where(
                User.id > after_id
            )

        statement = (
            statement
            .order_by(User.id)
            .limit(first + 1)
        )

        result = await maybe_await(self.db.execute(statement))

        return result.scalars().unique().all()




