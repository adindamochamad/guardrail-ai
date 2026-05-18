"""Fasad tipis: pemasangan backend observabilitas tanpa mengikat seluruh app ke satu vendor."""

from __future__ import annotations

from ..config import PengaturanAplikasi


def pasang_observabilitas_runtime(pengaturan: PengaturanAplikasi) -> None:
    """
    Menyiapkan instrumentasi runtime sekali saat startup.

    Saat ini: Sentry jika `SENTRY_DSN` terisi. Hud.io atau vendor lain bisa
    ditambah sebagai cabang di modul ini tanpa mengubah rute utama.
    """

    dsn = (pengaturan.dsn_sentry or "").strip()
    if not dsn:
        return

    # Impor malas agar jalur tanpa Sentry tetap tidak memanggil init secara tak sengaja.
    from .pelaksana_sentry import pasang_sentry

    pasang_sentry(pengaturan)


def ringkas_status_observabilitas(pengaturan: PengaturanAplikasi) -> str:
    """Label aman untuk health check (tanpa rahasia)."""

    if (pengaturan.dsn_sentry or "").strip():
        return "sentry"
    return "tidak_aktif"
