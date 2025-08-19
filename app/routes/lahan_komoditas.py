from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.lahan_komoditas import LahanKomoditas
from app.schemas.lahan_komoditas import (
    LahanKomoditasCreate, LahanKomoditasUpdate, LahanKomoditasOut
)
from . import get_or_404

router = APIRouter(prefix="/lahan-komoditas", tags=["Lahan Komoditas"])


@router.get("/", response_model=list[LahanKomoditasOut])
async def list_lahan(
    db: AsyncSession = Depends(get_db),
    keluarga_id: int | None = None,
    kategori: str | None = Query(default=None)
):
    stmt = select(LahanKomoditas)
    if keluarga_id:
        stmt = stmt.where(LahanKomoditas.keluarga_id == keluarga_id)
    if kategori:
        stmt = stmt.where(LahanKomoditas.kategori == kategori)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get("/{id}", response_model=LahanKomoditasOut)
async def get_lahan(id: int, db: AsyncSession = Depends(get_db)):
    return await get_or_404(db, LahanKomoditas, id)


@router.post("/", response_model=LahanKomoditasOut, status_code=201)
async def create_lahan(
    payload: LahanKomoditasCreate, db: AsyncSession = Depends(get_db)
):
    obj = LahanKomoditas(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{id}", response_model=LahanKomoditasOut)
async def update_lahan(
    id: int, payload: LahanKomoditasUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await get_or_404(db, LahanKomoditas, id)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
async def delete_lahan(id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_or_404(db, LahanKomoditas, id)
    await db.delete(obj)
    await db.commit()
