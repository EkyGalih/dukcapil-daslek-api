from sqlalchemy import (
    BigInteger, Column, Integer, String, Date, ForeignKey,
    DateTime, func
)
from sqlalchemy.orm import relationship
from app.database import Base


class Penduduk(Base):
    __tablename__ = "penduduks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    keluarga_id = Column(
        BigInteger,
        ForeignKey("keluargas.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )

    urutan_nik = Column(Integer, nullable=True)
    nik = Column(String, nullable=True, index=True)
    nama_lengkap = Column(String, nullable=True)
    jenis_kelamin = Column(String, nullable=True)
    tempat_lahir = Column(String, nullable=True)
    tanggal_lahir = Column(Date, nullable=True)
    agama = Column(String, nullable=True)
    status_pernikahan = Column(String, nullable=True)
    duda_janda = Column(String, nullable=True)
    golongan_darah = Column(String, nullable=True)
    pekerjaan = Column(String, nullable=True)
    nama_ayah = Column(String, nullable=True)
    nama_ibu = Column(String, nullable=True)
    hubungan_dalam_keluarga = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    keluarga = relationship("Keluarga", back_populates="penduduks")
    pendidikan = relationship(
        "Pendidikan",
        back_populates="penduduk", uselist=False, cascade="all, delete-orphan"
    )
    kesehatan = relationship(
        "Kesehatan",
        back_populates="penduduk", uselist=False, cascade="all, delete-orphan"
    )
    pendataans = relationship(
        "Pendataan",
        back_populates="penduduk", cascade="all, delete-orphan"
    )
