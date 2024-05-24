from fastapi.routing import APIRoute
from routes.mainpage.api import read_hostings


#호스팅 읽기 - 사업자번호로 비교 호스팅 리스트(Read)
mainpage_hosting_read_route = APIRoute(path="/hostings", endpoint=read_hostings, methods=["GET"])
