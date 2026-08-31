from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class UserSkill(Base):
    __tablename__ = "user_skills"
    __table_args__ = ( UniqueConstraint("user_id", "skill_id", name="uq_user_skill"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)