from fastapi import APIRouter
from routes.host import (
    auth_bussiness_num_route,
    new_store_insert_route,
    search_store_route,
)
from routes.login import login_route, login_token_route

login_routers = APIRouter(tags=["Login"])
host_routers = APIRouter(tags=["Host"])

host_routers.routes.append(auth_bussiness_num_route)
host_routers.routes.append(search_store_route)
host_routers.routes.append(new_store_insert_route)

login_routers.routes.append(login_route)
login_routers.routes.append(login_token_route)
