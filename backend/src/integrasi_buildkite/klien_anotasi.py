"""Klien HTTP tipis untuk mengirim anotasi build Buildkite (REST API v2)."""

from __future__ import annotations

from typing import Any

import httpx


def kirim_anotasi_build(
    *,
    token_api: str,
    slug_organisasi: str,
    slug_pipa: str,
    nomor_build: int,
    badan_markdown: str,
    konteks: str = "guardrail-ai",
    gaya: str = "info",
    url_dasar: str = "https://api.buildkite.com",
    klien_http: httpx.Client | None = None,
) -> tuple[bool, int, str]:
    """
    Membuat anotasi pada build. Mengembalikan (berhasil, status_http, teks_ringkas).

    `gaya`: salah satu info, warning, error, success (sesuai API Buildkite).
    """

    alamat = (
        f"{url_dasar.rstrip('/')}/v2/organizations/"
        f"{slug_organisasi}/pipelines/{slug_pipa}/builds/{nomor_build}/annotations"
    )
    muatan: dict[str, Any] = {
        "body": badan_markdown,
        "context": konteks,
        "style": gaya,
    }
    headers = {
        "Authorization": f"Bearer {token_api}",
        "Content-Type": "application/json",
    }

    tutup_manual = klien_http is None
    klien = klien_http or httpx.Client(timeout=30.0)
    try:
        balasan = klien.post(alamat, headers=headers, json=muatan)
    finally:
        if tutup_manual:
            klien.close()

    if balasan.status_code in (200, 201, 202):
        return True, balasan.status_code, "anotasi_terkirim"
    return False, balasan.status_code, balasan.text[:500]
