import io
import json
from typing import List, Annotated
from database.search_query import query_response_one
from database import get_db
from fastapi import Depends, File, Form, HTTPException, UploadFile, Header, Request
from models.user_table import UserModel
from auth.jwt import jwt_token2user_id
from sqlalchemy import select
from routes.host.api_helper import check_bno, get_business_no
from routes.hosting.api_helper import (
    delete_hosting_table,
    make_hosting_data,
    read_hosting_table,
    read_hosting_tables,
    s3_upload,
    s3_upload_issue,
    update_hosting_table,
    update_storeimage,
)
from sqlalchemy.ext.asyncio import AsyncSession

# 클라이언트에서 호스팅 정보를 받아 db에 등록하는 api 함수
# async def make_hosting(hostinginsertmodel: HostinginsertModel,  photos: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)):
"""async def make_hosting(hostinginsertmodel: HostinginsertModel, db: AsyncSession = Depends(get_db)):
    hosting_data = make_hosting_data(hostinginsertmodel)
    print(hosting_data)
    #update_storeimage(hostinginsertmodel.business_no,len(photos), hostinginsertmodel.screen_size)
    #print(hostingdata.game_start_date)
    if await check_bno(hosting_data.business_no, db):
        db.add(hosting_data)
        await db.commit()
        return "호스팅 되었습니다."
    else:
        raise HTTPException(status_code=200, detail=400)"""


async def test_img_upload(photos: List[UploadFile] = File(...)):
    try:
        await s3_upload_issue("test_img_upload", photos)
        return 'good'
    except Exception as e:
        return f"An error occurred: {e}"

'''async def test_img_upload(request: Request):
    return request'''

async def make_hosting_issue(
    jwToken: Annotated[str | None, Header(convert_underscores=False)],
    data: str = Form(...), photos: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)
):
    try:
        user_id = await jwt_token2user_id(jwToken)
        print(user_id)
        query = select(UserModel).where(UserModel.id == str(user_id))
        result = (await query_response_one(query, db)).one_or_none()
        if result:
            business_no = await get_business_no(user_id, db)
            print(business_no)
            print('photo:', photos)
            data = json.loads(data)
            hosting_data = make_hosting_data(data,business_no, False)
            print(hosting_data)
            print(business_no)
            if await check_bno(business_no, db):
                await update_storeimage(business_no, len(photos), data.get('screen_size'), db)
                await s3_upload(str(business_no), photos)
                db.add(hosting_data)
                await db.commit()
                return "호스팅 되었습니다."
            else:
                raise HTTPException(status_code=200, detail=400)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise 


async def make_hosting(
        jwToken: Annotated[str | None, Header(convert_underscores=False)],
        data: str = Form(...), 
        photos: List[UploadFile] = File(...), 
        db: AsyncSession = Depends(get_db)):
    try:
        user_id = await jwt_token2user_id(jwToken)
        print(user_id)
        query = select(UserModel).where(UserModel.id == str(user_id))
        result = (await query_response_one(query, db)).one_or_none()
        if result:
            business_no = await get_business_no(user_id, db)
            print(business_no)
            print('photo:', photos)
            data = json.loads(data)
            hosting_data = make_hosting_data(data,business_no, False)
            print(hosting_data)
            print(business_no)
            if await check_bno(business_no, db):
                await update_storeimage(business_no, len(photos), data.get('screen_size'), db)
                await s3_upload(str(business_no), photos)
                db.add(hosting_data)
                await db.commit()
                return "호스팅 되었습니다."
            else:
                raise HTTPException(status_code=200, detail=400)
    except Exception as e:
        error = f"An error occurred: {e}"
        return error

async def make_hosting_exceptimage(
        jwToken: Annotated[str | None, Header(convert_underscores=False)],
        data: str = Form(...), 
        db: AsyncSession = Depends(get_db)):
    try:
        user_id = await jwt_token2user_id(jwToken)
        print(user_id)
        query = select(UserModel).where(UserModel.id == str(user_id))
        result = (await query_response_one(query, db)).one_or_none()
        if result:
            business_no = await get_business_no(user_id, db)
            print(business_no)
            #print('photo:', photos)
            data = json.loads(data)
            hosting_data = make_hosting_data(data,business_no, False)
            print(hosting_data)
            print(business_no)
            if await check_bno(business_no, db):
                #await update_storeimage(business_no, len(photos), data.get('screen_size'), db)
                #await s3_upload(str(business_no), photos)
                db.add(hosting_data)
                await db.commit()
                return "호스팅 되었습니다."
            else:
                raise HTTPException(status_code=200, detail=400)
    except Exception as e:
        error = f"An error occurred: {e}"
        return error
async def update_hosting(
    hosting_id: int,
    data: str = Form(...),
    photos: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
):
    data = json.loads(data)
    print(f"update_hosting > data : {data}")
    hosting_data = make_hosting_data(data, True)
    print(f"update_hosting > hosting_data : {hosting_data}")
    await s3_upload(str(hosting_data.business_no), photos)
    try:

        await update_storeimage(hosting_data.business_no, len(photos), data["screen_size"], db)

        await update_hosting_table(hosting_id, hosting_data, db)
        return "호스팅이 수정되었습니다."
    except:
        raise HTTPException(status_code=200, detail=400)


# image, screen_size을 store테이블에 넣는 기능을 다른 api로 구현
"""async def update_image_store(business_no: int, screen_size:int, photos: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)):
    if await check_bno(business_no, db):
        await update_storeimage(business_no, len(photos), screen_size, db)
        return "이미지 스크린 사이즈 저장"
    else:
        raise HTTPException(status_code=200, detail=400)"""


# 클라이언트에서 호스팅 id를 받아 응답하는 함수
async def read_hostings(
        jwToken: Annotated[str | None, Header(convert_underscores=False)], 
        status:bool, 
        db: AsyncSession = Depends(get_db)):
    user_id = await jwt_token2user_id(jwToken)
    query = select(UserModel).where(UserModel.id == str(user_id))
    result = (await query_response_one(query, db)).one_or_none()
    if result:
        business_no = await get_business_no(user_id, db)
        hostings = await read_hosting_tables(business_no, status, db)
        return hostings if hostings else []
    else:
        raise HTTPException(status_code=200, detail={'detail': 400, 'message':'유효하지않는 jwToken.'})


async def read_hosting(hosting_id: int, db: AsyncSession = Depends(get_db)):
    print(hosting_id)
    result = await read_hosting_table(hosting_id, db)
    if result:
        return result
    else:
        raise HTTPException(status_code=200, detail=400)


async def delete_hosting(hosting_id: int, db: AsyncSession = Depends(get_db)):
    result = await delete_hosting_table(hosting_id, db)
    if result:
        return "삭제되었습니다."
    else:
        raise HTTPException(status_code=200, detail=400)
