from database import get_db
from database.search_query import query_response_one
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from routes.user.api_helper import search_sgisapi
from models.user_table import UserModel, Insert_Userinfo
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from routes.user.api_helper import insert_userinfo
from auth.jwt import jwt_token2user_id
from fastapi import Depends, Header, HTTPException, Response
async def search_local(address:str):
    result = await search_sgisapi(address)
    if result:
        return result
    else:
        raise HTTPException(status_code=200, detail = 400)
    

async def insert_user(
        jwToken: Annotated[str | None, Header(convert_underscores=False)],
        user_info:Insert_Userinfo,
        db: AsyncSession = Depends(get_db)
):
    user_id = await jwt_token2user_id(jwToken)
    query = select(UserModel).where(UserModel.id == str(user_id))
    result = (await query_response_one(query, db)).one_or_none()
    if result:
        
        return await insert_userinfo(str(user_id), user_info, db)
    else:
        raise HTTPException(status_code=200, detail=400)

    