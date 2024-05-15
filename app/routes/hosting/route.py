from datetime import datetime

from database import get_db
from database.search_query import query_response
from fastapi import Depends, HTTPException
from models.hosting_table import HostingData, HostingModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# 클라이언트에서 호스팅 정보를 받아 db에 등록하는 api 함수
async def make_hosting(hostingdata: HostingData, db: AsyncSession = Depends(get_db)):
    if await insert_hosting_table(hostingdata.to_HostingModel(), db):
        return "호스팅 되었습니다."
    else:
        raise HTTPException(status_code=200, detail=400)


# Hosting 테이블에 insert 하는 함수
async def insert_hosting_table(hostingModel: HostingModel, db: AsyncSession) -> bool:
    if not await check_hosting_table(hostingModel.hosting_name, hostingModel.start_time, db):
        db.add(hostingModel)
        await db.commit()
        return True
    else:
        raise HTTPException(status_code=200, detail=400)


# Hosting 테이블에 hosting_name과 start_time 기준으로 데이터가 있는지 확인하는 함수
async def check_hosting_table(hosting_name: str, start_time: datetime, db: AsyncSession):
    _query = select(HostingModel).where(
        HostingModel.hosting_name == hosting_name and HostingModel.start_time == start_time
    )
    return True if (await query_response(_query, db)).one_or_none() else False
