from datetime import datetime
from database import get_db
from database.search_query import query_response_one, query_response,delete_response, update_response
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from routes.user.api_helper import search_sgisapi
from models.user_table import UserModel, Insert_Userinfo, Update_Userinfo
from models.store_table import StoreModel
from models.hosting_table import HostingModel
from models.participation_table import ParticipationModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from routes.user.api_helper import insert_userinfo, making_participation
from auth.jwt import jwt_token2user_id
from routes.user.api_helper import delete_party_table, read_hosting_tables, making_user, update_user_table,add_current_person, check_applicants
from routes.hosting.api_helper import read_hosting_table
from routes.host.api_helper import get_business_no
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
async def read_user(
        jwToken: Annotated[str | None, Header(convert_underscores=False)],
        db: AsyncSession = Depends(get_db)
):
    user_id = await jwt_token2user_id(jwToken)
    query = select(UserModel).where(UserModel.id == str(user_id))
    result = await query_response(query, db)
    if result:
        return await making_user(result[0])
    else:
        raise HTTPException(status_code=200, detail=400)
    
async def update_user(
        jwToken: Annotated[str | None, Header(convert_underscores=False)],
        update_useinfo:Update_Userinfo,
        db: AsyncSession = Depends(get_db)
):
    user_id = await jwt_token2user_id(jwToken)
    query = select(UserModel).where(UserModel.id == str(user_id))
    result = await query_response(query, db)
    if result:
        return await update_user_table(str(user_id), update_useinfo, db)
    else:
        raise HTTPException(status_code=200, detail=400)
    
async def apply_party(
        jwToken: Annotated[str | None, Header(convert_underscores=False)],
        hosting_id:int,
        db: AsyncSession = Depends(get_db)
):
    status = await check_applicants(hosting_id, db)
    if status:
        user_id = await jwt_token2user_id(jwToken)
        user_query = select(UserModel).where(UserModel.id == str(user_id))
        hosting_query = select(HostingModel).where(HostingModel.hosting_id == hosting_id)
        user_info = await query_response(user_query, db)
        hosting_info = await query_response(hosting_query, db)
        data = await making_participation(user_info[0], hosting_info[0])
        if data:
            db.add(data)
            await db.commit()
            await add_current_person(hosting_id, db)
            return 'Success Apply'
        else:
            raise HTTPException(status_code=200, detail=400)
    else:
        raise HTTPException(status_code=200, detail={'status_code':400, 'message':'신청인원마감'})

async def read_partylist(
        jwToken: Annotated[str | None, Header(convert_underscores=False)],
        db: AsyncSession = Depends(get_db)
):
    hosting_list = []
    user_id = await jwt_token2user_id(jwToken)
    print(user_id)
    _query = select(ParticipationModel.hosting_id).where(ParticipationModel.id == str(user_id), ParticipationModel.delete_state == False, ParticipationModel.hosting_date > datetime.now())
    hosting_id_list = await query_response(_query, db)
    if hosting_id_list:
        for hosting_id in hosting_id_list:
            hosting = await read_hosting_tables(hosting_id, True, db)      
            hosting_list.append(hosting)
        return hosting_list
    else:
        raise HTTPException(status_code=200, detail={'detail':400, 'message':'예약내역이 없습니다.'})
    
    
async def read_party(
        jwToken: Annotated[str | None, Header(convert_underscores=False)],
        hosting_id: int,
        db: AsyncSession = Depends(get_db)
):
    user_id = await jwt_token2user_id(jwToken)
    query = select(UserModel).where(UserModel.id == str(user_id))
    result = (await query_response_one(query, db)).one_or_none()
    if result:
        hosting_table = await read_hosting_table(hosting_id, db)
        hosting_table['full_applicants'] = await check_applicants(hosting_id, db)
        return await read_hosting_table(hosting_id, db)
    else:
        raise HTTPException(status_code=200, detail={'detail':400, 'message':'jwtoken값이 유효하지않습니다.'})

async def delete_party(
        jwToken: Annotated[str | None, Header(convert_underscores=False)],
        hosting_id: int,
        db: AsyncSession = Depends(get_db)
):
    user_id = await jwt_token2user_id(jwToken)
    query = select(UserModel).where(UserModel.id == str(user_id))
    result = (await query_response_one(query, db)).one_or_none()
    if result:
        return await delete_party_table(hosting_id, db)
    else:
        raise HTTPException(status_code=200, detail={'detail':400, 'message':'jwtoken값이 유효하지않습니다.'})

    
async def delete_user(
    jwtToken: Annotated[str | None, Header(convert_underscores=False)],
    db: AsyncSession = Depends(get_db)
):
    user_id = await jwt_token2user_id(jwtToken)
    business_no = await get_business_no(str(user_id), db)
    query = select(UserModel.role).where(UserModel.id == str(user_id))
    result = (await query_response_one(query, db)).one_or_none()
    if result == 'host':
        query_hosting = delete(HostingModel).where(HostingModel.business_no == business_no)
        await delete_response(query_hosting, db)
        query_store = delete(StoreModel).where(StoreModel.id == str(user_id))
        await delete_response(query_store, db)
    _query = update(UserModel).where(UserModel.id == str(user_id)).values({
        UserModel.delete_state : True
    })
    return await update_response(_query, db)
        