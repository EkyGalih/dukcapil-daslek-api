from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PendidikanBase(BaseModel):
    penduduk_id: int
    pendidikan_terakhir: Optional[str] = None
    pendidikan_sedang_ditempuh: Optional[str] = None


class PendidikanCreate(PendidikanBase):
    pass


class PendidikanUpdate(BaseModel):
    pendidikan_terakhir: Optional[str] = None
    pendidikan_sedang_ditempuh: Optional[str] = None


class PendidikanOut(PendidikanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
