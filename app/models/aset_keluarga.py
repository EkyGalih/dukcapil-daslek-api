from sqlalchemy import BigInteger, Column, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class AsetKeluarga(Base):
    __tablename__ = "aset_keluargas"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    keluarga_id = Column(
        BigInteger,
        ForeignKey("keluargas.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )

    penguasaan_aset_tanah = Column(String, nullable=True)
    aset_sarana_transportasi_umum = Column(String, nullable=True)
    aset_sarana_produksi = Column(String, nullable=True)
    aset_lainnya = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    keluarga = relationship("Keluarga", back_populates="aset_list")
