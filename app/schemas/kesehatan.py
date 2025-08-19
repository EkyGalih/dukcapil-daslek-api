from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class KesehatanBase(BaseModel):
    penduduk_id: int
    jaminan_sosial_ketenagakerjaan: Optional[str] = None
    jaminan_sosial_kesehatan: Optional[str] = None
    penyakit_sedang_diderita: Optional[str] = None
    penyakit_kelainan: Optional[str] = None
    cacat_fisik: Optional[str] = None
    cacat_mental: Optional[str] = None
    ibu_hamil_melahirkan: Optional[bool] = None
    kualitas_ibu_hamil: Optional[str] = None
    tempat_persalinan: Optional[str] = None
    pertolongan_persalinan: Optional[str] = None
    kualitas_bayi: Optional[str] = None
    cakupan_imunisasi: Optional[str] = None
    status_gizi_balita: Optional[str] = None
    perilaku_hidup_bersih: Optional[str] = None
    pola_makan: Optional[str] = None
    kebiasaan_berobat: Optional[str] = None


class KesehatanCreate(KesehatanBase):
    pass


class KesehatanUpdate(KesehatanBase):
    pass


class KesehatanOut(KesehatanBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
