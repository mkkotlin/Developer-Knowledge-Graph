import strawberry
from strawberry.types import Info
from sqlalchemy import select

from app.graphql.types.developer import SkillType
from app.models.project import Project
from app.models.project_skill import ProjectSkill
from app.models.skill import Skill
from app.graphql.utils import maybe_await


@strawberry.type
class ProjectSkillMutation:

    @strawberry.mutation
    async def add_skill_to_project(
        self,
        info: Info,
        project_id: int,
        skill_id: int,
        proficiency_demonstrated: int | None = None,
    ) -> SkillType:

        if proficiency_demonstrated is not None:
            if not 1 <= proficiency_demonstrated <= 5:
                raise ValueError(
                    "Proficiency must be between 1 and 5"
                )

        db = info.context.db
        project = await maybe_await(db.get(Project, project_id))

        if project is None:
            raise ValueError("Project not found")

        skill = await maybe_await(db.get(Skill, skill_id))

        if skill is None:
            raise ValueError("Skill not found")

        res = await maybe_await(db.scalars(
            select(ProjectSkill).where(
                ProjectSkill.project_id == project_id,
                ProjectSkill.skill_id == skill_id,
            )
        ))
        existing = res.first()

        if existing:
            existing.proficiency_demonstrated = (
                proficiency_demonstrated
            )
        else:
            project_skill = ProjectSkill(
                project_id=project_id,
                skill_id=skill_id,
                proficiency_demonstrated=(
                    proficiency_demonstrated
                ),
            )

            db.add(project_skill)

        await maybe_await(db.commit())

        return SkillType(
            id=skill.id,
            name=skill.name,
            description=skill.description,
            proficiency=(
                proficiency_demonstrated or 0
            ),
        )

