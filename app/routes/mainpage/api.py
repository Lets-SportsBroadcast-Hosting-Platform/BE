from database import get_db
from fastapi import Depends, HTTPException
from models.hosting_table import HostingData
from routes.mainpage.api_helper import read_hosting_tables
from sqlalchemy.ext.asyncio import AsyncSession


async def read_hostings(db: AsyncSession = Depends(get_db)):
    result = await read_hosting_tables(db)
    if result:
        return result
    else:
        raise HTTPException(status_code=200, detail=400)