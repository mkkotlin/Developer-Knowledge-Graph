from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader
from strawberry.fastapi import BaseContext

from app.db.database import AsyncSessionLocal
from app.graphql.auth import get_current_user_id
from app.graphql.loaders import (
    load_project_skills,
    load_project_technologies,
)


class GraphQLContext(BaseContext):
    def __init__(
        self,
        db: AsyncSession,
        current_user_id: int | None = None,
        technology_loader: DataLoader = None,
        skill_loader: DataLoader = None,
    ):
        super().__init__()
        self.db = db
        self.current_user_id = current_user_id
        self.technology_loader = technology_loader or DataLoader(
            load_fn=lambda ids: load_project_technologies(ids, db)
        )
        self.skill_loader = skill_loader or DataLoader(
            load_fn=lambda ids: load_project_skills(ids, db)
        )


async def get_context(
    request: Request = None,
) -> AsyncIterator[GraphQLContext]:

    async with AsyncSessionLocal() as db:

        technology_loader = DataLoader(
            load_fn=lambda ids: load_project_technologies(ids, db)
        )

        skill_loader = DataLoader(
            load_fn=lambda ids: load_project_skills(ids, db)
        )

        user_id = get_current_user_id(request) if request else None

        yield GraphQLContext(
            db=db,
            current_user_id=user_id,
            technology_loader=technology_loader,
            skill_loader=skill_loader,
        )




