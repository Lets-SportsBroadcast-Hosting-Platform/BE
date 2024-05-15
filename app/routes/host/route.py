import io
import json
from typing import List

import httpx
from database import _s3, get_db, settings
from database.search_query import query_response
from fastapi import Depends, File, Form, HTTPException, UploadFile
from models.hosting_table import HostingModel
from models.store_table import Auth_Business_Registration_Number, StoreModel, storeData
from PIL import Image
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

common_header = {"Accept": "application/json", "Content-Type": "application/json"}


# 사업자 번호 인증 함수
async def auth_bussiness_num(req: Auth_Business_Registration_Number) -> dict:
    print(req)
    url = "http://api.odcloud.kr/api/nts-businessman/v1/status?"
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.post(
            url, data=req.__json__(), headers=common_header, params=req.__params__()
        )
        res_data = json.loads(response.text).get("data")[0]
        if "등록되지 않은" not in res_data.get("tax_type"):
            if res_data.get("b_stt") == "계속사업자":
                return {
                    "b_no": req.b_no[-1],
                    "type": res_data.get("b_stt"),
                }
            else:
                raise HTTPException(status_code=200, detail=400)
        else:
            raise HTTPException(status_code=200, detail=400)


# 가게 검색 함수
async def searchlist(keyword: str, provider: str):
    provider = provider.lower()
    if provider == "kakao":
        return await kakao_searchlist(keyword, provider)
    elif provider == "naver":
        return await naver_searchlist(keyword, provider)
    else:
        raise HTTPException(status_code=200, detail=400)


# 카카오 검색 api 함수
async def kakao_searchlist(keyword: str, provider: str) -> storeData:
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    header = {"Authorization": f"KakaoAK {settings.KAKAO_RESTAPI_KEY}"}
    header.update(common_header)
    data = {"query": keyword, "size": 5}
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(url, params=data, headers=header)
        if response.status_code == 200:
            return storeData(json.loads(response.text).get("documents"), provider)
        else:
            raise HTTPException(status_code=200, detail=400)


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
            raise HTTPException(status_code=200, detail=400)


# s3에 이미지를 올리고 db에 데이터를 커밋하는 api 함수
async def insert_store(
    data: str = Form(...), photos: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)
):
    store_table = make_store_data(json.loads(data), len(photos))
    if not await check_bno(store_table.business_no, db):
        _check_s3_upload = await s3_upload(str(store_table.business_no), photos)
    else:
        raise HTTPException(status_code=200, detail=400)
    if _check_s3_upload:
        db.add(store_table)
        await db.commit()
        return "Upload Success"
    else:
        raise HTTPException(status_code=200, detail=400)


# Store 테이블에 사업자 번호기 존재하는지 확인하는 함수
async def check_bno(b_no: int, db: AsyncSession):
    _query = select(StoreModel).where(StoreModel.business_no == b_no)
    return True if (await query_response(_query, db)).one_or_none() else False


# 클라이언트에서 받은 데이터를 StoreModel화하는 함수
def make_store_data(data: json, img_count: int) -> StoreModel:
    store_data = StoreModel(
        business_no=data.get("business_no"),
        token=data.get("token"),
        place_name=data.get("place_name"),
        address_name=data.get("address_name"),
        road_address_name=data.get("road_address_name"),
        phone=data.get("phone"),
        category_group_name=data.get("category_group_name"),
        image_url=f"https://letsapp.store/{data.get('business_no')}/",
        image_count=img_count,
        introduce=data.get("introduce"),
    )
    return store_data


# s3 사업자 번호를 기준으로 폴더를 만들고 이미지를 청크화해서 업로드하는 함수
async def s3_upload(folder: str, photos: List[UploadFile]):
    if _s3.create_folder(_s3.bucket_name, folder):
        for file_no in range(len(photos)):
            image_data = await photos[file_no].read()
            image = Image.open(io.BytesIO(image_data))
            output = io.BytesIO()
            image.save(output, format="JPEG", quality=80, optimize=True)
            _s3.upload_file_in_chunks(
                photo=output,
                bucket_name=_s3.bucket_name,
                object_name=f"{folder}/{file_no}",
            )
        return True
    else:
        return False
