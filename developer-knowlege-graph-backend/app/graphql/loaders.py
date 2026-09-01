from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader

from app.models.project_skill import ProjectSkill
from app.models.project_technology import ProjectTechnology
from app.models.skill import Skill
from app.models.technology import Technology
from app.graphql.utils import maybe_await


async def load_project_technologies(
    project_ids: list[int],
    db: AsyncSession,
) -> list[list[Technology]]:

    statement = (
        select(
            ProjectTechnology.project_id,
            Technology,
        )
        .join(
            Technology,
            Technology.id == ProjectTechnology.technology_id,
        )
        .where(
            ProjectTechnology.project_id.in_(project_ids)
        )
    )

    result = await maybe_await(db.execute(statement))

    grouped: dict[int, list[Technology]] = defaultdict(list)

    for project_id, technology in result.all():
        grouped[project_id].append(technology)

    return [
        grouped.get(project_id, [])
        for project_id in project_ids
    ]


async def load_project_skills(
    project_ids: list[int],
    db: AsyncSession,
) -> list[list[Skill]]:

    statement = (
        select(
            ProjectSkill.project_id,
            Skill,
        )
        .join(
            Skill,
            Skill.id == ProjectSkill.skill_id,
        )
        .where(
            ProjectSkill.project_id.in_(project_ids)
        )
    )

    result = await maybe_await(db.execute(statement))

    grouped: dict[int, list[Skill]] = defaultdict(list)

    for project_id, skill in result.all():
        grouped[project_id].append(skill)

    return [
        grouped.get(project_id, [])
        for project_id in project_ids
    ]

