from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LahanKomoditasBase(BaseModel):
    keluarga_id: int
    kategori: str
    memiliki: Optional[bool] = None
    luas_lahan_are: Optional[int] = None
    jenis_komoditas: Optional[str] = None
    produksi: Optional[int] = None
    satuan_produksi: Optional[str] = None
    nilai_produksi: Optional[int] = None
    pemasaran: Optional[str] = None


class LahanKomoditasCreate(LahanKomoditasBase):
    pass


class LahanKomoditasUpdate(BaseModel):
    kategori: Optional[str] = None
    memiliki: Optional[bool] = None
    luas_lahan_are: Optional[int] = None
    jenis_komoditas: Optional[str] = None
    produksi: Optional[int] = None
    satuan_produksi: Optional[str] = None
    nilai_produksi: Optional[int] = None
    pemasaran: Optional[str] = None


class LahanKomoditasOut(LahanKomoditasBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
