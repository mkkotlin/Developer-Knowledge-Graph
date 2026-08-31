from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base



class ProjectTechnology(Base):
    __tablename__ = "project_technologies"

    __table_args__ = ( UniqueConstraint("project_id", "technology_id", name="uq_project_technology"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    technology_id: Mapped[int] = mapped_column(ForeignKey("technologies.id", ondelete="RESTRICT"), nullable=False, index=True)
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    usage_type: Mapped[str | None] = mapped_column(String(50), nullable=True)