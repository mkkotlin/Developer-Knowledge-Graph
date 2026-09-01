import strawberry
from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.project import Project
from app.models.project_technology import ProjectTechnology
from app.models.skill import Skill
from app.models.technology import Technology
from app.models.user import User
from app.models.user_skill import UserSkill
from app.graphql.loaders import technology_loader

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
    async def technologies(self) -> list[TechnologyType]:
        technologies = await technology_loader.load(self.id)
        return[
            TechnologyType(id = technology.id, name=technology.name, description=technology.description )
            for technology in technologies
        ]

        

@strawberry.type
class DeveloperType:
    id: int
    username: str
    email: str
    bio: str | None

    @strawberry.field
    def skills(self) -> list[SkillType]:
        with SessionLocal() as db:
            statement = (
                select(Skill, UserSkill.proficiency)
                .join(UserSkill, UserSkill.skill_id == Skill.id)
                .where(UserSkill.user_id == self.id)
            )
            rows = db.execute(statement).all()
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
    def projects(self) -> list[ProjectType]:
        with SessionLocal() as db:
            statement = (select(Project).where(Project.owner_id == self.id))
            projects = db.scalars(statement).all()

            return [
                ProjectType(id = project.id, name=project.name, description=project.description, status=project.status,)
                for project in projects
            ]


@strawberry.type
class DeveloperQuery:

    @strawberry.field
    def developer(self, id: int) -> DeveloperType | None:
        with SessionLocal() as db:
            user = db.get(User, id)

            if user is None:
                return None

            return DeveloperType(id=user.id, username=user.username, email=user.email, bio=user.bio)