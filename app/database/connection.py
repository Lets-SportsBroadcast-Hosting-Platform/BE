from typing import Optional
from pydantic_settings import BaseSettings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import  async_sessionmaker, async_session

# Setting config load
class Settings(BaseSettings):
    SECRET_KEY: Optional[str] = None
    NAVER_CLIENT_ID: Optional[str] = None
    NAVER_SECRET_KEY: Optional[str] = None
    DATABASE_HOST: Optional[str] = None
    DATABASE_USER: Optional[str] = None
    DATABASE_PWD: Optional[str] = None
    DATABASE_NAME: Optional[str] = None

    class Config:
        env_file = ".env"


# 데이터베이스 테이블 연결하는 클래스
class conn:
    def __init__(self, engine_url):
        self.engine = create_async_engine(engine_url, echo=True)
        try:
            self.engine.connect()
            print("db 연결됨")
        except:
            print("연결 안됨...")

    def sessionmaker(self):
        Session = async_sessionmaker(autocommit=False, autoflush=False, bind=self.engine,expire_on_commit=False)
        session = Session()
        return session