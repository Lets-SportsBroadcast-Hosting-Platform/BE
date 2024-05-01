from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.login import login_routers

# FastAPI
app = FastAPI()

# CORS
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# 라우터 등록
app.include_router(login_routers, prefix="/login")


if __name__ == "__main__":
    print("hello let's")

    # import uvicorn
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
