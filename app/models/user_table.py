from typing import Optional

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


# Pydantic 사용자 모델 정의
class UserCreate(BaseModel):
    user_id: Optional[int]
    email: Optional[EmailStr]
    name: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    birth: Optional[str]


class TokenCreate(BaseModel):
    hash: Optional[str]
    user_id: Optional[int]
    provider: Optional[str]


class TokenResponse(BaseModel):
    access_token: Optional[str] = None
    jwt_token: Optional[str] = None
    # token_type: Optional[str]


# SQLModel 사용자 모델 정의
class User(SQLModel, table=True):
    user_id: Optional[int] = Field(primary_key=True)
    email: Optional[EmailStr]
    name: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    birth: Optional[str]


class LoginToken(SQLModel, table=True):
    hash: Optional[str] = Field(primary_key=True)
    user_id: Optional[int]
    provider: Optional[str]
