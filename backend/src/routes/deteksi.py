"""Endpoint REST untuk deteksi kode AI."""

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..ai_detector import deteksi_ai
from ..config import dapatkan_pengaturan

router = APIRouter(tags=["deteksi"])


class PermintaanDeteksi(BaseModel):
    """Body JSON untuk meminta analisis cuplikan kode."""

    kode: str = Field(
        ...,
        min_length=1,
        max_length=500_000,
        description="Cuplikan atau berkas penuh yang akan dianalisis",
    )
    pesan_commit: str | None = Field(
        None,
        max_length=32_000,
        description="Pesan commit mentah (opsional, untuk trailer Copilot dll.)",
    )
    gunakan_llm: bool = Field(
        False,
        description="Jika true, memanggil OpenAI bila `OPENAI_API_KEY` terset",
    )


class BalasanDeteksi(BaseModel):
    """Bentuk respons terstruktur (selaras dengan `HasilDeteksi`)."""

    apakah_ai: bool
    skor_keyakinan: float
    ambang_batas: float
    sinyal: dict[str, Any]


@router.post(
    "/detect",
    response_model=BalasanDeteksi,
    summary="Deteksi kemungkinan kode hasil AI",
)
def lakukan_deteksi(badan: PermintaanDeteksi) -> BalasanDeteksi:
    """Menghitung skor gabungan dari pola, metadata Git, dan LLM opsional."""

    pengaturan_jalan = dapatkan_pengaturan()
    hasil = deteksi_ai(
        badan.kode,
        pesan_commit=badan.pesan_commit,
        gunakan_llm=badan.gunakan_llm,
        pengaturan=pengaturan_jalan,
    )
    return BalasanDeteksi(
        apakah_ai=hasil.apakah_ai,
        skor_keyakinan=hasil.skor_keyakinan,
        ambang_batas=hasil.ambang_batas,
        sinyal=hasil.sinyal,
    )
