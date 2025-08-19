from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class PendudukBase(BaseModel):
    keluarga_id: int
    urutan_nik: Optional[int] = None
    nik: Optional[str] = None
    nama_lengkap: Optional[str] = None
    jenis_kelamin: Optional[str] = None
    tempat_lahir: Optional[str] = None
    tanggal_lahir: Optional[date] = None
    agama: Optional[str] = None
    status_pernikahan: Optional[str] = None
    duda_janda: Optional[str] = None
    golongan_darah: Optional[str] = None
    pekerjaan: Optional[str] = None
    nama_ayah: Optional[str] = None
    nama_ibu: Optional[str] = None
    hubungan_dalam_keluarga: Optional[str] = None


class PendudukCreate(PendudukBase):
    pass


class PendudukUpdate(PendudukBase):
    urutan_nik: Optional[int] = None
    nik: Optional[str] = None
    nama_lengkap: Optional[str] = None
    jenis_kelamin: Optional[str] = None
    tempat_lahir: Optional[str] = None
    tanggal_lahir: Optional[date] = None
    agama: Optional[str] = None
    status_pernikahan: Optional[str] = None
    duda_janda: Optional[str] = None
    golongan_darah: Optional[str] = None
    pekerjaan: Optional[str] = None
    nama_ayah: Optional[str] = None
    nama_ibu: Optional[str] = None
    hubungan_dalam_keluarga: Optional[str] = None


class PendudukOut(PendudukBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
