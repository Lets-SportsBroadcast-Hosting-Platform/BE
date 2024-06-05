import base64
import uuid
from database.search_query import update_response
from fastapi import HTTPException
from models.user_table import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import *
import requests
from database import settings
from models.user_table import Insert_Userinfo
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
    
async def jwt_token2user_id(jwt):
    token = verify_access_token(jwt)
    user_id = uuid.UUID(bytes=base64.b64decode(token.get("auth_token")))
    return user_id

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