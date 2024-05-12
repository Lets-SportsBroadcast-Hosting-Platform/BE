from datetime import datetime
from typing import Optional

from models import Base
from pydantic import BaseModel, EmailStr
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


# User 테이블
class UserModel(Base):
    __tablename__ = "User"

    user_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)  # type: ignore
    mail: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    birthyear: Mapped[str] = mapped_column(nullable=False)
    birthday: Mapped[str] = mapped_column(nullable=False)
    region: Mapped[str] = mapped_column(nullable=False)
    alarm: Mapped[bool] = mapped_column(nullable=False)
    join_date: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())


# 인증 테이블
class AuthModel(Base):
    __tablename__ = "Auth"

    token: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    provider: Mapped[str] = mapped_column(nullable=False)
    create_time: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())


class userInfo_server2client(BaseModel):
    name: Optional[str] = None
    mail: Optional[EmailStr] = None
    gender: Optional[str] = None
    birthyear: Optional[str] = None
    birthday: Optional[str] = None
    region: Optional[str] = None

    def __init__(self, user_instance: UserModel, **kwargs):
        super().__init__(**kwargs)
        self.name = user_instance.name
        self.mail = user_instance.mail
        self.gender = user_instance.gender
        self.birthyear = user_instance.birthyear
        self.birthday = user_instance.birthday
        self.region = user_instance.region


class ssologin_client2server(BaseModel):
    access_token: str
    state: str | None = None
    provider: str


class authlogin_client2server(BaseModel):
    jwt_token: Optional[str]


# 로그인 인증한 후 클라이언트로 보낼때 모델
class login_result_server2client(authlogin_client2server):
    userInfo: Optional[dict] = None

    def __init__(self, instance: UserModel, **kwargs):
        super().__init__(**kwargs)
        self.userInfo = userInfo_server2client(user_instance=instance).model_dump()
