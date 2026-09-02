import strawberry
from strawberry.types import Info
from sqlalchemy import select

from app.models.project import Project
from app.models.skill import Skill
from app.models.user import User
from app.models.user_skill import UserSkill
from app.models.project_skill import ProjectSkill
from app.models.project_technology import ProjectTechnology
from app.models.technology import Technology
from app.models.technology_category import TechnologyCategory
from app.graphql.inputs.filters import DeveloperFilter, ProjectFilter
from app.graphql.utils import maybe_await
from app.graphql.errors import ValidationError
from app.graphql.pagination import (
    DeveloperConnection,
    DeveloperEdge,
    PageInfo,
    ProjectConnection,
    ProjectEdge,
    decode_cursor,
    encode_cursor,
)
from app.services.developer_service import DeveloperService
from app.services.project_service import ProjectService






# ----------------------------------Types---------------------------------------------------------

@strawberry.type
class SkillType:
    id: int
    name: str
    description: str | None
    proficiency: int


@strawberry.type
class TechnologyCategoryType:
    id: int
    name: str
    description: str | None


@strawberry.type
class TechnologyType:
    id: int
    name: str
    description: str | None

    @strawberry.field
    async def category(
        self,
        info: Info,
    ) -> TechnologyCategoryType | None:

        db = info.context.db

        technology = await maybe_await(
            db.get(
                Technology,
                self.id,
            )
        )

        if technology is None:
            return None

        category = await maybe_await(
            db.get(
                TechnologyCategory,
                technology.category_id,
            )
        )

        if category is None:
            return None

        return TechnologyCategoryType(
            id=category.id,
            name=category.name,
            description=category.description,
        )



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
        service = info.context.developer_service
        user = await service.get_developer(id)

        if user is None:
            return None

        return DeveloperType(id=user.id, username=user.username, email=user.email, bio=user.bio)

    @strawberry.field
    async def developers(
        self,
        info: Info,
        first: int = 20,
        after: str | None = None,
        filter: DeveloperFilter | None = None,
    ) -> DeveloperConnection:

        if first < 1 or first > 100:
            raise ValidationError(
                "first must be between 1 and 100"
            )

        after_id = (
            decode_cursor(after)
            if after
            else None
        )

        service = info.context.developer_service

        users = await service.search(
            first=first,
            after_id=after_id,
            skills=(
                filter.skills
                if filter
                else None
            ),
            technologies=(
                filter.technologies
                if filter
                else None
            ),
            min_proficiency=(
                filter.min_proficiency
                if filter
                else None
            ),
        )



        has_next_page = len(users) > first

        users = users[:first]

        edges = [
            DeveloperEdge(
                cursor=encode_cursor(user.id),
                node=DeveloperType(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    bio=user.bio,
                ),
            )
            for user in users
        ]

        return DeveloperConnection(
            edges=edges,
            page_info=PageInfo(
                has_next_page=has_next_page,
                end_cursor=(
                    edges[-1].cursor
                    if edges
                    else None
                ),
            ),
        )


    @strawberry.field
    async def projects(
        self,
        info: Info,
        first: int = 20,
        after: str | None = None,
        filter: ProjectFilter | None = None,
    ) -> ProjectConnection:

        if first < 1 or first > 100:
            raise ValidationError(
                "first must be between 1 and 100"
            )

        after_id = (
            decode_cursor(after)
            if after
            else None
        )

        service = info.context.project_service

        projects = await service.search(
            first=first,
            after_id=after_id,
            technology=(
                filter.technology
                if filter
                else None
            ),
            skill=(
                filter.skill
                if filter
                else None
            ),
        )

        has_next_page = len(projects) > first

        projects = projects[:first]

        edges = [
            ProjectEdge(
                cursor=encode_cursor(project.id),
                node=ProjectType(
                    id=project.id,
                    name=project.name,
                    description=project.description,
                    status=project.status,
                ),
            )
            for project in projects
        ]

        return ProjectConnection(
            edges=edges,
            page_info=PageInfo(
                has_next_page=has_next_page,
                end_cursor=(
                    edges[-1].cursor
                    if edges
                    else None
                ),
            ),
        )







