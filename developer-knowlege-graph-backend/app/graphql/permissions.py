from sqlalchemy.ext.asyncio import AsyncSession

from app.graphql.errors import (
    AuthorizationError,
    NotFoundError,
)
from app.models.project import Project
from app.graphql.utils import maybe_await


async def require_project_owner(
    db: AsyncSession,
    user_id: int,
    project_id: int,
) -> Project:

    project = await maybe_await(db.get(Project, project_id))

    if project is None:
        raise NotFoundError("Project not found")

    if project.owner_id != user_id:
        raise AuthorizationError("You do not own this project")

    return project

