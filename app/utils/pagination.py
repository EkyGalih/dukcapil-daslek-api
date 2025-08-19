from math import ceil
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def paginate(db: AsyncSession, stmt, page: int = 1, size: int = 20):
    page = max(1, page)
    size = max(1, min(100, size))
    total = (
        await db.execute(select(func.count()).select_from(stmt.subquery()))
    ).scalar()
    rows = (
        await db.execute(stmt.limit(size).offset((page-1)*size))
    ).scalars().all()
    return {
        "items": rows,
        "total": total or 0,
        "page": page,
        "size": size,
        "pages": ceil((total or 0)/size) if total else 0
    }
