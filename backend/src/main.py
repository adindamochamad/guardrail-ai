"""Aplikasi FastAPI GuardRail AI — Day 1–4: deteksi, analisis, Buildkite webhook."""

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .config import dapatkan_pengaturan
from .database import BasisModel, dapatkan_sesi_db, mesin_database
from .models import CodeFile, Scan  # noqa: F401 — memastikan metadata ORM terdaftar
from .routes import analisis_risiko as rute_analisis
from .routes import buildkite_webhook as rute_buildkite
from .routes import deteksi as rute_deteksi


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Buat skema tabel saat startup (MVP dev; produksi pakai migrasi terpisah)."""

    BasisModel.metadata.create_all(bind=mesin_database)
    yield


pengaturan_aplikasi = dapatkan_pengaturan()

app = FastAPI(
    title=pengaturan_aplikasi.nama_aplikasi,
    version="0.4.0",
    lifespan=lifespan,
)

app.include_router(rute_deteksi.router)
app.include_router(rute_analisis.router)
app.include_router(rute_buildkite.router)


@app.get("/health", tags=["kesehatan"])
def baca_kesehatan() -> dict[str, str]:
    """Endpoint ringan untuk smoke test dan orkestrasi kontainer."""

    return {
        "status": "ok",
        "service": pengaturan_aplikasi.nama_aplikasi,
    }


@app.get("/db/ping", tags=["kesehatan"])
def periksa_database(
    sesi: Annotated[Session, Depends(dapatkan_sesi_db)],
) -> dict[str, str | int]:
    """Memastikan koneksi ORM dan tabel terbaca; berguna untuk debugging Day 1."""

    jumlah_scan = sesi.execute(select(func.count(Scan.id))).scalar_one()
    jumlah_berkas = sesi.execute(select(func.count(CodeFile.id))).scalar_one()
    return {
        "status": "ok",
        "scans_count": jumlah_scan,
        "code_files_count": jumlah_berkas,
    }


__all__ = ["app"]
