"""Integrasi konkret: Sentry SDK untuk FastAPI / Starlette."""

from __future__ import annotations

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from ..config import PengaturanAplikasi


def pasang_sentry(pengaturan: PengaturanAplikasi) -> None:
    """Menginisialisasi klien Sentry; panggil hanya jika DSN sudah divalidasi ada."""

    dsn = (pengaturan.dsn_sentry or "").strip()
    if not dsn:
        return

    sentry_sdk.init(
        dsn=dsn,
        environment=pengaturan.lingkungan_sentry,
        send_default_pii=False,
        integrations=[
            StarletteIntegration(transaction_style="endpoint"),
            FastApiIntegration(),
        ],
        traces_sample_rate=float(pengaturan.rasio_sampel_trace_sentry),
    )
