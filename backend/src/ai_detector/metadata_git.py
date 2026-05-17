"""Hitung skor dari cuplikan pesan commit / trailer Git (mis. Copilot)."""

from __future__ import annotations

import re


def skor_dari_metadata_git(pesan_commit: str | None) -> tuple[float, dict]:
    """
    Mengembalikan skor 0–1 dan rincian jika ada sinyal kuat generator AI di metadata.

    Catatan: tanpa hash atau struktur commit sungguhan, ini hanya heuristik pada teks.
    """

    if not pesan_commit or not pesan_commit.strip():
        return 0.0, {"terdeteksi": False, "alasan": "pesan_kosong"}

    teks_normal = pesan_commit.lower()

    # Trailer Git umum menyebut copilot secara eksplisit
    if "co-authored-by:" in teks_normal and "copilot" in teks_normal:
        return 0.95, {
            "terdeteksi": True,
            "alasan": "copilot_co_author_trailer",
        }

    if "github copilot" in teks_normal:
        return 0.9, {"terdeteksi": True, "alasan": "copilot_nama_lengkap"}

    if re.search(r"\bcopilot\b", teks_normal):
        return 0.65, {"terdeteksi": True, "alasan": "copilot_kata_tunggal"}

    return 0.0, {"terdeteksi": False, "alasan": "tanpa_sinyal_git_jelas"}
