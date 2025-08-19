from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AsetKeluargaBase(BaseModel):
    keluarga_id: int
    penguasaan_aset_tanah: Optional[str] = None
    aset_sarana_transportasi_umum: Optional[str] = None
    aset_sarana_produksi: Optional[str] = None
    aset_lainnya: Optional[str] = None


class AsetKeluargaCreate(AsetKeluargaBase):
    pass


class AsetKeluargaUpdate(BaseModel):
    penguasaan_aset_tanah: Optional[str] = None
    aset_sarana_transportasi_umum: Optional[str] = None
    aset_sarana_produksi: Optional[str] = None
    aset_lainnya: Optional[str] = None


class AsetKeluargaOut(AsetKeluargaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
