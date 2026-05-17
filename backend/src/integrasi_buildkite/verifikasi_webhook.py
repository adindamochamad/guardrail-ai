"""Verifikasi keaslian webhook Buildkite (token polos atau HMAC-SHA256)."""

from __future__ import annotations

import hashlib
import hmac
import time


def periksa_keaslian_webhook(
    tubuh_mentah: bytes,
    header_token: str | None,
    header_tanda: str | None,
    rahasia_webhook: str,
    *,
    batas_usia_detik: int = 300,
    waktu_sekarang: float | None = None,
) -> tuple[bool, str]:
    """
    Mengembalikan (lolos, alasan_singkat).

    - `X-Buildkite-Token`: harus sama dengan rahasia (perbandingan aman).
    - `X-Buildkite-Signature`: format `timestamp=...,signature=...` dengan
      HMAC-SHA256 heksadesimal atas `{timestamp}.{tubuh_teks}` (lihat dok Buildkite).
    """

    if header_token is not None:
        if not hmac.compare_digest(header_token.strip(), rahasia_webhook.strip()):
            return False, "token_publik_tidak_cocok"
        return True, "token_ok"

    if header_tanda is None:
        return False, "tanpa_token_atau_tanda"

    pasangan = _uraikan_header_tanda(header_tanda)
    if pasangan is None:
        return False, "format_tanda_tidak_valid"
    stempel_waktu_str, tanda_terima = pasangan

    try:
        stempel_int = int(stempel_waktu_str)
    except ValueError:
        return False, "timestamp_bukan_angka"

    sekarang = int(waktu_sekarang or time.time())
    if abs(sekarang - stempel_int) > batas_usia_detik:
        return False, "timestamp_di_luar_jendela_replay"

    try:
        tubuh_teks = tubuh_mentah.decode("utf-8")
    except UnicodeDecodeError:
        return False, "tubuh_bukan_utf8"

    pesan = f"{stempel_waktu_str}.{tubuh_teks}"
    diharapkan = hmac.new(
        rahasia_webhook.encode("utf-8"),
        pesan.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(diharapkan, tanda_terima):
        return False, "hmac_tidak_cocok"

    return True, "tanda_ok"


def _uraikan_header_tanda(header: str) -> tuple[str, str] | None:
    """Memecah `timestamp=...,signature=...` menjadi tuple (timestamp, hex)."""

    bagian: dict[str, str] = {}
    for fragmen in header.split(","):
        fragmen = fragmen.strip()
        if "=" not in fragmen:
            continue
        kunci, nilai = fragmen.split("=", 1)
        bagian[kunci.strip()] = nilai.strip()

    if "timestamp" not in bagian or "signature" not in bagian:
        return None
    return bagian["timestamp"], bagian["signature"]
