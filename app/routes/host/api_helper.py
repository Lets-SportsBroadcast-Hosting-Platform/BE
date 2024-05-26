import io
import json
from typing import List

import httpx
from database import _s3, settings
from database.search_query import query_response, update_response, delete_response
from fastapi import HTTPException, Response, UploadFile
from models.store_table import StoreModel, storeData
from PIL import Image
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from .models.store_models import StoreinsertModel, StoreUpdateModel


# 카카오 검색 함수

async def kakao_searchlist(keyword: str, provider: str) -> storeData:
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    header = {"Authorization": f"KakaoAK {settings.KAKAO_RESTAPI_KEY}"}
    data = {"query": keyword, "size": 5}
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(url, params=data, headers=header)
        if response.status_code == 200:
            return storeData(json.loads(response.text).get("documents"), provider)
        else:
            raise HTTPException(status_code=200, detail=400)


# 네이버 검색 함수
async def naver_searchlist(keyword: str, provider: str) -> storeData:
    url = "https://openapi.naver.com/v1/search/local.json"
    header = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_SECRET_KEY,
    }
    data = {"query": keyword, "display": 5}
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(url, params=data, headers=header)
        if response.status_code == 200:
            return storeData(json.loads(response.text).get("items"), provider)
        else:
            raise HTTPException(status_code=200, detail=400)


# Store 테이블에 사업자 번호기 존재하는지 확인하는 함수
async def check_bno(b_no: int, db: AsyncSession):
    _query = select(StoreModel).where(StoreModel.business_no == b_no)
    return True if (await query_response(_query, db)) else False


# 클라이언트에서 받은 데이터를 StoreModel화하는 함수
def make_store_data(data: StoreinsertModel) -> StoreModel:
    store_data = StoreModel(
        business_no=data.business_no,
        id=data.id,
        store_name=data.store_name,
        store_address=data.store_address,
        store_road_address=data.store_road_address,
        store_number=data.store_number,
        store_category=data.store_category,
    )
    return store_data


# s3 사업자 번호를 기준으로 폴더를 만들고 이미지를 청크화해서 업로드하는 함수
async def s3_upload(folder: str, photos: List[UploadFile]):
    if _s3.create_folder(_s3.bucket_name, folder):
        for file_no in range(len(photos)):
            image_data = await photos[file_no].read()
            image = Image.open(io.BytesIO(image_data))
            print(image.mode)
            if image.mode in ("RGBA", "RGBX", "LA", "P", "PA"):
                rgb_image = image.convert("RGB")
            output = io.BytesIO()
            rgb_image.save(output, format="JPEG", quality=80, optimize=True)
            _s3.upload_file_in_chunks(
                photo=output,
                bucket_name=_s3.bucket_name,
                object_name=f"{folder}/{file_no}",
            )
        return True
    else:
        return False

#async def s3_delete(folder: str):
    
async def host_read_store(business_no: int, db: AsyncSession):
    _query = select(StoreModel).where(StoreModel.business_no == business_no)
    existing_store = (await query_response(_query, db))
    print(existing_store)
    if existing_store:
        # 객체의 컬럼 값을 가져오기
        existing_store = existing_store[0]
        store_details = {
            "business_no": existing_store.business_no,
            "id": existing_store.id,
            "store_name": existing_store.store_name,
            "store_address": existing_store.store_address,
            "store_road_address": existing_store.store_road_address,
            "store_category": existing_store.store_category,
            "store_number": existing_store.store_number,
            "store_image_url": existing_store.store_image_url,
            "store_image_count": existing_store.store_image_count,
            "screen_size": existing_store.screen_size,
            "create_time": existing_store.create_time,
            "update_time": existing_store.update_time,
            "delete_state": existing_store.delete_state
        }
        return store_details
    else:
        raise HTTPException(status_code=200, detail=400)


async def user_read_store(store_name: str, db: AsyncSession):
    _query = select(StoreModel).where(StoreModel.store_name == store_name)
    existing_store = (await query_response(_query, db)).one_or_none()
    print(existing_store.store_name)
    if existing_store:
        return existing_store.store_name
    else:
        raise HTTPException(status_code=200, detail=400)


async def host_update_store(data: StoreUpdateModel, business_no: int, db: AsyncSession):
    value = {
        StoreModel.store_address : data.store_address,
        StoreModel.store_road_address : data.store_road_address,
        StoreModel.store_name : data.store_name
    }
    _query = update(StoreModel).where(StoreModel.business_no == business_no).values(value)
    await update_response(_query, db)

async def host_delete_store(business_no: int, db: AsyncSession):
    value = {
        StoreModel.delete_state : True
    }
    _query = update(StoreModel).where(StoreModel.business_no == business_no).values(value)
    await update_response(_query,db)
