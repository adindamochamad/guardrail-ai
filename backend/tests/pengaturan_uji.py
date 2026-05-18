"""Pabrik pengaturan terisolasi untuk unit test (tanpa membaca `.env` produksi)."""

from __future__ import annotations

from pydantic_settings import PydanticBaseSettingsSource, SettingsConfigDict
from src.config import PengaturanAplikasi


class PengaturanUjiAplikasi(PengaturanAplikasi):
    """Sama seperti produksi, tetapi **hanya** memakai argumen konstruktor (tanpa env / file)."""

    model_config = SettingsConfigDict(
        env_file=None,
        extra="ignore",
        populate_by_name=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[PengaturanUjiAplikasi],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Penting: tanpa ini, variabel OS / `.env` tetap menimpa nilai yang kita set di tes.
        return (init_settings,)


def buat_pengaturan_uji(**nilai_timpa: object) -> PengaturanAplikasi:
    """Mengembalikan `PengaturanAplikasi` dengan default aman untuk uji."""

    dasar: dict[str, object] = {
        "url_database": "sqlite:///:memory:",
        "nama_aplikasi": "uji_guardrail",
        "kunci_openai": None,
        "model_openai": "gpt-4o-mini",
        "ambang_deteksi_ai": 0.55,
        "token_webhook_buildkite": None,
        "izinkan_webhook_tanpa_verifikasi": False,
        "token_api_buildkite": None,
        "slug_organisasi_buildkite": None,
        "webhook_klon_git_otomatis": False,
        "kedalaman_klon_git": 1,
        "dsn_sentry": None,
        "lingkungan_sentry": "development",
        "rasio_sampel_trace_sentry": 0.0,
        "aktifkan_rute_debug_sentry": False,
    }
    dasar.update(nilai_timpa)
    return PengaturanUjiAplikasi(**dasar)
