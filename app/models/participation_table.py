from datetime import datetime

from models import Base
from pydantic import BaseModel
from sqlalchemy import func, DateTime, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


# Participation 테이블
class ParticipationModel(Base):
    __tablename__ = "Participation"

    participant_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    hosting_id: Mapped[str] = mapped_column(nullable=False)
    id: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    area: Mapped[str] = mapped_column(nullable=False)
    introduce: Mapped[str] = mapped_column(nullable=False)
    age_range: Mapped[str] = mapped_column(nullable=False)
    hosting_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    delete_state: Mapped[bool] = mapped_column(nullable=False, default=False)

