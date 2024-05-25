import json
from typing import Annotated, List

import httpx
from database import get_db
from fastapi import Depends, File, Form, Header, HTTPException, UploadFile
from models.store_table import Auth_Business_Registration_Number
from routes.host.api_helper import (
    check_bno,
    host_read_store,
    kakao_searchlist,
    make_store_data,
    naver_searchlist,
    s3_upload,
    user_read_store,
    host_update_store,
    host_delete_store,
)
from sqlalchemy.ext.asyncio import AsyncSession

common_header = {"Accept": "application/json", "Content-Type": "application/json"}


# 사업자 번호 인증 함수
async def auth_business_num(
    bno: Annotated[str | None, Header(convert_underscores=False)] = None
) -> dict:
    print(bno)
    business_num = Auth_Business_Registration_Number(b_no=bno)
    print(business_num.b_no)
    url = "http://api.odcloud.kr/api/nts-businessman/v1/status?"
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.post(
            url,
            data=business_num.__json__(),
            headers=common_header,
            params=business_num.__params__(),
        )
        res_data = json.loads(response.text).get("data")[0]
        if "등록되지 않은" not in res_data.get("tax_type"):
            if res_data.get("b_stt") == "계속사업자":
                return {
                    "b_no": business_num.b_no[-1],
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


# s3에 이미지를 올리고 db에 데이터를 커밋하는 api 함수
async def insert_store(
    data: str = Form(...), photos: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)
):
    store_table = make_store_data(json.loads(data), len(photos))
    print(store_table)
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


# db에있는 가게 조회
async def read_store(
    business_no: Annotated[str | None, Header(convert_underscores=False)] = None,
    store_name: str = None,
    db: AsyncSession = Depends(get_db),
):
    if business_no:
        result = await host_read_store(business_no, db)
    else:
        result = await user_read_store(store_name, db)
    #result = await host_read_store(business_no, db)
    return result

async def update_store(
    screen: int,
    business_no: int,
    db: AsyncSession = Depends(get_db),
):
    await host_update_store(screen, business_no, db)

async def delete_store(
    business_no: int,
    db: AsyncSession = Depends(get_db),
):
    await host_delete_store(business_no, db)