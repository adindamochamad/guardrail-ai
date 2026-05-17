"""Orkestrasi sinyal deteksi AI dan agregasi bobot."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from ..config import PengaturanAplikasi, dapatkan_pengaturan
from .layanan_llm import perkiraan_skor_llm_bawaan
from .metadata_git import skor_dari_metadata_git
from .pola_kode import hitung_skor_pola


@dataclass(frozen=True)
class HasilDeteksi:
    """Keluaran tunggal deteksi — siap dipetakan ke JSON API."""

    apakah_ai: bool
    skor_keyakinan: float
    ambang_batas: float
    sinyal: dict[str, Any]


def hitung_skor_gabungan(
    skor_git: float,
    skor_pola: float,
    skor_llm: float | None,
    minta_llm: bool,
) -> float:
    """
    Menggabungkan sinyal dengan bobot dasar lalu menormalisasi agar total = 1.

    Bobot relatif: Git (jika ada skor) > LLM (jika dipakai & tersedia) > pola statis.
    """

    llm_siap = minta_llm and skor_llm is not None
    w_git = 0.45 if skor_git > 0 else 0.0
    w_llm = 0.40 if llm_siap else 0.0
    w_pola = 0.35
    total_bobot = w_git + w_llm + w_pola
    w_git_n = w_git / total_bobot
    w_llm_n = w_llm / total_bobot
    w_pola_n = w_pola / total_bobot
    kontribusi_llm = float(skor_llm) if llm_siap else 0.0
    return w_git_n * skor_git + w_llm_n * kontribusi_llm + w_pola_n * skor_pola


def deteksi_ai(
    kode: str,
    *,
    pesan_commit: str | None = None,
    gunakan_llm: bool = False,
    pengaturan: PengaturanAplikasi | None = None,
    fungsi_llm: Callable[[str], float | None] | None = None,
) -> HasilDeteksi:
    """
    Menjalankan pipeline deteksi: metadata Git, pola statis, dan LLM opsional.

    `fungsi_llm` dipakai di tes untuk stub; bila None dan `gunakan_llm`, pakai OpenAI bawaan.
    """

    pengaturan_jalan = pengaturan or dapatkan_pengaturan()
    skor_git, rincian_git = skor_dari_metadata_git(pesan_commit)
    skor_pola, rincian_pola = hitung_skor_pola(kode)

    skor_llm: float | None = None
    info_llm: dict[str, Any] = {"digunakan": False, "skor": None}

    if gunakan_llm:
        info_llm["digunakan"] = True
        if fungsi_llm is not None:
            skor_llm = fungsi_llm(kode)
        else:
            skor_llm = perkiraan_skor_llm_bawaan(kode, pengaturan_jalan)
        info_llm["skor"] = skor_llm
        if skor_llm is None:
            info_llm["alasan"] = "gagal_atau_tanpa_kunci"

    minta_llm = gunakan_llm
    skor_akhir = hitung_skor_gabungan(
        skor_git,
        skor_pola,
        skor_llm,
        minta_llm,
    )
    # Jika trailer Git eksplisit (Copilot), angkat skor minimal ke skor Git
    if skor_git >= 0.85:
        skor_akhir = max(skor_akhir, skor_git)

    skor_akhir = max(0.0, min(1.0, float(skor_akhir)))

    ambang = pengaturan_jalan.ambang_deteksi_ai

    return HasilDeteksi(
        apakah_ai=skor_akhir >= ambang,
        skor_keyakinan=round(skor_akhir, 4),
        ambang_batas=ambang,
        sinyal={
            "metadata_git": {"skor": round(skor_git, 4), **rincian_git},
            "pola": {"skor": round(skor_pola, 4), **rincian_pola},
            "llm": info_llm,
        },
    )
