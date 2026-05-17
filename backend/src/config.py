"""Konfigurasi aplikasi dari variabel lingkungan (lihat `.env.example`)."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PengaturanAplikasi(BaseSettings):
    """Memuat pengaturan sekali per proses; mendukung file `.env` di folder backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    url_database: str = Field(
        default="sqlite:///./guardrail.db",
        validation_alias="DATABASE_URL",
    )
    nama_aplikasi: str = Field(
        default="GuardRail AI",
        validation_alias="APP_NAME",
    )
    kunci_openai: str | None = Field(
        default=None,
        validation_alias="OPENAI_API_KEY",
    )
    model_openai: str = Field(
        default="gpt-4o-mini",
        validation_alias="OPENAI_MODEL",
    )
    ambang_deteksi_ai: float = Field(
        default=0.55,
        ge=0.0,
        le=1.0,
        validation_alias="AI_DETECT_THRESHOLD",
    )
    # --- Buildkite (Day 4) ---
    token_webhook_buildkite: str | None = Field(
        default=None,
        validation_alias="BUILDKITE_WEBHOOK_TOKEN",
        description="Token webhook (plain) atau rahasia HMAC — sama seperti di UI Buildkite.",
    )
    izinkan_webhook_tanpa_verifikasi: bool = Field(
        default=False,
        validation_alias="BUILDKITE_WEBHOOK_ALLOW_UNVERIFIED",
        description="Hanya untuk dev lokal; matikan di produksi.",
    )
    token_api_buildkite: str | None = Field(
        default=None,
        validation_alias="BUILDKITE_API_TOKEN",
    )
    slug_organisasi_buildkite: str | None = Field(
        default=None,
        validation_alias="BUILDKITE_ORG_SLUG",
    )
    webhook_klon_git_otomatis: bool = Field(
        default=False,
        validation_alias="BUILDKITE_WEBHOOK_GIT_CLONE",
        description="Jika true, git clone ringkas saat webhook (butuh git & jaringan di host).",
    )
    kedalaman_klon_git: int = Field(
        default=1,
        ge=1,
        le=50,
        validation_alias="BUILDKITE_GIT_DEPTH",
    )


@lru_cache
def dapatkan_pengaturan() -> PengaturanAplikasi:
    """Singleton cache agar pembacaan env konsisten dan murah."""

    return PengaturanAplikasi()
