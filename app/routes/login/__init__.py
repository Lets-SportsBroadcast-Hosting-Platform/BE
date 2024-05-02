from fastapi import APIRouter
from fastapi.routing import APIRoute
from routes.login.route import login_as_token, sso

login_routers = APIRouter(tags=["Login"])

login_route = APIRoute(path="/", endpoint=sso, methods=["POST"])
login_token_route = APIRoute(path="/token", endpoint=login_as_token, methods=["POST"])
login_routers.routes.append(login_route)
login_routers.routes.append(login_token_route)
