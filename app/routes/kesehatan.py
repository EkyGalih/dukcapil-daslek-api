from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.kesehatan import Kesehatan
from app.schemas.kesehatan import (
    KesehatanCreate, KesehatanUpdate, KesehatanOut
)
from . import get_or_404

router = APIRouter(prefix="/kesehatans", tags=["Kesehatans"])


@router.get("/", response_model=list[KesehatanOut])
async def list_kesehatans(
    db: AsyncSession = Depends(get_db)
):
    res = await db.execute(select(Kesehatan))
    return res.scalars().all()


@router.get("/{id}", response_model=KesehatanOut)
async def get_kesehatan(
    id: int, db: AsyncSession = Depends(get_db)
):
    return await get_or_404(db, Kesehatan, id)


@router.post("/", response_model=KesehatanOut, status_code=201)
async def create_kesehatan(
    payload: KesehatanCreate, db: AsyncSession = Depends(get_db)
):
    obj = Kesehatan(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{id}", response_model=KesehatanOut)
async def update_kesehatan(
    id: int, payload: KesehatanUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await get_or_404(db, Kesehatan, id)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
async def delete_kesehatan(
    id: int, db: AsyncSession = Depends(get_db)
):
    obj = await get_or_404(db, Kesehatan, id)
    await db.delete(obj)
    await db.commit()
