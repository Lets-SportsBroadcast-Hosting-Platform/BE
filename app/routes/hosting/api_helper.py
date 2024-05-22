from datetime import datetime

from database.search_query import query_response
from fastapi import HTTPException
from models.hosting_table import HostingModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# Hosting 테이블에 insert 하는 함수 CQRS : Create
async def insert_hosting_table(hostingModel: HostingModel, db: AsyncSession) -> bool:
    try:
        db.add(hostingModel)
        await db.commit()
        return True
    except:
        raise HTTPException(status_code=200, detail=400)


# Hosting 테이블에서 id로 Read 하는 함수 CQRS : Read
async def read_hosting_table(hosting_name: str, db: AsyncSession) -> HostingModel:
    _query = select(HostingModel).where(
        HostingModel.business_no == hosting_name,
        HostingModel.active_state == True,
        HostingModel.delete_state == False,
    )
    response = (await query_response(_query, db)).all()
    if response:
        return response
    else:
        raise HTTPException(status_code=200, detail=400)
