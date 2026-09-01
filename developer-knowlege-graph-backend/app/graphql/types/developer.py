import strawberry
from strawberry.types import Info
from sqlalchemy import select

from app.models.project import Project
from app.models.skill import Skill
from app.models.user import User
from app.models.user_skill import UserSkill
from app.models.project_skill import ProjectSkill
from app.graphql.utils import maybe_await


# ----------------------------------Types---------------------------------------------------------

@strawberry.type
class SkillType:
    id: int
    name: str
    description: str | None
    proficiency: int


@strawberry.type
class TechnologyType:
    id: int
    name: str
    description: str | None


@strawberry.type
class ProjectType:
    id: int
    name: str
    description: str | None
    status: str

    @strawberry.field
    async def technologies(
        self,
        info: Info,
    ) -> list[TechnologyType]:

        technologies = await (
            info.context.technology_loader.load(self.id)
        )

        return [
            TechnologyType(
                id=technology.id,
                name=technology.name,
                description=technology.description,
            )
            for technology in technologies
        ]

    @strawberry.field
    async def skills(
        self,
        info: Info,
    ) -> list[SkillType]:

        skills = await (
            info.context.skill_loader.load(self.id)
        )

        return [
            SkillType(
                id=skill.id,
                name=skill.name,
                description=skill.description,
                proficiency=0,
            )
            for skill in skills
        ]


        

@strawberry.type
class DeveloperType:
    id: int
    username: str
    email: str
    bio: str | None

    @strawberry.field
    async def skills(self, info: Info) -> list[SkillType]:
        db = info.context.db
        statement = (
            select(Skill, UserSkill.proficiency)
            .join(UserSkill, UserSkill.skill_id == Skill.id)
            .where(UserSkill.user_id == self.id)
        )
        result = await maybe_await(db.execute(statement))
        rows = result.all()
        return [
            SkillType(
                id=skill.id,
                name=skill.name,
                description=skill.description,
                proficiency=proficiency,
            )
            for skill, proficiency in rows
        ]

    @strawberry.field
    async def projects(self, info: Info) -> list[ProjectType]:
        db = info.context.db
        statement = select(Project).where(Project.owner_id == self.id)
        result = await maybe_await(db.scalars(statement))
        projects = result.all()

        return [
            ProjectType(id = project.id, name=project.name, description=project.description, status=project.status,)
            for project in projects
        ]


@strawberry.type
class DeveloperQuery:

    @strawberry.field
    async def developer(self, info: Info, id: int) -> DeveloperType | None:
        db = info.context.db
        user = await maybe_await(db.get(User, id))

        if user is None:
            return None

        return DeveloperType(id=user.id, username=user.username, email=user.email, bio=user.bio)

