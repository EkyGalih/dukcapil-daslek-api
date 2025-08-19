from sqlalchemy import (
    BigInteger, Column, ForeignKey, Integer, String, Boolean,
    DateTime, func
)
from sqlalchemy.orm import relationship
from app.database import Base


class LahanKomoditas(Base):
    __tablename__ = "lahan_komoditas"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    keluarga_id = Column(
        BigInteger,
        ForeignKey("keluargas.id", ondelete="CASCADE"),
        index=True, nullable=False
    )

    # tanaman_pangan, perkebunan, buah, obat, hutan, ternak, perikanan
    # galian, pengolahan_ternak
    kategori = Column(String, nullable=False)
    memiliki = Column(Boolean, nullable=True)
    luas_lahan_are = Column(Integer, nullable=True)
    jenis_komoditas = Column(String, nullable=True)
    produksi = Column(Integer, nullable=True)
    satuan_produksi = Column(String, nullable=True)
    nilai_produksi = Column(BigInteger, nullable=True)
    pemasaran = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    keluarga = relationship(
        "Keluarga",
        back_populates="lahan_list"
    )
