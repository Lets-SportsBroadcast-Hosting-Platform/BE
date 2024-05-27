from database import get_db
import io
from fastapi import Depends, HTTPException, File, UploadFile
from typing import List
from .models.hosting_models import HostinginsertModel
from routes.host.api_helper import check_bno
from routes.hosting.api_helper import (
    read_hosting_table, 
    read_hosting_tables, 
    update_hosting_table, 
    delete_hosting_table,
    update_storeimage,
    make_hosting_data)
from sqlalchemy.ext.asyncio import AsyncSession

# 클라이언트에서 호스팅 정보를 받아 db에 등록하는 api 함수
#async def make_hosting(hostinginsertmodel: HostinginsertModel,  photos: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)):
async def make_hosting(hostinginsertmodel: HostinginsertModel, db: AsyncSession = Depends(get_db)):
    hosting_data = make_hosting_data(hostinginsertmodel)
    print(hosting_data)
    #update_storeimage(hostinginsertmodel.business_no,len(photos), hostinginsertmodel.screen_size)
    #print(hostingdata.game_start_date)
    if await check_bno(hosting_data.business_no, db):
        db.add(hosting_data)
        await db.commit()
        return "호스팅 되었습니다."
    else:
        raise HTTPException(status_code=200, detail=400)
    

#image, screen_size을 store테이블에 넣는 기능을 다른 api로 구현
async def update_image_store(business_no: int, screen_size:int, photos: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)):
    if await check_bno(business_no, db):
        await update_storeimage(business_no, len(photos), screen_size, db)
        return "이미지 스크린 사이즈 저장"
    else:
        raise HTTPException(status_code=200, detail=400)


# 클라이언트에서 호스팅 id를 받아 응답하는 함수
async def read_hostings(business_no: int, db: AsyncSession = Depends(get_db)):
    result = await read_hosting_tables(business_no, db)
    if result:
        return result
    else:
        raise HTTPException(status_code=200, detail=400)

async def read_hosting(hosting_id: int, db: AsyncSession = Depends(get_db)):
    result = await read_hosting_table(hosting_id, db)
    if result:
        return result
    else:
        raise HTTPException(status_code=200, detail=400)
    
async def update_hosting(hosting_id: int, db: AsyncSession = Depends(get_db)):
    result = await update_hosting_table(hosting_id, db)
    if result:
        return "수정되었습니다."
    else:
        raise HTTPException(status_code=200, detail=400)
    
async def delete_hosting(hosting_id: int, db: AsyncSession = Depends(get_db)):
    result = await delete_hosting_table(hosting_id, db)
    if result:
        return "삭제되었습니다."
    else:
        raise HTTPException(status_code=200, detail=400)
    

