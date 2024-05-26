import base64
import uuid
from typing import Annotated, Any

from auth.jwt import verify_access_token
from database import get_db
from database.search_query import query_response_one
from fastapi import Depends, Header, HTTPException, Response
from models.user_table import (
    AuthModel,
    UserModel,
    authlogin_client2server,
    ssologin_client2server,
    userInfo_server2client,
)
from routes.login.api_helper import login_by_kakao, login_by_naver
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# 소셜 로그인 함수
async def sso(
    accesstoken: Annotated[str, Header(convert_underscores=False)] = None,
    state: Annotated[str | None, Header(convert_underscores=False)] = None,
    provider: Annotated[str, Header(convert_underscores=False)] = None,
    data: dict = None,
    db: AsyncSession = Depends(get_db),
):
    print(accesstoken, state, provider, data.get("region"), data.get("alarm"))
    req = ssologin_client2server(access_token=accesstoken, state=state, provider=provider)
    if req.provider.lower() == "kakao":
        return await login_by_kakao(req, data.get("region"), data.get("alarm"), db)
    elif req.provider.lower() == "naver":
        return await login_by_naver(req, data.get("region"), data.get("alarm"), db)
    else:
        raise HTTPException(status_code=200, detail=400)


# 클라이언트에서 토큰으로 로그인
async def login_as_token(
    jwToken: Annotated[str | None, Header(convert_underscores=False)] = None,
    db: AsyncSession = Depends(get_db),
) -> userInfo_server2client:
    decode_jwt_token = verify_access_token(authlogin_client2server(jwt_token=jwToken).jwt_token)
    query = select(AuthModel).where(
        AuthModel.token == decode_jwt_token.get("auth_token"),
        AuthModel.provider == decode_jwt_token.get("provider"),
    )
    if not (await query_response_one(query, db)).one_or_none():
        raise HTTPException(status_code=200, detail=400)
    user_id = uuid.UUID(bytes=base64.b64decode(decode_jwt_token.get("auth_token")))
    query = select(UserModel).where(UserModel.id == str(user_id))
    result = (await query_response_one(query, db)).one_or_none()
    if result:
        return Response("Success")
    else:
        raise HTTPException(status_code=200, detail=400)
