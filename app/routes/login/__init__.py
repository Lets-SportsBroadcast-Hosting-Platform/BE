from fastapi.routing import APIRoute
from models.user_table import login_result_server2client, userInfo_server2client
from routes.login.api import login_as_token, sso


# 소셜 로그인 (Create) #헤더 사용
login_route = APIRoute(
    path="/", endpoint=sso, methods=["POST"], response_model=login_result_server2client
)

# 토큰으로 로그인 (Read) # 헤더 사용
login_token_route = APIRoute(
    path="/token", endpoint=login_as_token, methods=["GET"], response_model=userInfo_server2client
)
