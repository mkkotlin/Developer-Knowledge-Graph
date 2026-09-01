from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.project_skill import ProjectSkill
    from app.models.user_skill import UserSkill


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_skills: Mapped[list["UserSkill"]] = relationship(
        back_populates="skill",
    )

    project_skills: Mapped[list["ProjectSkill"]] = relationship(
        back_populates="skill",
    )