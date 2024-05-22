from typing import Any
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession


async def data_in_db(table: Any, attr:str,compare:Any, db: AsyncSession)-> bool:
    _query = select(type(table)).where(getattr(type(table),attr) == compare)

    
async def query_response(query: select, db: AsyncSession) -> ScalarResult:
    async with db as session:
        result = await session.execute(query)
        return result.scalars()
