from fastapi.routing import APIRoute
from routes.user.api import (
    search_local, 
    insert_user, 
    apply_party, 
    read_partylist, 
    read_party,
    delete_party
    )


#호스팅 읽기 - 사업자번호로 비교 호스팅 리스트(Read)
user_search_local_route = APIRoute(path="/search-local", endpoint=search_local, methods=["GET"])

user_insert_route = APIRoute(path="", endpoint=insert_user, methods=["POST"])

user_apply_party_route = APIRoute(path="/party/{hosting_id}", endpoint=apply_party, methods=["POST"])

user_read_partylist_route = APIRoute(path="/party_list", endpoint = read_partylist, methods = ["GET"])

user_read_party_route = APIRoute(path="/party/{hosting_id}", endpoint=read_party, methods=["GET"])

user_delete_party_route = APIRoute(path="/party{hosting_id}", endpoint=delete_party, methods=["DELETE"])