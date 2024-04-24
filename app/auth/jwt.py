from datetime import datetime, timedelta

from database.connection import Settings
from fastapi import HTTPException, status
from jose import JWTError, jwt
from pydantic import EmailStr

# Settings 클래스를 인스턴스화 해서 .env 값을 가져온다.
settings = Settings()


# 토큰을 생성하는 함수
def create_access_token(email: EmailStr, hash: str) -> str:
    # 토큰을 생성할 때 user 이메일과 exp(만료시간)을 받아온다
    # 받아온 정보를 기반으로 payload를 작성한다. 필요한 정보만큼 저장하면 된다.
    payload = {"email": email, "hash": hash}
    # 작성된 payload와 secrets키, 암호화 알고리즘을 지정해준다.
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    # 만들어진 토큰을 리턴한다.
    return token


# 토큰을 검증하는 함수
def verify_access_token(token: str):
    try:
        # 토큰을 decode한 값을 data에 저장한다.
        # 이 단계에서 decode되지 않으면 당연히 검증된 토큰이 아니다.
        data = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        _hash = data.get("hash")
        if _hash is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No access token supplied"
            )
        return _hash
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
