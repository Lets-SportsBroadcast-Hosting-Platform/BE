import json
import secrets
import string

import httpx
from auth.jwt import create_access_token, verify_access_token
from database.connection import get_session
from fastapi import Depends, HTTPException, status
from models.user_table import LoginToken, TokenCreate, TokenResponse, User, UserCreate
from sqlalchemy.orm import Session


# route 함수 카카오 로그인
async def kakao_auth_login(token: TokenResponse, db: Session = Depends(get_session)) -> dict:
    if token.jwt_token:
        token_verify_db(verify_access_token(token.jwt_token)) # 토큰 검증한후
    else:
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer ${token.access_token}",
        }

        async with httpx.AsyncClient() as client:
            response = json.loads((await client.post(url, headers=headers)).text)
            user_data = UserCreate(
                user_id=1,
                email=response.get("kakao_account").get("email"),
                name=response.get("kakao_account").get("name"),
                gender=response.get("kakao_account").get("gender"),
                age=0,
                birth=response.get("kakao_account").get("birthyear")
                + response.get("kakao_account").get("birthday"),
            )
            return user_auth_db(user_data, db)


# db에 데이터가 있는지 확인하는 함수
def token_verify_db(token: TokenCreate, db):
    existing_hash = db.query(LoginToken).filter(LoginToken.user_id == token.user_id).first()
    try:
        if existing_hash:
            return {"login_access": "success", "token_type": "Bearer"}
        else:
            return {"login_access": "fail", "token_type": "Bearer"}
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="잘못된 해쉬값이 전달됨",
        )


def make_hash():
    return "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(32))


# db에 유저 데이터가있는지 확인하고 없으면 데이터 추가
def user_auth_db(user_data: UserCreate, db):
    # 로그인 유저가 DB에 있는지 검사한뒤
    existing_user = db.query(User).filter(User.name == user_data.name).first()
    try:
        if not existing_user:
            db_data = User.from_orm(user_data)
            db_token = LoginToken.from_orm(TokenCreate(hash=make_hash(), user_id=1, provider=""))
            db.add(db_data)
            db.commit()
            db.refresh(db_data)
            db.add(db_token)
            db.commit()
            db.refresh(db_token)
            return {
                "access_token": create_access_token(user_data.user_id, db_token.hash),
                "token_type": "Bearer",
            }
        else:
            if existing_user.email == user_data.email:
                return user_verify_db(existing_user.user_id, db)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Parameter")


# db에 데이터가 있는지 확인하는 함수
def user_verify_db(userid, db):
    existing_hash = db.query(LoginToken).filter(LoginToken.user_id == userid).first()
    try:
        if existing_hash:
            return {
                "access_token": create_access_token(existing_hash.user_id, existing_hash.hash),
                "token_type": "Bearer",
            }
        else:
            return {"login_access": "fail", "token_type": "Bearer"}
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="잘못된 해쉬값이 전달됨",
        )
