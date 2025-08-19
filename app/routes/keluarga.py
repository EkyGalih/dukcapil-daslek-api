from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.keluarga import Keluarga
from app.schemas.keluarga import KeluargaCreate, KeluargaUpdate, KeluargaOut
from . import get_or_404
from app.auth.security import get_current_user
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/keluargas", tags=["Keluargas"])


@router.get("/", response_model=list[KeluargaOut])
async def list_keluargas(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Keluarga))
    return res.scalars().all()


@router.get("/{id}", response_model=KeluargaOut)
async def get_keluarga(id: int, db: AsyncSession = Depends(get_db)):
    return await get_or_404(db, Keluarga, id)


@router.post("/", response_model=KeluargaOut, status_code=201)
async def create_keluarga(
    payload: KeluargaCreate,
    db: AsyncSession = Depends(get_db)
):
    obj = Keluarga(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{id}", response_model=KeluargaOut)
async def update_keluarga(
    id: int,
    payload: KeluargaUpdate,
    db: AsyncSession = Depends(get_db)
):
    obj = await get_or_404(db, Keluarga, id)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
async def delete_keluarga(id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_or_404(db, Keluarga, id)
    await db.delete(obj)
    await db.commit()


@router.get("/{id}/detail")
async def get_keluarga_detail(
    id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)
):
    stmt = (
        select(Keluarga)
        .where(Keluarga.id == id)
        .options(
            selectinload(Keluarga.penduduks),
            selectinload(Keluarga.aset_list),
            selectinload(Keluarga.lahan_list)
        )
    )
    res = await db.execute(stmt)
    keluarga = res.scalar_one_or_none()
    if not keluarga:
        raise HTTPException(status_code=404, detail="keluargas not found")
    # bentuk response manual (biar rapi)
    return {
        "id": keluarga.id,
        "nomor": keluarga.nomor,
        "nomor_kk": keluarga.nomor_kk,
        "nama_kepala_keluarga": keluarga.nama_kepala_keluarga,
        "dusun": keluarga.dusun,
        "rw": keluarga.rw,
        "rt": keluarga.rt,
        "nomor_rumah": keluarga.nomor_rumah,
        "status_kepemilikan_rumah": keluarga.status_kepemilikan_rumah,
        "luas_lantai_m2": keluarga.luas_lantai_m2,
        "dinding_rumah": keluarga.dinding_rumah,
        "lantai_rumah": keluarga.lantai_rumah,
        "atap_rumah": keluarga.atap_rumah,
        "status_kepemilikan_lahan_rumah":
            keluarga.status_kepemilikan_lahan_rumah,
        "luas_lahan_rumah_m2": keluarga.luas_lahan_rumah_m2,
        "penerima_bantuan": keluarga.penerima_bantuan,
        "penduduks": [
            {
                "id": p.id,
                "nik": p.nik,
                "nama_lengkap": p.nama_lengkap,
                "jenis_kelamin": p.jenis_kelamin,
                "tanggal_lahir": p.tanggal_lahir,
                "agama": p.agama,
                "status_pernikahan": p.status_pernikahan,
                "hubungan_dalam_keluarga": p.hubungan_dalam_keluarga,
            }
            for p in keluarga.penduduks
        ],
        "aset_keluargas": [
            {
                "id": a.id,
                "penguasaan_aset_tanah": a.penguasaan_aset_tanah,
                "aset_sarana_transportasi_umum":
                    a.aset_sarana_transportasi_umum,
                "aset_sarana_produksi": a.aset_sarana_produksi,
                "aset_lainnya": a.aset_lainnya,
            }
            for a in keluarga.aset_list
        ],
        "lahan_komoditas": [
            {
                "id": lahan.id,
                "kategori": lahan.kategori,
                "memiliki": lahan.memiliki,
                "luas_lahan_are": lahan.luas_lahan_are,
                "jenis_komoditas": lahan.jenis_komoditas,
                "produksi": lahan.produksi,
                "satuan_produksi": lahan.satuan_produksi,
                "nilai_produksi": lahan.nilai_produksi,
                "pemasaran": lahan.pemasaran,
            }
            for lahan in keluarga.lahan_list
        ],
    }
