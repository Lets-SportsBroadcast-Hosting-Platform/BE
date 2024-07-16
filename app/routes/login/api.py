import base64
import uuid
from typing import Annotated, Any
import random
from auth.jwt import verify_access_token
from database import get_db
from database.search_query import query_response_one
from fastapi import Depends, Header, HTTPException, Response
from models.certification_table import CertificationModel
from models.store_table import StoreModel
from models.user_table import (
    AuthModel,
    UserModel,
    authlogin_client2server,
    ssologin_client2server,
    userInfo_server2client,
)
from routes.login.api_helper import login_by_kakao, login_by_naver, send_message
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
        raise HTTPException(status_code=200, detail={'detail':400, 'message':'가입자가 아닙니다.'})
    user_id = uuid.UUID(bytes=base64.b64decode(decode_jwt_token.get("auth_token")))
    query = select(UserModel.role).where(UserModel.id == str(user_id))
    role = (await query_response_one(query, db)).one_or_none()
    
    if role == 'host':
        query = select(StoreModel).where(StoreModel.id == str(user_id))
        result = (await query_response_one(query,db)).one_or_none()
        return result
    else:
        query = select(UserModel).where(UserModel.id == str(user_id))
        result = (await query_response_one(query,db)).one_or_none()
        return result

async def send_certification_number(
        phone_number: str,
        db: AsyncSession = Depends(get_db)
):
    key = ''
    for _ in range(5):
        key += str(random.randint(0, 9))
    #DB에 저장하는 로직
    insertdata = CertificationModel(
        certification_number = key
    )
    db.add(insertdata)
    await db.commit()
    data = {
        "message": {
            "to": phone_number,
            "from": "01087636341",
            "text": key
        }
    }
    return await send_message(data)

async def check_certification_number(
        id: int,
        certification_number: str,
        jwToken: Annotated[str | None, Header(convert_underscores=False)] = None,
        db: AsyncSession = Depends(get_db)
):
    query = select(CertificationModel.certification_number).where(CertificationModel.id == id)
    number = (await query_response_one(query, db)).one_or_none()
    if certification_number == number:
        #핸드폰 번호 저장 로직
        return '인증완료'
    else:
        raise HTTPException(status_code=200, detail= {'status_code':400, 'message':'잘못된 인증번호'})