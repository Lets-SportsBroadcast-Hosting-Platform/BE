from database import settings
from jose import JWTError, jwt


# jwt 토큰을 생성하는 함수
def create_jwt_access_token(token: str, provider: str) -> str:
    payload = {"auth_token": token, "provider": provider}
    try:
        jwt_token = jwt.encode(payload, settings.SERVER_SECRET_KEY, algorithm="HS256")
        return jwt_token
    except JWTError:
        raise ValueError("인코딩이 되지 않았습니다.")


# jwt 토큰을 검증하는 함수 -> 디코드된 토큰을 반환한다
def verify_access_token(jwt_token: str) -> str:
    print("verfiy_access_token", jwt_token, flush=True)
    try:
        # 토큰을 decode한 값을 data에 저장한다.
        # 이 단계에서 decode되지 않으면 당연히 검증된 토큰이 아니다.
        token = jwt.decode(jwt_token, settings.SERVER_SECRET_KEY, algorithms="HS256")
        return token
    except JWTError:
        raise ValueError("디코딩 이 불가합니다.")
