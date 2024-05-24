from typing import Any
from sqlalchemy import ScalarResult, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


async def data_in_db(table: Any, attr:str,compare:Any, db: AsyncSession)-> bool:
    _query = select(type(table)).where(getattr(type(table),attr) == compare)

    
async def query_response_one(query: select, db: AsyncSession) -> ScalarResult:
    async with db as session:
        result = await session.execute(query)
        return result.scalars()

    
async def query_response(query: select, db: AsyncSession) -> ScalarResult:
    async with db as session:
        result = await session.execute(query)
        all_results = result.scalars().all()  # 변경된 부분
        
        # 데이터 출력
        for row in all_results:
            print(row)
        
        # ScalarResult 반환
        return all_results

async def update_response(query: update, db: AsyncSession):
    async with db as session:
        await session.execute(query)
        await session.commit()
    
async def delete_response(query: delete, db: AsyncSession):
    async with db as session:
        await session.execute(query)
        await session.commit()
