from datetime import datetime
from typing import Optional

from models import Base
from pydantic import BaseModel, EmailStr
from sqlalchemy import func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


# User 테이블 CQRS : Create
class UserModel(Base):
    __tablename__ = "User"

    id: Mapped[str] = mapped_column(primary_key=True, nullable=False)  # type: ignore
    name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    birthyear: Mapped[int] = mapped_column(nullable=False)
    area: Mapped[str] = mapped_column(nullable=False)
    alarm: Mapped[bool] = mapped_column(nullable=False)
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True, onupdate=func.now())
    delete_state: Mapped[bool] = mapped_column(nullable=False, default=False)
# 인증 테이블 CQRS : Create
class AuthModel(Base):
    __tablename__ = "Auth"

    token: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    provider: Mapped[str] = mapped_column(nullable=False)
    create_time: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())


# User 테이블 CQRS : Read
class userInfo_server2client(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    birthyear: Optional[str] = None
    area: Optional[str] = None

    def __init__(self, user_instance: UserModel, **kwargs):
        super().__init__(**kwargs)
        self.name = user_instance.name
        self.gender = user_instance.gender
        self.birthyear = user_instance.birthyear
        self.area = user_instance.area


# 로그인 인증 반환
class ssologin_client2server(BaseModel):
    access_token: str
    state: str | None = None
    provider: str


# 로그인 토큰 응답
class authlogin_client2server(BaseModel):
    jwt_token: Optional[str]


# 로그인 인증한 후 클라이언트로 보낼때 모델
class login_result_server2client(authlogin_client2server):
    userInfo: Optional[dict] = None

    def __init__(self, instance: UserModel, **kwargs):
        super().__init__(**kwargs)
        self.userInfo = userInfo_server2client(user_instance=instance).model_dump()
