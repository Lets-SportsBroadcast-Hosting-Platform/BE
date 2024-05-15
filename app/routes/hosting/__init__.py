from fastapi.routing import APIRoute
from routes.hosting.route import make_hosting

hosting_route = APIRoute(path="/make_hosting", endpoint=make_hosting, methods=["POST"])
