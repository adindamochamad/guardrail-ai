"""Webhook Buildkite — verifikasi, pemindaian GuardRail, anotasi opsional."""

from __future__ import annotations

import json
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, HTTPException, Request

from ..config import PengaturanAplikasi, dapatkan_pengaturan
from ..integrasi_buildkite import jalankan_pemindaian_dari_webhook, periksa_keaslian_webhook

router = APIRouter(tags=["buildkite"])


@router.post("/webhooks/buildkite", summary="Terima event webhook pipeline Buildkite")
async def terima_webhook_buildkite(
    permintaan: Request,
    pengaturan: Annotated[PengaturanAplikasi, Depends(dapatkan_pengaturan)],
    x_buildkite_token: str | None = Header(default=None, alias="X-Buildkite-Token"),
    x_buildkite_signature: str | None = Header(default=None, alias="X-Buildkite-Signature"),
    x_buildkite_event: str | None = Header(default=None, alias="X-Buildkite-Event"),
) -> dict[str, Any]:
    """
    Memverifikasi token atau tanda HMAC, lalu menjalankan deteksi + analisis pada cuplikan.

    Tanpa `BUILDKITE_API_TOKEN` hasil tetap dihitung tetapi anotasi dilewati.
    """

    tubuh = await permintaan.body()
    rahasia = (pengaturan.token_webhook_buildkite or "").strip()

    if not rahasia:
        if not pengaturan.izinkan_webhook_tanpa_verifikasi:
            raise HTTPException(
                status_code=503,
                detail="Webhook Buildkite: set BUILDKITE_WEBHOOK_TOKEN atau "
                "BUILDKITE_WEBHOOK_ALLOW_UNVERIFIED=true hanya untuk dev.",
            )
        lolos, alasan = True, "dev_tanpa_rahasia"
    else:
        lolos, alasan = periksa_keaslian_webhook(
            tubuh,
            x_buildkite_token,
            x_buildkite_signature,
            rahasia,
        )

    if not lolos:
        raise HTTPException(status_code=401, detail=f"Webhook ditolak: {alasan}")

    try:
        muatan = json.loads(tubuh.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=400, detail="JSON tidak valid") from exc

    ringkas = jalankan_pemindaian_dari_webhook(
        muatan,
        pengaturan,
        apakah_klon_git=pengaturan.webhook_klon_git_otomatis,
        kedalaman_klon=pengaturan.kedalaman_klon_git,
    )
    ringkas["keaslian_webhook"] = alasan
    ringkas["x_buildkite_event"] = x_buildkite_event
    return ringkas
