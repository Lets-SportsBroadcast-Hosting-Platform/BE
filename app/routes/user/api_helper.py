import base64
import uuid
from datetime import datetime
from database.search_query import update_response, query_response
from fastapi import HTTPException
from models.participation_table import ParticipationModel
from models.hosting_table import HostingModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import *
import requests
from database import settings
from models.user_table import UserModel,Insert_Userinfo,Update_Userinfo
from auth.jwt import verify_access_token
AUTH_URL = 'https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json'
LOCAL_URL = 'https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json'
GEO_URL = 'https://sgisapi.kostat.go.kr/OpenAPI3/addr/geocode.json'
async def search_sgisapi(address: str):
    try:
        body = {
            'consumer_key' : settings.SGISAPI_KEY,
            'consumer_secret' : settings.SGISAPI_SECRET
        }
        response = requests.get(AUTH_URL, data=body) # 인증 accessToken발급

        response = response.json()
        print(response)
        access_token = response['result']['accessToken']
        req = {
            'accessToken':access_token,
            'address' : address
        }
        local_lists = requests.get(GEO_URL, data=req)
        local_lists = local_lists.json()
        print(local_lists)
        code = local_lists['result']['resultdata'][0]["sgg_cd"]

        #code = code[0]["sgg_cd"]
        req = {
            'accessToken':access_token,
            'cd': code
            
        }
        local_lists = requests.get(LOCAL_URL, data=req)
        local_lists = local_lists.json()
        local_lists = local_lists['result']
        result = []
        for local_list in local_lists:
            result.append({
                'addr_name': local_list['addr_name']
            })
        return result
    except:
        raise HTTPException(status_code=200, detail=400) 
    
'''async def jwt_token2user_id(jwt):
    token = verify_access_token(jwt)
    user_id = uuid.UUID(bytes=base64.b64decode(token.get("auth_token")))
    return user_id'''

async def insert_userinfo(id: str, user_info:Insert_Userinfo, db: AsyncSession):
    print('id', id)
    print(user_info.alarm)
    print(user_info.area)
    try:
        value = {
            UserModel.alarm : user_info.alarm,
            UserModel.area : user_info.area
        }
        _query = update(UserModel).where(UserModel.id == id).values(value)
        
        return await update_response(_query, db)
    except:
        raise HTTPException(status_code=200, detail=400)
    
async def making_user(userinfo: UserModel):
    
    result = {
        'name':userinfo.name,
        'age':datetime.now().year-userinfo.birthyear,
        'area':userinfo.area
    }
    return result

async def update_user_table(id:str, update_useinfo:Update_Userinfo, db):
    value = {
        UserModel.name : update_useinfo.name,
        UserModel.birthyear : datetime.now().year - update_useinfo.age,
        UserModel.area : update_useinfo.area
    }
    _query = update(UserModel).where(UserModel.id == id).values(value)
    return await update_response(_query,db)

async def making_participation(user_info: UserModel, hosting_info: HostingModel):
    age_range = f'{hosting_info.age_group_min}-{hosting_info.age_group_max}'
    data = ParticipationModel(
        hosting_id = hosting_info.hosting_id,
        id = user_info.id,
        gender = user_info.gender,
        area = user_info.area,
        introduce = hosting_info.introduce,
        age_range = age_range,
        hosting_date = hosting_info.hosting_date,
        create_time = hosting_info.create_time,
        delete_state = False
    )
    return data

async def read_hosting_tables(hosting_id: int, status: bool, db: AsyncSession) -> HostingModel:
    try:
        diff_status = not status
        _query = select(HostingModel).where(
            HostingModel.hosting_id == hosting_id,
            HostingModel.active_state == status,
            HostingModel.delete_state == diff_status,
        )
        response = (await query_response(_query, db))
        response = response[0]
        hosting_list = {
                    "hosting_id" : response.hosting_id,
                    "hosting_name": response.hosting_name,
                    "business_no": response.business_no,
                    "introduce": response.introduce,
                    "current_personnel": response.current_personnel,
                    "max_personnel": response.max_personnel,
                    "age_group_min": response.age_group_min,
                    "age_group_max": response.age_group_max,
                    "hosting_date": response.hosting_date,
                }
        return hosting_list
    except:
        raise HTTPException(status_code=200, detail=400)
    
async def delete_party_table(hosting_id: int, db: AsyncSession):
    value = {
        ParticipationModel.delete_state : True
    }
    _query = update(ParticipationModel).where(ParticipationModel.hosting_id == hosting_id).values(value)
    return await update_response(_query,db)
    
