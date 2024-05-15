from fastapi import FastAPI
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from routes import host_routers, hosting_routers, login_routers
from starlette.exceptions import HTTPException as StarletteHTTPException

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


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


# 라우터 등록
app.include_router(login_routers, prefix="/login")
app.include_router(host_routers, prefix="/host")
app.include_router(hosting_routers, prefix="/hosting")


@app.get("/")
async def index():
    return "Hello this is Let's Server"


@app.get("/hello")
async def hello():
    return "Hello"


if __name__ == "__main__":
    print("hello let's")

    # import uvicorn

    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
