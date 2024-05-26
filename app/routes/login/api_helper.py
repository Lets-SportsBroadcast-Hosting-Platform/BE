import base64
import json
import uuid
from datetime import datetime

import httpx
from auth.jwt import create_jwt_access_token
from database import settings
from database.search_query import query_response_one
from fastapi import HTTPException
from models.user_table import (
    AuthModel,
    UserModel,
    login_result_server2client,
    ssologin_client2server,
    userInfo_server2client,
)
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession


# 카카오 로그인 함수 구현 CQRS : Create
async def login_by_kakao(
    req: ssologin_client2server, region: str, alarm: bool, db: AsyncSession
) -> login_result_server2client:
    url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer ${req.access_token}",
    }
    async with httpx.AsyncClient(http2=True) as client:
        response = json.loads((await client.post(url, headers=headers)).text)
        if not response:
            raise HTTPException(status_code=200, detail=400)
        res = await user_auth_db(*make_user_data(response, req.provider, region, alarm), db)
        if type(res) == ValueError:
            raise HTTPException(status_code=200, detail=400)
        return login_result_server2client(jwt_token=res[0], instance=res[-1])


# 네이버 로그인 함수 구현 CQRS : Create
async def login_by_naver(
    req: ssologin_client2server, region: str, alarm: bool, db: AsyncSession
) -> login_result_server2client:
    access_token = await naver_auth_token(req)
    if not access_token:
        raise HTTPException(status_code=200, detail=400)
    response = await naver_get_data(access_token)
    if not response:
        raise HTTPException(status_code=200, detail=400)
    res = await user_auth_db(*make_user_data(response, req.provider, region, alarm), db)
    if type(res) == ValueError:
        raise HTTPException(status_code=200, detail=400)
    return login_result_server2client(jwt_token=res[0], instance=res[-1])


# 네이버 access_token 발급 함수
async def naver_auth_token(req: ssologin_client2server) -> str:
    token_url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={settings.NAVER_CLIENT_ID}&client_secret={settings.NAVER_SECRET_KEY}&code={req.access_token}&state={req.state}"
    async with httpx.AsyncClient(http2=True) as client:
        response = json.loads((await client.get(token_url)).text)
        return response.get("access_token")


# 네이버 유저 데이터 발급 함수
async def naver_get_data(access_token: str) -> dict:
    url = "https://openapi.naver.com/v1/nid/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient(http2=True) as client:
        return json.loads((await client.get(url, headers=headers)).text)


# 응답 받은 유저 정보를 db에 넘기기 위한 모델로 변환하는 함수
def make_user_data(response: dict, provider: str, region: str, alarm: bool) -> (UserModel, AuthModel):  # type: ignore
    print("유저 정보", response)
    if provider == "kakao":
        response = response.get("kakao_account")
        user_gender = "M" if response.get("gender") == "male" else "F"
    elif provider == "naver":
        response = response.get("response")
        user_gender = response.get("gender")
    user_uuid = uuid.uuid5(namespace=uuid.NAMESPACE_OID, name=response.get("email"))

    user_data = UserModel(
        id=str(user_uuid),
        name=response.get("name"),
        gender=user_gender,
        birthyear=response.get("birthyear"),
        area=region,
        alarm=alarm,
    )
    auth_data = AuthModel(token=str(base64.b64encode(user_uuid.bytes))[2:-1], provider=provider)
    return user_data, auth_data


# db에 유저 데이터가있는지 확인하고 없으면 데이터 추가
async def user_auth_db(
    user_table: UserModel, auth_table: AuthModel, db: AsyncSession
) -> tuple | ValueError:
    # 로그인 유저가 DB에 있는지 검사한뒤
    before_check_db = userInfo_server2client(user_instance=user_table)
    db_check, after_check_db = await user_db_check(user_table, db)
    if db_check:
        print("유저 있음", flush=True)
        jwt_token_or_error = await token_verify_db(user_table.id, auth_table.provider, db)
        if type(jwt_token_or_error) == str:  # Jwt_token일떄
            return jwt_token_or_error, after_check_db
        else:  # ValueError일때
            return jwt_token_or_error
    else:
        auth_table.create_time = datetime.today()
        db.add_all([user_table, auth_table])
        await db.commit()
        await db.refresh(user_table)
        await db.refresh(auth_table)
        jwt_token = create_jwt_access_token(auth_table.token, auth_table.provider)
        return jwt_token, before_check_db


# user table에 가입되어 있는지 확인
async def user_db_check(data: UserModel, db: AsyncSession) -> (bool, UserModel | None):  # type: ignore

    _query = select(UserModel).where(UserModel.name == data.name, UserModel.id == data.id)
    existing_id = (await query_response_one(_query, db)).one_or_none()
    return True if existing_id else False, existing_id


# auth table에 데이터가 있는지 확인하고
# 소셜 로그인 provider와 일치하는지 확인하는 함수
# jwt 토큰 반환
async def token_verify_db(user_id: str, provider: str, db: AsyncSession) -> str | ValueError:
    existing_token = await auth_table_check_by_userid(user_id, db)
    if existing_token and existing_token.provider == provider:
        return create_jwt_access_token(existing_token.token, existing_token.provider)
    elif existing_token.provider != provider:
        return ValueError(existing_token.provider + " 로 가입된 계정이 있습니다.")
    else:
        return ValueError("잘못된 토큰값이 전달됨")


# auth table에 값이 있는지 확인
async def auth_table_check_by_userid(user_id: str, db: AsyncSession) -> ScalarResult | bool:
    user_id_to_token = base64.b64encode(uuid.UUID(user_id).bytes)
    query = select(AuthModel).where(AuthModel.token == str(user_id_to_token)[2:-1])
    result = (await query_response_one(query, db)).one_or_none()
    return result if result else False
