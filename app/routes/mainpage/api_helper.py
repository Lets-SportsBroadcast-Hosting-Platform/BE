from database.search_query import query_response
from fastapi import HTTPException
from models.hosting_table import HostingModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# Hosting 테이블에서 사업자번호로 Read 하는 함수 CQRS : Read
async def read_hosting_tables(db: AsyncSession) -> HostingModel:
    _query = select(HostingModel).where(
        HostingModel.active_state == True,
        HostingModel.delete_state == False,
    )
    responses = await query_response(_query, db)
    if responses:
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
        ]
    else:
        raise HTTPException(status_code=200, detail=400)
