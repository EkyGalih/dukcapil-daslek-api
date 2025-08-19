from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.aset_keluarga import AsetKeluarga
from app.schemas.aset_keluarga import (
    AsetKeluargaCreate, AsetKeluargaUpdate, AsetKeluargaOut
)
from . import get_or_404

router = APIRouter(prefix="/aset-keluargas", tags=["Aset Keluargas"])


@router.get("/", response_model=list[AsetKeluargaOut])
async def list_aset(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AsetKeluarga))
    return res.scalars().all()


@router.get("/{id}", response_model=AsetKeluargaOut)
async def get_aset(id: int, db: AsyncSession = Depends(get_db)):
    return await get_or_404(db, AsetKeluarga, id)


@router.post("/", response_model=AsetKeluargaOut, status_code=201)
async def create_aset(
    payload: AsetKeluargaCreate, db: AsyncSession = Depends(get_db)
):
    obj = AsetKeluarga(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{id}", response_model=AsetKeluargaOut)
async def update_aset(
    id: int, payload: AsetKeluargaUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await get_or_404(db, AsetKeluarga, id)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
async def delete_aset(id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_or_404(db, AsetKeluarga, id)
    await db.delete(obj)
    await db.commit()
