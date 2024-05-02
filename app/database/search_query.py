from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession


async def query_response(query: select, db: AsyncSession) -> ScalarResult:
    async with db as session:
        result = await session.execute(query)
        return result.scalars()
