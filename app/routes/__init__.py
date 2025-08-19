from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_or_404(db: AsyncSession, model, id: int):
    res = await db.execute(select(model).where(model.id == id))
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(
            status_code=404,
            detail=f"{model.__tablename__} not found"
        )
    return obj
