"""Endpoint analisis risiko (`/analyze`) dan gabungan (`/scan`)."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..ai_detector import deteksi_ai
from ..analisis_risiko import analisis_kode, jumlah_semua_aturan_harian
from ..analisis_risiko.tipe_data import HasilAnalisis
from ..config import dapatkan_pengaturan
from .deteksi import BalasanDeteksi, PermintaanDeteksi

router = APIRouter(tags=["analisis_risiko"])


class PermintaanAnalisis(BaseModel):
    """Permintaan pemindaian aturan statis / AST."""

    kode: str = Field(..., min_length=1, max_length=500_000)
    bahasa: str = Field(
        default="python",
        description="python | javascript | typescript | text (hanya aturan universal)",
    )
    apakah_ai: bool | None = Field(
        default=None,
        description="Jika null, inferensi cepat via deteksi AI tanpa LLM.",
    )
    lewati_aturan_khusus_ai_jika_bukan_ai: bool = Field(
        default=True,
        description="Abaikan aturan bertanda khusus_AI bila kode dianggap bukan AI.",
    )


class TemuanKeluaran(BaseModel):
    """Satu temuan untuk respons JSON."""

    id_aturan: str
    kategori: str
    tingkat_keparahan: str
    nomor_baris: int | None
    deskripsi: str
    saran_perbaikan: str | None = None
    cuplikan: str | None = None
    dari_ast: bool = False


class BalasanAnalisis(BaseModel):
    """Hasil analisis lengkap."""

    daftar_temuan: list[TemuanKeluaran]
    jumlah_temuan: int
    ringkasan_keparahan: dict[str, int]
    apakah_ai_inferensi: bool
    apakah_ai_efektif: bool
    bahasa: str


def _konversi_hasil_analisis(hasil: HasilAnalisis) -> BalasanAnalisis:
    return BalasanAnalisis(
        daftar_temuan=[
            TemuanKeluaran(
                id_aturan=t.id_aturan,
                kategori=t.kategori,
                tingkat_keparahan=t.tingkat_keparahan,
                nomor_baris=t.nomor_baris,
                deskripsi=t.deskripsi,
                saran_perbaikan=t.saran_perbaikan,
                cuplikan=t.cuplikan,
                dari_ast=t.dari_ast,
            )
            for t in hasil.daftar_temuan
        ],
        jumlah_temuan=hasil.jumlah_temuan,
        ringkasan_keparahan=hasil.ringkasan_keparahan(),
        apakah_ai_inferensi=hasil.apakah_ai_inferensi,
        apakah_ai_efektif=hasil.apakah_ai_efektif,
        bahasa=hasil.bahasa,
    )


@router.post(
    "/analyze",
    response_model=BalasanAnalisis,
    summary="Analisis risiko berbasis aturan + AST (Python)",
)
def lakukan_analisis(badan: PermintaanAnalisis) -> BalasanAnalisis:
    """Menjalankan mesin aturan GuardRail untuk cuplikan tunggal."""

    pengaturan_jalan = dapatkan_pengaturan()
    hasil = analisis_kode(
        badan.kode,
        bahasa=badan.bahasa,
        apakah_ai=badan.apakah_ai,
        lewati_aturan_khusus_ai_jika_bukan_ai=badan.lewati_aturan_khusus_ai_jika_bukan_ai,
        pengaturan=pengaturan_jalan,
    )
    return _konversi_hasil_analisis(hasil)


class PermintaanPindaian(PermintaanDeteksi):
    """Gabungan Day 3: deteksi AI + analisis risiko dalam satu permintaan."""

    bahasa: str = Field(default="python")
    apakah_ai: bool | None = Field(
        default=None,
        description=(
            "Jika null, inferensi AI mengikuti hasil deteksi "
            "(bukan menghitung ulang di analisis)."
        ),
    )
    lewati_aturan_khusus_ai_jika_bukan_ai: bool = Field(default=True)


class BalasanPindaian(BaseModel):
    """Respons gabungan untuk demo alur penuh."""

    deteksi: BalasanDeteksi
    analisis: BalasanAnalisis
    jumlah_total_aturan_sistem: int = Field(
        description="Jumlah aturan regex + AST bawaan (metadata produk).",
    )


@router.post(
    "/scan",
    response_model=BalasanPindaian,
    summary="Deteksi AI lalu analisis risiko (alur utama MVP)",
)
def lakukan_pindaian_penuh(badan: PermintaanPindaian) -> BalasanPindaian:
    """
    Menjalankan deteksi, meneruskan label AI ke analisis agar konsisten.

    Ini mengurangi dua kali inferensi berbeda saat `apakah_ai` tidak diisi.
    """

    pengaturan_jalan = dapatkan_pengaturan()
    hasil_deteksi = deteksi_ai(
        badan.kode,
        pesan_commit=badan.pesan_commit,
        gunakan_llm=badan.gunakan_llm,
        pengaturan=pengaturan_jalan,
    )
    balasan_deteksi = BalasanDeteksi(
        apakah_ai=hasil_deteksi.apakah_ai,
        skor_keyakinan=hasil_deteksi.skor_keyakinan,
        ambang_batas=hasil_deteksi.ambang_batas,
        sinyal=hasil_deteksi.sinyal,
    )
    apakai_untuk_analisis = (
        badan.apakah_ai if badan.apakah_ai is not None else hasil_deteksi.apakah_ai
    )
    hasil_analisis = analisis_kode(
        badan.kode,
        bahasa=badan.bahasa,
        apakah_ai=apakai_untuk_analisis,
        lewati_aturan_khusus_ai_jika_bukan_ai=badan.lewati_aturan_khusus_ai_jika_bukan_ai,
        pengaturan=pengaturan_jalan,
    )

    return BalasanPindaian(
        deteksi=balasan_deteksi,
        analisis=_konversi_hasil_analisis(hasil_analisis),
        jumlah_total_aturan_sistem=jumlah_semua_aturan_harian(),
    )
