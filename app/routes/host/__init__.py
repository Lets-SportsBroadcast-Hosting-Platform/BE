from fastapi.routing import APIRoute
from models.store_table import Add_New_StoreInfo, storeData
from routes.host.route import auth_bussiness_num, searchlist, storeInsert

auth_bussiness_num_route = APIRoute(
    path="/bussiness_num", endpoint=auth_bussiness_num, methods=["POST"]
)

search_store_route = APIRoute(
    path="/search", endpoint=searchlist, methods=["POST"], response_model=storeData
)

new_store_insert_route = APIRoute(
    path="/newstore", endpoint=storeInsert, methods=["POST"], response_model=Add_New_StoreInfo
)
