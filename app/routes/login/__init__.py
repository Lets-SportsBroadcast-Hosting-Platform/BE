from fastapi.routing import APIRoute
from routes.login.route import login_as_token, sso

login_route = APIRoute(path="/", endpoint=sso, methods=["POST"])
login_token_route = APIRoute(path="/token", endpoint=login_as_token, methods=["POST"])
