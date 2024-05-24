from database import get_db
from fastapi import Depends, HTTPException
from models.hosting_table import HostingData
from routes.hosting.api_helper import insert_hosting_table, read_hosting_table, read_hosting_tables
from sqlalchemy.ext.asyncio import AsyncSession


# 클라이언트에서 호스팅 정보를 받아 db에 등록하는 api 함수
async def make_hosting(hostingdata: HostingData, db: AsyncSession = Depends(get_db)):
    print(hostingdata.game_start_date)
    if await insert_hosting_table(hostingdata.to_HostingModel(), db):
        return "호스팅 되었습니다."
    else:
        raise HTTPException(status_code=200, detail=400)


# 클라이언트에서 호스팅 id를 받아 응답하는 함수
async def read_hostings(hosting_name: int, db: AsyncSession = Depends(get_db)):
    result = await read_hosting_tables(hosting_name, db)
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