from datetime import datetime

from database.search_query import query_response, update_response
from fastapi import HTTPException
from models.hosting_table import HostingModel
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from routes.hosting.models.hosting_models import HostinginsertModel
from routes.host.api_helper import host_update_image  
# Hosting 테이블에 insert 하는 함수 CQRS : Create
async def insert_hosting_table(hostingModel: HostinginsertModel, db: AsyncSession) -> bool:
    try:
        hostings = HostingModel(
            hosting_name=hostingModel.hosting_name,
            business_no=hostingModel.business_no,
            introduce=hostingModel.introduce,
            current_personnel=hostingModel.current_personnel,
            max_personnel=hostingModel.max_personnel,
            age_group_start=hostingModel.age_group_start,
            hosting_data=hostingModel.hosting_data,
        )
        print(hostings)
        db.add(hostings)
        await db.commit()
        return True
    except:
        raise HTTPException(status_code=200, detail=400)


# Hosting 테이블에서 사업자번호로 Read 하는 함수 CQRS : Read
async def read_hosting_tables(hosting_name: str, db: AsyncSession) -> HostingModel:
    _query = select(HostingModel).where(
        HostingModel.business_no == hosting_name,
        HostingModel.active_state == True,
        HostingModel.delete_state == False,
    )
    responses = (await query_response(_query, db))
    if responses:
        hosting_list =[]
        # 객체의 컬럼 값을 가져오기
        for response in responses:
            #response = response[0]
            hosting_list.append({
                "hosting_name": response.hosting_name,
                "business_no": response.business_no,
                "introduce": response.introduce,
                "cur_personnel": response.cur_personnel,
                "max_personnel": response.max_personnel,
                "age_group_start": response.age_group_start,
                "age_group_end": response.age_group_end,
                "game_start_date": response.game_start_date,
            })
        return hosting_list
    else:
        raise HTTPException(status_code=200, detail=400)

# Hosting 테이블에서 hosting_id로 Read 하는 함수 CQRS : Read
async def read_hosting_table(hosting_id: str, db: AsyncSession) -> HostingModel:
    _query = select(HostingModel).where(
        HostingModel.hosting_id == hosting_id,
        HostingModel.active_state == True,
        HostingModel.delete_state == False,
    )
    response = (await query_response(_query, db))
    if response:
        response = response[0]
        hosting_list={
            "hosting_name": response.hosting_name,
            "business_no": response.business_no,
            "introduce": response.introduce,
            "cur_personnel": response.cur_personnel,
            "max_personnel": response.max_personnel,
            "age_group_start": response.age_group_start,
            "age_group_end": response.age_group_end,
            "game_start_date": response.game_start_date,
        }
        return hosting_list
    else:
        raise HTTPException(status_code=200, detail=400)
    
async def delete_hosting_table(hosting_id: int, db: AsyncSession):
    value = {
        HostingModel.active_state : False,
        HostingModel.delete_state : True
    }
    _query = update(HostingModel).where(HostingModel.hosting_id == hosting_id).values(value)
    await update_response(_query,db)

async def update_hosting_table(hosting_id: int, db: AsyncSession):
    value = {
        HostingModel.active_state : False,
        HostingModel.delete_state : True
    }
    _query = update(HostingModel).where(HostingModel.hosting_id == hosting_id).values(value)
    await update_response(_query,db)