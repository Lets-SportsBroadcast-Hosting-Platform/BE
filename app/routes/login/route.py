import base64
import json
import uuid
from datetime import datetime
from typing import Optional

import httpx
from auth.jwt import create_jwt_access_token, verify_access_token
from database import get_db, settings
from database.search_query import query_response
from fastapi import Depends, HTTPException, status
from models.user_table import AuthModel, TokenResponse, UserModel
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession


# 소셜 로그인 함수
async def sso(token: Optional[TokenResponse], db: AsyncSession = Depends(get_db)):
    try:
        if token.provider == "kakao":
            return await login_by_kakao(token, db)
        elif token.provider == "naver":
            return await login_by_naver(token, db)
        else:
            raise ValueError("잘못된 소셜 로그인을 하셨습니다.")
    except ValueError as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# 클라이언트에서 토큰으로 로그인
async def login_as_token(token: Optional[TokenResponse] = None, db: AsyncSession = Depends(get_db)):
    print(token)
    decode_jwt_token = verify_access_token(token.jwt_token)
    try:
        query = select(AuthModel).where(
            AuthModel.token == decode_jwt_token.get("login_token")
            and AuthModel.provider == decode_jwt_token.get("provider")
        )
        if (await query_response(query, db)).one_or_none():
            user_id = uuid.UUID(bytes=base64.b64decode(decode_jwt_token.get("login_token")))
            print("디코딩된 AuthModel.token을 uuid로 변환", user_id)
            query = select(UserModel).where(UserModel.user_id == user_id)
            if (await query_response(query, db)).one_or_none():
                return HTTPException(status_code=status.HTTP_200_OK, detail="Success")
            else:
                raise ValueError("Fail")
        else:
            raise ValueError("Fail")
    except ValueError as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# 카카오 로그인 함수 구현
async def login_by_kakao(token: Optional[TokenResponse], db: AsyncSession) -> dict:
    print("카카오 로그인 시도")
    url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer ${token.access_token}",
    }
    async with httpx.AsyncClient() as client:
        response = json.loads((await client.post(url, headers=headers)).text)
        try:
            if response:
                user_data, auth_data = make_user_data(response, token.provider)
                return await user_auth_db(user_data, auth_data, db)
            else:
                raise ValueError("Bad Parameter")
        except ValueError as e:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# 네이버 로그인 함수 구현
async def login_by_naver(token: Optional[TokenResponse], db: AsyncSession) -> dict:
    print("네이버 로그인 시도")
    try:
        access_token = await naver_auth_token(token)
        if access_token:
            response = await naver_get_data(access_token)
        else:
            raise ValueError("Bad Parameter")
        if response:
            user_data, auth_data = make_user_data(response, token.provider)
            return await user_auth_db(user_data, auth_data, db)
        else:
            raise ValueError("Bad Parameter")
    except ValueError as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# 네이버 access_token 발급 함수
async def naver_auth_token(token: Optional[TokenResponse]) -> str:
    token_url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={settings.NAVER_CLIENT_ID}&client_secret={settings.NAVER_SECRET_KEY}&code={token.access_token}&state={token.state}"
    async with httpx.AsyncClient() as client:
        response = json.loads((await client.get(token_url)).text)
        return response.get("access_token")


# 네이버 유저 데이터 발급 함수
async def naver_get_data(access_token: str) -> dict:
    url = "https://openapi.naver.com/v1/nid/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        return json.loads((await client.get(url, headers=headers)).text)


def make_user_data(response: dict, provider: str) -> (UserModel, AuthModel):  # type: ignore
    if provider == "kakao":
        response = response.get("kakao_account")
    elif provider == "naver":
        response = response.get("response")
    user_uuid = uuid.uuid5(namespace=uuid.NAMESPACE_OID, name=response.get("email"))
    user_data = UserModel(
        user_id=str(user_uuid),
        mail=response.get("email"),
        name=response.get("name"),
        gender=False if response.get("gender") == "male" else True,
        birthyear=response.get("birthyear"),
        birthday=response.get("birthday").replace("-", ""),
    )
    auth_data = AuthModel(token=str(base64.b64encode(user_uuid.bytes))[2:-1], provider=provider)
    return user_data, auth_data


# db에 유저 데이터가있는지 확인하고 없으면 데이터 추가
async def user_auth_db(user_table: UserModel, auth_table: AuthModel, db: AsyncSession) -> dict:
    # 로그인 유저가 DB에 있는지 검사한뒤
    if not await user_db_check(user_table, db):
        print("유저 없음")
        user_table.region, user_table.alarm = "서울", False
        auth_table.create_time = user_table.join_date = datetime.today()
        db.add_all([user_table, auth_table])
        await db.commit()
        await db.refresh(user_table)
        await db.refresh(auth_table)
        return {"jwToken": create_jwt_access_token(auth_table.token, auth_table.provider)}
    else:
        print("유저 있음")
        return await token_verify_db(user_table.user_id, auth_table.provider, db)


# user table에 가입되어 있는지 확인
async def user_db_check(data: UserModel, db: AsyncSession) -> bool:
    _query = select(UserModel).where(UserModel.name == data.name)
    existing_id = (await query_response(_query, db)).one_or_none()
    return True if existing_id else False


# login table에 데이터가 있는지 확인하고
# 소셜 로그인 provider와 일치하는지 확인하는 함수
async def token_verify_db(user_id: str, provider: str, db: AsyncSession) -> dict:
    existing_token = await login_token_db_check_by_token(user_id, db)
    try:
        if existing_token and existing_token.provider == provider:
            return {
                "jwt_token": create_jwt_access_token(existing_token.token, existing_token.provider)
            }
        elif existing_token.provider != provider:
            raise ValueError(existing_token.provider + " 로 가입된 계정이 있습니다.")
        else:
            raise ValueError("잘못된 토큰값이 전달됨")
    except ValueError as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# login table에 값이 있는지 확인
async def login_token_db_check_by_token(user_id: str, db: AsyncSession) -> ScalarResult:
    user_id_to_token = base64.b64encode(uuid.UUID(user_id).bytes)
    query = select(AuthModel).where(AuthModel.token == str(user_id_to_token)[2:-1])
    result = (await query_response(query, db)).one_or_none()
    return result if result else False
