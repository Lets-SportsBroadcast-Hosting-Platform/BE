from fastapi.routing import APIRoute
from routes.hosting.api import make_hosting

# 호스팅 등록 (Create)
hosting_route = APIRoute(path="/make_hosting", endpoint=make_hosting, methods=["POST"])
