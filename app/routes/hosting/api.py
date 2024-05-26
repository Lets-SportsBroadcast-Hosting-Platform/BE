from database import get_db
import io
from fastapi import Depends, HTTPException, File, UploadFile
from typing import List
from .models.hosting_models import HostinginsertModel
from routes.hosting.api_helper import (
    insert_hosting_table, 
    read_hosting_table, 
    read_hosting_tables, 
    update_hosting_table, 
    delete_hosting_table,
    update_storeimage,
    make_hosting_data)
from sqlalchemy.ext.asyncio import AsyncSession

# 클라이언트에서 호스팅 정보를 받아 db에 등록하는 api 함수
async def make_hosting(hostinginsertmodel: HostinginsertModel,  photos: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)):
    hosting_data = make_hosting_data(hostinginsertmodel)
    print(hosting_data)
    update_storeimage(hosting_data.business_no,len(photos), hosting_data.screen_size)

    #print(hostingdata.game_start_date)
    if await insert_hosting_table(hostinginsertmodel, db):
        return "호스팅 되었습니다."
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
        return result
    else:
        raise HTTPException(status_code=200, detail=400)
    
async def delete_hosting(hosting_id: int, db: AsyncSession = Depends(get_db)):
    result = await delete_hosting_table(hosting_id, db)
    if result:
        return result
    else:
        raise HTTPException(status_code=200, detail=400)
    

