import strawberry
from strawberry.types import Info
from sqlalchemy import select

from app.graphql.auth import require_user
from app.graphql.permissions import require_project_owner
from app.graphql.types.developer import TechnologyType
from app.models.project_technology import ProjectTechnology
from app.models.technology import Technology
from app.graphql.utils import maybe_await


@strawberry.type
class TechnologyMutation:

    @strawberry.mutation
    async def add_technology_to_project(
        self,
        info: Info,
        project_id: int,
        technology_id: int,
        version: str | None = None,
        usage_type: str | None = None,
    ) -> TechnologyType:

        user_id = require_user(info)

        db = info.context.db

        project = await require_project_owner(
            db=db,
            user_id=user_id,
            project_id=project_id,
        )

        technology = await maybe_await(db.get(Technology, technology_id))

        if technology is None:
            raise ValueError("Technology not found")

        res = await maybe_await(db.scalars(
            select(ProjectTechnology).where(
                ProjectTechnology.project_id == project_id,
                ProjectTechnology.technology_id == technology_id,
            )
        ))
        existing = res.first()

        if existing:
            existing.version = version
            existing.usage_type = usage_type
        else:
            project_technology = ProjectTechnology(
                project_id=project_id,
                technology_id=technology_id,
                version=version,
                usage_type=usage_type,
            )

            db.add(project_technology)

        await maybe_await(db.commit())

        return TechnologyType(
            id=technology.id,
            name=technology.name,
            description=technology.description,
        )


