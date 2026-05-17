"""Tes HTTP untuk webhook Buildkite."""

from __future__ import annotations

import json
from unittest.mock import patch

from fastapi.testclient import TestClient
from src.config import dapatkan_pengaturan
from src.main import app
from tests.pengaturan_uji import buat_pengaturan_uji


def _muatan_build_ringkas() -> dict[str, object]:
    """Payload minimal mirip event pipeline (tanpa klon Git)."""

    return {
        "event": "build.finished",
        "build": {
            "number": 7,
            "message": (
                "chore: contoh\n\n"
                "def foo():\n"
                "    subprocess.call('ls', shell=True)\n"
            ),
            "state": "passed",
        },
        "pipeline": {"slug": "demo-pipa", "repository": ""},
        "organization": {"slug": "acme-org"},
    }


def test_webhook_503_tanpa_token_konfigurasi() -> None:
    # Override memastikan perilaku sama walau `.env` lokal punya BUILDKITE_WEBHOOK_TOKEN.
    app.dependency_overrides[dapatkan_pengaturan] = lambda: buat_pengaturan_uji(
        token_webhook_buildkite=None,
        izinkan_webhook_tanpa_verifikasi=False,
    )
    with TestClient(app) as klien:
        badan_bytes = json.dumps({"event": "ping"}).encode("utf-8")
        balasan = klien.post("/webhooks/buildkite", content=badan_bytes)
    assert balasan.status_code == 503


def test_webhook_401_token_salah() -> None:
    app.dependency_overrides[dapatkan_pengaturan] = lambda: buat_pengaturan_uji(
        token_webhook_buildkite="benar",
    )
    with TestClient(app) as klien:
        balasan = klien.post(
            "/webhooks/buildkite",
            content=b'{"event":"ping"}',
            headers={"X-Buildkite-Token": "salah"},
        )
    assert balasan.status_code == 401


def test_webhook_400_json_tidak_valid() -> None:
    app.dependency_overrides[dapatkan_pengaturan] = lambda: buat_pengaturan_uji(
        izinkan_webhook_tanpa_verifikasi=True,
    )
    with TestClient(app) as klien:
        balasan = klien.post("/webhooks/buildkite", content=b"bukan-json")
    assert balasan.status_code == 400


def test_webhook_200_mode_dev_longgar() -> None:
    app.dependency_overrides[dapatkan_pengaturan] = lambda: buat_pengaturan_uji(
        izinkan_webhook_tanpa_verifikasi=True,
    )
    muatan = _muatan_build_ringkas()
    badan_bytes = json.dumps(muatan).encode("utf-8")
    with TestClient(app) as klien:
        balasan = klien.post("/webhooks/buildkite", content=badan_bytes)
    assert balasan.status_code == 200
    isi = balasan.json()
    assert isi.get("keaslian_webhook") == "dev_tanpa_rahasia"
    assert isi.get("deteksi") is not None
    assert isi.get("anotasi") == "dilewati_token_atau_metadata_tidak_lengkap"


def test_webhook_200_verifikasi_token_header() -> None:
    app.dependency_overrides[dapatkan_pengaturan] = lambda: buat_pengaturan_uji(
        token_webhook_buildkite="rahasia-webhook",
    )
    muatan = _muatan_build_ringkas()
    badan_bytes = json.dumps(muatan).encode("utf-8")
    with TestClient(app) as klien:
        balasan = klien.post(
            "/webhooks/buildkite",
            content=badan_bytes,
            headers={"X-Buildkite-Token": "rahasia-webhook"},
        )
    assert balasan.status_code == 200
    assert balasan.json().get("keaslian_webhook") == "token_ok"


@patch("src.integrasi_buildkite.orkestrator.kirim_anotasi_build")
def test_webhook_mengirim_anotasi_saat_token_api_ada(mock_kirim_annotations) -> None:
    mock_kirim_annotations.return_value = (True, 201, "anotasi_terkirim")

    def pengaturan_dengan_buildkite() -> object:
        return buat_pengaturan_uji(
            token_webhook_buildkite="wh-token",
            token_api_buildkite="api-token",
            slug_organisasi_buildkite="acme-org",
        )

    app.dependency_overrides[dapatkan_pengaturan] = pengaturan_dengan_buildkite

    muatan = _muatan_build_ringkas()
    badan_bytes = json.dumps(muatan).encode("utf-8")
    with TestClient(app) as klien:
        balasan = klien.post(
            "/webhooks/buildkite",
            content=badan_bytes,
            headers={"X-Buildkite-Token": "wh-token"},
        )

    assert balasan.status_code == 200
    isi = balasan.json()
    assert isi.get("anotasi_terkirim") is True
    assert isi.get("anotasi_status_http") == 201
    mock_kirim_annotations.assert_called_once()
    argumen_panggilan = mock_kirim_annotations.call_args.kwargs
    assert argumen_panggilan["slug_organisasi"] == "acme-org"
    assert argumen_panggilan["slug_pipa"] == "demo-pipa"
    assert argumen_panggilan["nomor_build"] == 7
