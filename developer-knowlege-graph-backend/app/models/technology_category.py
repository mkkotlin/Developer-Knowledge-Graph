from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.technology import Technology


class TechnologyCategory(Base):
    __tablename__ = "technology_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    technologies: Mapped[list["Technology"]] = relationship(
        back_populates="category",
    )