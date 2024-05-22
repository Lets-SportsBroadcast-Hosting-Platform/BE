from fastapi.routing import APIRoute
from models.store_table import storeData
from routes.host.api import auth_business_num, insert_store, read_store, searchlist

# 사업자 번호 조회 (헤더에 사업자번호)
auth_bussiness_num_route = APIRoute(
    path="/business_num", endpoint=auth_business_num, methods=["GET"]
)

# 주소나 가게 조회
search_store_route = APIRoute(
    path="/search", endpoint=searchlist, methods=["GET"], response_model=storeData
)

# 가게 등록
store_insert_route = APIRoute(path="/insertstore", endpoint=insert_store, methods=["POST"])

# 가게 조회
store_read_route = APIRoute(path="/readstore", endpoint=read_store, methods=["GET"])
