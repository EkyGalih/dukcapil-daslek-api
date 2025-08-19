from sqlalchemy import BigInteger, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Keluarga(Base):
    __tablename__ = "keluargas"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nomor = Column(String, nullable=True)
    nomor_kk = Column(String, nullable=True, index=True)
    nama_kepala_keluarga = Column(String, nullable=True)
    dusun = Column(String, nullable=True)
    rw = Column(String, nullable=True)
    rt = Column(String, nullable=True)
    nomor_rumah = Column(String, nullable=True)
    status_kepemilikan_rumah = Column(String, nullable=True)
    luas_lantai_m2 = Column(Integer, nullable=True)
    dinding_rumah = Column(String, nullable=True)
    lantai_rumah = Column(String, nullable=True)
    atap_rumah = Column(String, nullable=True)
    status_kepemilikan_lahan_rumah = Column(String, nullable=True)
    luas_lahan_rumah_m2 = Column(Integer, nullable=True)
    penerima_bantuan = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    penduduks = relationship(
        "Penduduk",
        back_populates="keluarga",
        cascade="all,delete-orphan"
    )
    aset_list = relationship(
        "AsetKeluarga",
        back_populates="keluarga",
        cascade="all, delete-orphan"
    )
    lahan_list = relationship(
        "LahanKomoditas",
        back_populates="keluarga",
        cascade="all, delete-orphan"
    )
