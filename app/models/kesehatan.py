from sqlalchemy import (
    BigInteger, Boolean, Column, ForeignKey, String,
    DateTime, func
)
from sqlalchemy.orm import relationship
from app.database import Base


class Kesehatan(Base):
    __tablename__ = "kesehatans"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    penduduk_id = Column(
        BigInteger,
        ForeignKey("penduduks.id", ondelete="CASCADE"),
        unique=True, nullable=False
    )

    jaminan_sosial_ketenagakerjaan = Column(String, nullable=True)
    jaminan_sosial_kesehatan = Column(String, nullable=True)
    penyakit_sedang_diderita = Column(String, nullable=True)
    penyakit_kelainan = Column(String, nullable=True)
    cacat_fisik = Column(String, nullable=True)
    cacat_mental = Column(String, nullable=True)
    ibu_hamil_melahirkan = Column(Boolean, nullable=True)
    kualitas_ibu_hamil = Column(String, nullable=True)
    tempat_persalinan = Column(String, nullable=True)
    pertolongan_persalinan = Column(String, nullable=True)
    kualitas_bayi = Column(String, nullable=True)
    cakupan_imunisasi = Column(String, nullable=True)
    status_gizi_balita = Column(String, nullable=True)
    perilaku_hidup_bersih = Column(String, nullable=True)
    pola_makan = Column(String, nullable=True)
    kebiasaan_berobat = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    penduduk = relationship("Penduduk", back_populates="kesehatan")
