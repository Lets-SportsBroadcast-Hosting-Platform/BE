<<<<<<< HEAD
import pymysql
from database.connection import Settings, conn
from sqlalchemy.orm import Session
=======
from database.connection import Settings, conn

>>>>>>> 225624dc07f5e2c506438cd54e0b50fc1062df98

# Settings 클래스를 인스턴스화 해서 .env 값을 가져온다.
settings = Settings()

# SQLAlchemy를 사용하는 경우
<<<<<<< HEAD
DB_URL = f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PWD}@{settings.DATABASE_HOST}:{3306}/{settings.DATABASE_NAME}"
_engine = conn(DB_URL)


def get_db():
=======
DB_URL = f"mysql+aiomysql://{settings.DATABASE_USER}:{settings.DATABASE_PWD}@{settings.DATABASE_HOST}:{3306}/{settings.DATABASE_NAME}"
_engine = conn(DB_URL)


async def get_db():
>>>>>>> 225624dc07f5e2c506438cd54e0b50fc1062df98
    db = _engine.sessionmaker()
    try:
        yield db
    finally:
<<<<<<< HEAD
        db.close()
=======
        await db.close()
>>>>>>> 225624dc07f5e2c506438cd54e0b50fc1062df98


# pymysql 을 사용하는 경우
# conn = pymysql.connect(
#     host=settings.DATABASE_HOST,
#     user=settings.DATABASE_USER,
#     password=settings.DATABASE_PWD,
#     db=settings.DATABASE_NAME,
#     host=3306,
#     charset="utf8",
# )
