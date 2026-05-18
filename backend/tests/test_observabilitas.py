"""Tes fasad observabilitas (tanpa mengirim ke Sentry)."""

from __future__ import annotations

from src.observabilitas.fasad import pasang_observabilitas_runtime, ringkas_status_observabilitas
from tests.pengaturan_uji import buat_pengaturan_uji


def test_ringkas_status_tanpa_dsn() -> None:
    pengaturan = buat_pengaturan_uji(dsn_sentry=None)
    assert ringkas_status_observabilitas(pengaturan) == "tidak_aktif"


def test_ringkas_status_dengan_dsn() -> None:
    pengaturan = buat_pengaturan_uji(dsn_sentry="https://contoh@sentry.io/1")
    assert ringkas_status_observabilitas(pengaturan) == "sentry"


def test_pasang_tidak_melempar_tanpa_dsn() -> None:
    pengaturan = buat_pengaturan_uji(dsn_sentry=None)
    pasang_observabilitas_runtime(pengaturan)
