import json

import httpx
from database import settings
from fastapi import HTTPException
from models.store_table import (
    Add_New_StoreInfo,
    Auth_Business_Registration_Number,
    storeData,
)

common_header = {"Accept": "application/json", "Content-Type": "application/json"}


# 사업자 번호 인증 함수
async def auth_bussiness_num(req: Auth_Business_Registration_Number) -> dict:
    url = "http://api.odcloud.kr/api/nts-businessman/v1/status?"
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.post(
            url, data=req.__json__(), headers=common_header, params=req.__params__()
        )
        res_data = json.loads(response.text).get("data")[0]
        if "등록되지 않은" not in res_data.get("tax_type"):
            if res_data.get("b_stt") == "계속사업자":
                return {"type": res_data.get("b_stt"), "result": "인증 되었습니다."}
            else:
                raise HTTPException(status_code=400, detail=res_data.get("b_stt"))
        else:
            raise HTTPException(status_code=400, detail=res_data.get("tax_type"))


# 새로운 가게 추가
async def storeInsert(info: Add_New_StoreInfo):
    return info.model_dump()


# 가게 검색 함수
async def searchlist(keyword: str, provider: str):
    print(keyword, provider)
    provider = provider.lower()
    if provider == "kakao":
        return await kakao_searchlist(keyword, provider)
    elif provider == "naver":
        return await naver_searchlist(keyword, provider)
    else:
        raise HTTPException(status_code=400, detail="bad provider")


# 카카오 검색 api 함수
async def kakao_searchlist(keyword: str, provider: str) -> storeData:
    print(keyword, provider)
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    header = {"Authorization": f"KakaoAK {settings.KAKAO_RESTAPI_KEY}"}
    header.update(common_header)
    data = {"query": keyword, "size": 5}
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(url, params=data, headers=header)
        if response.status_code == 200:
            return storeData(json.loads(response.text).get("documents"), provider)
        else:
            raise HTTPException(status_code=500, detail="잘못된 요청입니다.")


# 네이버 검색 api 함수
async def naver_searchlist(keyword: str, provider: str) -> storeData:
    url = "https://openapi.naver.com/v1/search/local.json"
    header = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_SECRET_KEY,
    }
    header.update(common_header)
    data = {"query": keyword, "display": 5}
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(url, params=data, headers=header)
        if response.status_code == 200:
            return storeData(json.loads(response.text).get("items"), provider)
        else:
            raise HTTPException(status_code=500, detail="잘못된 요청입니다.")
