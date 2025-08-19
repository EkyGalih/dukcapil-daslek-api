from sqlalchemy import (
    BigInteger, Column, ForeignKey, String,
    DateTime, func
)
from sqlalchemy.orm import relationship
from app.database import Base


class Pendidikan(Base):
    __tablename__ = "pendidikans"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    penduduk_id = Column(
        BigInteger,
        ForeignKey("penduduks.id", ondelete="CASCADE"),
        unique=True, nullable=False
    )

    pendidikan_terakhir = Column(String, nullable=True)
    pendidikan_sedang_ditempuh = Column(String, nullable=True)

    penduduk = relationship("Penduduk", back_populates="pendidikan")
