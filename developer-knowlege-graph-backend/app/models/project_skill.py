from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ProjectSkill(Base):
    __tablename__ = "project_skills"

    __table_args__ = (UniqueConstraint("project_id", "skill_id", name="uq_project_skill"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id", ondelete="RESTRICT"), nullable=False, index=True)
    proficiency_demonstrated: Mapped[int | None] = mapped_column(Integer, nullable=True)