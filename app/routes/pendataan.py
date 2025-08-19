from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.pendataan import Pendataan
from app.schemas.pendataan import (
    PendataanCreate, PendataanUpdate, PendataanOut
)
from . import get_or_404

router = APIRouter(prefix="/pendataans", tags=["Pendataans"])


@router.get("/", response_model=list[PendataanOut])
async def list_pendataan(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Pendataan))
    return res.scalars().all()


@router.get("/{id}", response_model=PendataanOut)
async def get_pendataan(
    id: int, db: AsyncSession = Depends(get_db)
):
    return await get_or_404(db, Pendataan, id)


@router.post("/", response_model=PendataanOut, status_code=201)
async def create_pendataan(
    payload: PendataanCreate, db: AsyncSession = Depends(get_db)
):
    obj = Pendataan(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{id}", response_model=PendataanOut)
async def update_pendataan(
    id: int, payload: PendataanUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await get_or_404(db, Pendataan, id)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
async def delete_pendataan(id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_or_404(db, Pendataan, id)
    await db.delete(obj)
    await db.commit()
