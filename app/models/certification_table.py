from datetime import datetime

from models import Base
from pydantic import BaseModel
from sqlalchemy import func, DateTime, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


# Certification 테이블
class CertificationModel(Base):
    __tablename__ = "Certification"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    certification_number: Mapped[str] = mapped_column(nullable=False)

