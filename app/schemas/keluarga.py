from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class KeluargaBase(BaseModel):
    nomor: Optional[str] = None
    nomor_kk: Optional[str] = None
    nama_kepala_keluarga: Optional[str] = None
    dusun: Optional[str] = None
    rw: Optional[str] = None
    rt: Optional[str] = None
    nomor_rumah: Optional[str] = None
    status_kepemilikan_rumah: Optional[str] = None
    luas_lantai_m2: Optional[int] = None
    dinding_rumah: Optional[str] = None
    lantai_rumah: Optional[str] = None
    atap_rumah: Optional[str] = None
    status_kepemilikan_lahan_rumah: Optional[str] = None
    luas_lahan_rumah_m2: Optional[int] = None
    penerima_bantuan: Optional[str] = None


class KeluargaCreate(KeluargaBase):
    pass


class KeluargaUpdate(KeluargaBase):
    pass


class KeluargaOut(KeluargaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
