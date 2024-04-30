from datetime import datetime

from models import Base
from pydantic import BaseModel
from sqlalchemy import func

from sqlalchemy.orm import Mapped, mapped_column



class UserModel(Base):
    __tablename__ = "User"

    user_id: Mapped[str] = mapped_column(primary_key=True,nullable=False) # type: ignore
    mail: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    birthyear: Mapped[str] = mapped_column(nullable=False)
    birthday: Mapped[str] = mapped_column(nullable=False)
    region: Mapped[str] = mapped_column(nullable=False)
    alarm: Mapped[str] = mapped_column(nullable=False)
    join_date: Mapped[datetime] = mapped_column(nullable=False,server_default=func.now())

class AuthModel(Base):
    __tablename__ = "Auth"

    token : Mapped[str] = mapped_column(primary_key=True,nullable=False)
    provider : Mapped[str] = mapped_column(nullable=False)
    create_time: Mapped[datetime] = mapped_column(nullable=False,server_default=func.now())

class TokenResponse(BaseModel):
    access_token: str = None
    login_token: str = None
    jwt_token: str = None
    state: str = None
    provider: str = None
