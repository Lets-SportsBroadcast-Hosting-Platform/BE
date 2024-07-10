import json
from typing import Annotated

import httpx
from database import get_db
from fastapi import Depends, Form, Header, HTTPException
from models.store_table import Auth_Business_Registration_Number
from routes.host.api_helper import (
    check_bno,
    host_read_store,
    kakao_searchlist,
    make_store_data,
    naver_searchlist,
    other_searchlist,
    user_read_store,
    get_name,
    host_update_store,
    host_delete_store,
    store_update_alarm,
    change_user_type,
)
from auth.jwt import jwt_token2user_id
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from .models.store_models import StoreinsertModel, StoreUpdateModel

common_header = {"Accept": "application/json", "Content-Type": "application/json"}


# 사업자 번호 인증 함수
async def auth_business_num(
    jwToken: Annotated[str | None, Header(convert_underscores=False)],
    business_no: str,
    start_dt: str,
    db: AsyncSession = Depends(get_db)
) -> dict:
    business_num = Auth_Business_Registration_Number(b_no=business_no)
    print(business_num.b_no)
    id = await jwt_token2user_id(jwToken)
    name = await get_name(str(id), db)  # Ensure get_name is an async function
    url = "http://api.odcloud.kr/api/nts-businessman/v1/validate?serviceKey=IRIyY0JPZa84xQT1zGNnN3lnQ3zu7iuMgnOfdJUmdN6VgDzCCYP8PKzQTm09LRuFKs7mdN3bf9xBVPACVqD2xw=="
    if name is None:
        name = '이름이존재하지않음'
    body = {
        "businesses": [
            {
                "b_no": business_num.b_no[0],
                "start_dt": start_dt,
                "p_nm": str(name)
            }
        ]
    }
    
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.post(
            url,
            json=body,  # Use json parameter to automatically encode the dictionary as JSON
            headers=common_header
        )
        print(response)
        res_data = response.json().get("data")[0]
        if "02" not in res_data.get("valid"):
            res_data = res_data.get("status")
            if res_data.get("b_stt") == "계속사업자":
                return {
                    "b_no": business_num.b_no,
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

async def check_address(keyword:str, provider:str):
    provider = 'other'
    return await other_searchlist(keyword, provider)


# s3에 이미지를 올리고 db에 데이터를 커밋하는 api 함수
async def insert_store(
    jwToken: Annotated[str | None, Header(convert_underscores=False)],
    storeinsertmodel: StoreinsertModel, db: AsyncSession = Depends(get_db)
):
    id = await jwt_token2user_id(jwToken)
    store_table = make_store_data(storeinsertmodel, str(id))
    #store_table = make_store_data(json.loads(data), len(photos))
    #print(store_table)
    if not await check_bno(store_table.business_no, db):
        await store_update_alarm(storeinsertmodel.alarm, store_table.id, db)
        await change_user_type(store_table.id, db)
        db.add(store_table)
        await db.commit()
        return "Upload Success"
    else:
        raise HTTPException(status_code=200, detail={'detail':400, 'message':'이미 등록된 사업자번호입니다.'}, )


# db에있는 가게 조회
async def read_store(
    business_no: int,
    db: AsyncSession = Depends(get_db),
):
    if business_no:
        result = await host_read_store(business_no, db)
    else:
        return HTTPException(status_code=200, detail={'detail':400, 'message':'사업자번호를 입력해주세요'})
    #result = await host_read_store(business_no, db)
    return result
#business_no: Annotated[str | None, Header(convert_underscores=False)] = None,
async def update_store(
    business_no: int,
    storeupdatemodel: StoreUpdateModel,
    db: AsyncSession = Depends(get_db),
):
    try:
        await host_update_store(storeupdatemodel, business_no, db)
        return "Update Success"
    except:
        raise HTTPException(status_code=200, detail=400) 

async def delete_store(
    business_no: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        await host_delete_store(business_no, db)
        return "Delete Success"
    except:
        raise HTTPException(status_code=200, detail=400)