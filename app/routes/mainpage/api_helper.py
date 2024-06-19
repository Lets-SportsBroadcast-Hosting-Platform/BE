from database.search_query import query_response
from fastapi import HTTPException
from models.hosting_table import HostingModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

# Hosting 테이블에서 사업자번호로 Read 하는 함수 CQRS : Read
async def read_hosting_tables(db: AsyncSession) -> HostingModel:
    _query = select(HostingModel).where(
        HostingModel.active_state == True,
        HostingModel.delete_state == False
    ).order_by(HostingModel.hosting_date.asc())
    responses = await query_response(_query, db)
    
    if responses:
        for response in responses:
            if response.hosting_date > datetime.now():
                _query = update(HostingModel).where(
                    HostingModel.hosting_id == response.hosting_id
                ).values(
                    {
                        HostingModel.active_state : False,
                        HostingModel.delete_state: True
                    }
                )
        # 객체의 컬럼 값을 가져오기
        return [
            {
                "hosting_id": response.hosting_id,
                "hosting_name": response.hosting_name,
                "business_no": response.business_no,
                "introduce": response.introduce,
                "current_personnel": response.current_personnel,
                "max_personnel": response.max_personnel,
                "age_group_min": response.age_group_min,
                "age_group_max": response.age_group_max,
                "hosting_date": response.hosting_date,
            }
            for response in responses
            if response.hosting_date > datetime.now()
        ]
    else:
        return []
