from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.penduduk import Penduduk
from app.schemas.penduduk import PendudukCreate, PendudukUpdate, PendudukOut
from app.auth.security import get_current_user
from app.utils.pagination import paginate
from . import get_or_404
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/penduduks", tags=["Penduduks"])


@router.get("/", response_model=list[PendudukOut])
async def list_penduduk(
    db: AsyncSession = Depends(get_db),
    # _=Depends(get_current_user),
    keluarga_id: int | None = None,
    nik: str | None = None,
    nama: str | None = None,
    page: int = 1, size: int = 20
):
    stmt = select(Penduduk)
    if keluarga_id:
        stmt = stmt.where(Penduduk.keluarga_id == keluarga_id)
    if nik:
        stmt = stmt.where(Penduduk.nik == nik)
    if nama:
        stmt = stmt.where(Penduduk.nama_lengkap.ilike(f"%{nama}%"))
    data = await paginate(db, stmt, page, size)
    # kalau mau return meta:
    # return data
    return data["items"]


@router.get("/{id}", response_model=PendudukOut)
async def get_penduduk(id: int, db: AsyncSession = Depends(get_db)):
    return await get_or_404(db, Penduduk, id)


@router.post("/", response_model=PendudukOut, status_code=201)
async def create_penduduk(
    payload: PendudukCreate, db: AsyncSession = Depends(get_db)
):
    obj = Penduduk(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{id}", response_model=PendudukOut)
async def update_penduduk(
    id: int, payload: PendudukUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await get_or_404(db, Penduduk, id)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
async def delete_penduduk(
    id: int, db: AsyncSession = Depends(get_db)
):
    obj = await get_or_404(db, Penduduk, id)
    await db.delete(obj)
    await db.commit()


@router.get("/{id}/detail")
async def get_penduduk_detail(
    id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)
):
    stmt = (
        select(Penduduk)
        .where(Penduduk.id == id)
        .options(
            selectinload(Penduduk.pendidikan), selectinload(Penduduk.kesehatan)
        )
    )
    res = await db.execute(stmt)
    p = res.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="penduduks not found")
    return {
        "id": p.id,
        "keluarga_id": p.keluarga_id,
        "nik": p.nik,
        "nama_lengkap": p.nama_lengkap,
        "pendidikan": (
            {
                "id": p.pendidikan.id,
                "pendidikan_terakhir": p.pendidikan.pendidikan_terakhir,
                "pendidikan_sedang_ditempuh":
                    p.pendidikan.pendidikan_sedang_ditempuh,
            }
            if p.pendidikan else None
        ),
        "kesehatan": (
            {
                "id": p.kesehatan.id,
                "jaminan_sosial_kesehatan":
                    p.kesehatan.jaminan_sosial_kesehatan
            }
            if p.kesehatan else None
        ),
    }
