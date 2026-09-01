from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.technology import Technology


class ProjectTechnology(Base):
    __tablename__ = "project_technologies"

    __table_args__ = ( UniqueConstraint("project_id", "technology_id", name="uq_project_technology"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    technology_id: Mapped[int] = mapped_column(ForeignKey("technologies.id", ondelete="RESTRICT"), nullable=False, index=True)
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    usage_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    project: Mapped["Project"] = relationship(
        back_populates="project_technologies",
    )

    technology: Mapped["Technology"] = relationship(
        back_populates="project_technologies",
    )