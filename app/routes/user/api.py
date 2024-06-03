from database import get_db
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from routes.user.api_helper import search_sgisapi

async def search_local(address:str):
    result = await search_sgisapi(address)
    if result:
        return result
    else:
        raise HTTPException(status_code=200, detail = 400)
    

#async def insert_user():