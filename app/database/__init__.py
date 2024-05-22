from database.connection import Settings, conn_db, conn_S3

# Settings 클래스를 인스턴스화 해서 .env 값을 가져온다.
settings = Settings()

# SQLAlchemy를 사용하는 경우
DB_URL = f"mysql+aiomysql://{settings.DATABASE_USER}:{settings.DATABASE_PWD}@{settings.DATABASE_HOST}:{3306}/{settings.DATABASE_NAME}"
_engine = conn_db(DB_URL)
_s3 = conn_S3(
    settings.AWS_ACCESS_KEY_ID,
    settings.AWS_SECRET_ACCESS_KEY,
    settings.REGION_NAME,
    settings.BUCKET_NAME,
)


async def get_db():
    db = _engine.sessionmaker()
    try:
        yield db
    finally:
        await db.close()


# pymysql 을 사용하는 경우
# conn = pymysql.connect(
#     host=settings.DATABASE_HOST,
#     user=settings.DATABASE_USER,
#     password=settings.DATABASE_PWD,
#     db=settings.DATABASE_NAME,
#     host=3306,
#     charset="utf8",
# )
