from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import (
    auth,
    keluarga,
    penduduk,
    pendidikan,
    kesehatan,
    aset_keluarga,
    lahan_komoditas,
    pendataan
)

app = FastAPI(title="API Pendataan", version="1.0.0")

# === CORS Middleware ===
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# include routers
app.include_router(auth.router)
app.include_router(keluarga.router)
app.include_router(penduduk.router)
app.include_router(pendidikan.router)
app.include_router(kesehatan.router)
app.include_router(aset_keluarga.router)
app.include_router(lahan_komoditas.router)
app.include_router(pendataan.router)


# optional: create tables automatically (untuk deb; produksi pakai Alembic)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
