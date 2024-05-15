from fastapi import APIRouter
from routes.host import auth_bussiness_num_route, search_store_route, store_insert_route
from routes.hosting import hosting_route
from routes.login import login_route, login_token_route

login_routers = APIRouter(tags=["Login"])
host_routers = APIRouter(tags=["Host"])
hosting_routers = APIRouter(tags=["Hosting"])

host_routers.routes.append(auth_bussiness_num_route)
host_routers.routes.append(search_store_route)
host_routers.routes.append(store_insert_route)

login_routers.routes.append(login_route)
login_routers.routes.append(login_token_route)

hosting_routers.routes.append(hosting_route)
