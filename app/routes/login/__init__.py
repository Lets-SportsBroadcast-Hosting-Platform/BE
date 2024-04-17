from fastapi import APIRouter
from fastapi.routing import APIRoute

from models.user_table import TokenResponse
from routes.login.route import google_auth_login

login_routers = APIRouter(tags=["Login"])

google_login_route = APIRoute(
    path="/google", endpoint=google_auth_login, methods=["POST"], response_model=TokenResponse
)

login_routers.routes.append(google_login_route)
