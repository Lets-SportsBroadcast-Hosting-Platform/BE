from fastapi.routing import APIRoute
from models.user_table import login_result_server2client, userInfo_server2client
from routes.login.route import login_as_token, sso

login_route = APIRoute(
    path="/", endpoint=sso, methods=["POST"], response_model=login_result_server2client
)
login_token_route = APIRoute(
    path="/token", endpoint=login_as_token, methods=["POST"], response_model=userInfo_server2client
)
