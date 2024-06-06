from fastapi import APIRouter
from routes.crawl import esports_schedule_route, sports_schedule_route
from routes.host import (
    auth_bussiness_num_route,
    search_store_route,
    store_insert_route,
    store_read_route,
    store_update_route,
    store_delete_route,
)
from routes.hosting import (
    hosting_create_route, 
    hosting_read_tables_route, 
    hosting_read_table_route,
    hosting_delete_table_route,
    hosting_update_table_route,
    )
from routes.user import user_search_local_route, user_insert_route
from routes.login import login_route, login_token_route
from routes.mainpage import mainpage_hosting_read_route
login_routers = APIRouter(tags=["Login"])
host_routers = APIRouter(tags=["Host"])
hosting_routers = APIRouter(tags=["Hosting"])
sports_crawl_routers = APIRouter(tags=["SportsSchedule"])
mainpage_routers = APIRouter(tags=["Mainpage"])
user_routers = APIRouter(tags=['User'])

host_routers.routes.append(auth_bussiness_num_route)
host_routers.routes.append(search_store_route)
host_routers.routes.append(store_insert_route)
host_routers.routes.append(store_read_route)
host_routers.routes.append(store_update_route)
host_routers.routes.append(store_delete_route)
login_routers.routes.append(login_route)
login_routers.routes.append(login_token_route)

hosting_routers.routes.append(hosting_create_route)
hosting_routers.routes.append(hosting_read_tables_route)
hosting_routers.routes.append(hosting_read_table_route)
hosting_routers.routes.append(hosting_delete_table_route)
hosting_routers.routes.append(hosting_update_table_route)
#hosting_routers.routes.append(store_input_image)

mainpage_routers.routes.append(mainpage_hosting_read_route)

sports_crawl_routers.routes.append(esports_schedule_route)
sports_crawl_routers.routes.append(sports_schedule_route)

user_routers.routes.append(user_search_local_route)
user_routers.routes.append(user_insert_route)