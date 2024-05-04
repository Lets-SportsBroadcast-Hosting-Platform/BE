from fastapi.routing import APIRoute
from routes.sports.route import kbo_datacrawl

kbo_route = APIRoute(path="/kbo", endpoint=kbo_datacrawl, methods=["POST"])
