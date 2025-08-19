from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from app.database import Base


class Pendataan(Base):
    __tablename__ = "pendataans"

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
        index=True, nullable=False
    )

    completion_time = Column(DateTime, nullable=True)
    pendata = Column(String, nullable=True)

    penduduk = relationship("Penduduk", back_populates="pendataans")
