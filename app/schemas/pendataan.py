from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PendataanBase(BaseModel):
    penduduk_id: int
    completion_time: Optional[datetime] = None
    pendata: Optional[str] = None


class PendataanCreate(PendataanBase):
    pass


class PendataanUpdate(BaseModel):
    completion_time: Optional[datetime] = None
    pendata: Optional[str] = None


class PendataanOut(PendataanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
