"""Engine SQLAlchemy, session factory, dan Base ORM."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from .config import dapatkan_pengaturan

pengaturan_koneksi = dapatkan_pengaturan()

_apakah_sqlite_memori = pengaturan_koneksi.url_database.startswith(
    "sqlite:///:memory",
)

if _apakah_sqlite_memori:
    # Satu koneksi dibagikan; tanpa ini setiap checkout pool = DB memori kosong baru.
    mesin_database = create_engine(
        pengaturan_koneksi.url_database,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    _argumen_sambungan_sqlite = (
        {"check_same_thread": False}
        if pengaturan_koneksi.url_database.startswith("sqlite")
        else {}
    )
    mesin_database = create_engine(
        pengaturan_koneksi.url_database,
        connect_args=_argumen_sambungan_sqlite,
    )

pembuat_sesi = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=mesin_database,
)


class BasisModel(DeclarativeBase):
    """Base declarative untuk semua model Day 1."""


def dapatkan_sesi_db() -> Generator[Session, None, None]:
    """Menyediakan sesi DB per-request; tutup otomatis setelah selesai."""

    sesi_basis_data = pembuat_sesi()
    try:
        yield sesi_basis_data
    finally:
        sesi_basis_data.close()
