from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import conn
from routes.login import login_routers

# FastAPI
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(login_routers, prefix="/login")


# 애플리케이션이 시작 될 때 데이터베이스를 생성하도록 만듬
@app.on_event("startup")
def on_startup():
    conn()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
