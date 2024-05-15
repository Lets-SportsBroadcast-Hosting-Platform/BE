from fastapi.routing import APIRoute
from models.store_table import storeData
from routes.host.route import auth_bussiness_num, insert_store, searchlist

auth_bussiness_num_route = APIRoute(
    path="/bussiness_num", endpoint=auth_bussiness_num, methods=["POST"]
)

search_store_route = APIRoute(
    path="/search", endpoint=searchlist, methods=["POST"], response_model=storeData
)

store_insert_route = APIRoute(path="/insertstore", endpoint=insert_store, methods=["POST"])
