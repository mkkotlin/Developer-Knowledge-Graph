import strawberry
from strawberry.types import Info
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.models.skill import Skill
from app.graphql.types.developer import SkillType
from app.models.user_skill import UserSkill
from app.models.user import User
from app.graphql.utils import maybe_await

@strawberry.type
class SkillMutation:

    @strawberry.mutation
    async def create_skill(self, info: Info, name: str, description: str | None = None) -> SkillType:
        db = info.context.db
        skill = Skill(name = name, description = description)
        db.add(skill)

        try:
            await maybe_await(db.commit())
            await maybe_await(db.refresh(skill))
        except IntegrityError:
            await maybe_await(db.rollback())
            raise ValueError("Skill already exists")
        return SkillType(id = skill.id, name = skill.name, description = skill.description, proficiency = 0)

    @strawberry.mutation
    async def add_skill_to_developer(self, info: Info, developer_id: int, skill_id: int, proficiency: int) -> SkillType:
        if not 1 <= proficiency <= 5:
            raise ValueError("Proficiency must be between 1 and 5")

        db = info.context.db
        user = await maybe_await(db.get(User, developer_id))
        if user is None:
            raise ValueError("Developer not found")

        skill = await maybe_await(db.get(Skill, skill_id))
        if skill is None:
            raise ValueError("Skill not found")

        res = await maybe_await(db.scalars(select(UserSkill).where(UserSkill.user_id == developer_id, UserSkill.skill_id == skill_id)))
        existing = res.first()

        if existing:
            existing.proficiency = proficiency
        else:
            user_skill = UserSkill(user_id = developer_id, skill_id = skill_id, proficiency = proficiency)
            db.add(user_skill)
        await maybe_await(db.commit())

        return SkillType(id = skill.id, name= skill.name, description=skill.description, proficiency=proficiency)

