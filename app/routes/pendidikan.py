from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.pendidikan import Pendidikan
from app.schemas.pendidikan import (
    PendidikanCreate, PendidikanUpdate, PendidikanOut
)
from . import get_or_404

router = APIRouter(prefix="/pendidikans", tags=["Pendidikans"])


@router.get("/", response_model=list[PendidikanOut])
async def list_pendidikans(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Pendidikan))
    return res.scalars().all()


@router.get("/{id}", response_model=PendidikanOut)
async def get_pendidikan(
    id: int, db: AsyncSession = Depends(get_db)
):
    return await get_or_404(db, Pendidikan, id)


@router.post("/", response_model=PendidikanOut, status_code=201)
async def create_pendidikan(
    payload: PendidikanCreate, db: AsyncSession = Depends(get_db)
):
    obj = Pendidikan(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{id}", response_model=PendidikanOut)
async def update_pendidikan(
    id: int, payload: PendidikanUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await get_or_404(db, Pendidikan, id)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
async def delete_pendidikan(
    id: int, db: AsyncSession = Depends(get_db)
):
    obj = await get_or_404(db, Pendidikan, id)
    await db.delete(obj)
    await db.commit()
