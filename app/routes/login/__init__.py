from fastapi import APIRouter
from fastapi.routing import APIRoute

from models.user_table import TokenResponse
from routes.login.route import kakao_auth_login

login_routers = APIRouter(tags=["Login"])

kakao_login_route = APIRoute(path="/kakao", endpoint=kakao_auth_login, methods=["POST"])
login_routers.routes.append(kakao_login_route)
