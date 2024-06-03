from fastapi.routing import APIRoute
from routes.user.api import search_local


#호스팅 읽기 - 사업자번호로 비교 호스팅 리스트(Read)
user_search_local_route = APIRoute(path="/search-local", endpoint=search_local, methods=["GET"])