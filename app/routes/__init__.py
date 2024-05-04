from fastapi import APIRouter
from routes.login import login_route, login_token_route
from routes.sports import kbo_route

sports_routers = APIRouter(tags=["Sports"])
login_routers = APIRouter(tags=["Login"])

login_routers.routes.append(login_route)
login_routers.routes.append(login_token_route)
sports_routers.routes.append(kbo_route)
