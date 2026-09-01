from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.project_technology import ProjectTechnology
    from app.models.technology_category import TechnologyCategory


class Technology(Base):
    __tablename__ = "technologies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=Text)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("technology_categories.id", ondelete="RESTRICT"), nullable=False)

    category: Mapped["TechnologyCategory"] = relationship(
        back_populates="technologies",
    )

    project_technologies: Mapped[list["ProjectTechnology"]] = relationship(
        back_populates="technology",
    )