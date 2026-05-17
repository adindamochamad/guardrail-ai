"""Fixture pytest: paksa DB in-memory sebelum modul aplikasi pertama kali diimpor."""

import os

# Wajib dijalankan sebelum import `src.*` agar singleton engine menunjuk SQLite memori.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient

from src.database import BasisModel, mesin_database
from src.main import app


@pytest.fixture(autouse=True)
def reset_skema_tiap_tes() -> None:
    """Mencegah tes saling mempengaruhi pada satu engine SQLite in-memory."""

    BasisModel.metadata.drop_all(bind=mesin_database)
    BasisModel.metadata.create_all(bind=mesin_database)
    yield


@pytest.fixture
def klien_api() -> TestClient:
    """Klien HTTP sinkron untuk endpoint FastAPI."""

    with TestClient(app) as klien:
        yield klien


@pytest.fixture(autouse=True)
def bersihkan_override_dependensi() -> None:
    """Pastikan `dependency_overrides` tidak bocor antar-tes."""

    yield
    app.dependency_overrides.clear()
