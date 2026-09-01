from collections import defaultdict

from sqlalchemy import select
from strawberry.dataloader import DataLoader

from app.db.database import SessionLocal
from app.models.project_technology import ProjectTechnology
from app.models.technology import Technology


async def load_technologies(project_ids: list[int]) -> list[list[Technology]]:

    with SessionLocal() as db:
        statement = (
            select(ProjectTechnology.project_id, Technology)
            .join(Technology, Technology.id == ProjectTechnology.technology_id)
            .where(ProjectTechnology.project_id.in_(project_ids))
        )
        rows = db.execute(statement).all()
    grouped: dict[int, list[Technology]] = defaultdict(list)

    for project_id, technology in rows:
        grouped[project_id].append(technology)

    return[ grouped.get(project_id, []) for project_id in project_ids]
technology_loader = DataLoader(load_fn=load_technologies,)