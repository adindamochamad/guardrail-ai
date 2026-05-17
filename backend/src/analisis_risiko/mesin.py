"""Orkestrasi analisis risiko: regex + AST, filter konteks AI, deduplikasi."""

from __future__ import annotations

import ast
from collections.abc import Iterable

from ..ai_detector import deteksi_ai
from ..config import PengaturanAplikasi, dapatkan_pengaturan
from .cek_ast_python import jumlah_pemeriksaan_ast_bawaan, temuan_dari_ast_python
from .daftar_aturan import AturanRegex, daftar_aturan_regex_bawaan, filter_aturan_oleh_lingkup
from .tipe_data import HasilAnalisis, TemuanRisiko


def deduplikasi_temuan(temuan: list[TemuanRisiko]) -> list[TemuanRisiko]:
    """Menghindari duplikat ketat untuk kombinasi id aturan + baris."""

    dilihat: set[tuple[str, int | None]] = set()
    hasil: list[TemuanRisiko] = []
    for tunggal in temuan:
        kunci = (tunggal.id_aturan, tunggal.nomor_baris)
        if kunci in dilihat:
            continue
        dilihat.add(kunci)
        hasil.append(tunggal)
    return hasil


def terapkan_aturan_regex(
    kode: str,
    aturan_masuk: Iterable[AturanRegex],
) -> list[TemuanRisiko]:
    """Mencocokkan semua pola regex terhadap teks sumber."""

    temuan: list[TemuanRisiko] = []
    for aturan in aturan_masuk:
        for kecocokan in aturan.pola.finditer(kode):
            posisi = kecocokan.start()
            nomor_baris = kode[:posisi].count("\n") + 1
            cuplikan_teks = kecocokan.group(0)
            if len(cuplikan_teks) > 240:
                cuplikan_teks = cuplikan_teks[:240] + "…"
            temuan.append(
                TemuanRisiko(
                    id_aturan=aturan.id_aturan,
                    kategori=aturan.kategori,
                    tingkat_keparahan=aturan.tingkat_keparahan,
                    nomor_baris=nomor_baris,
                    deskripsi=aturan.deskripsi,
                    saran_perbaikan=aturan.saran_perbaikan,
                    cuplikan=cuplikan_teks,
                    dari_ast=False,
                )
            )
    return temuan


def analisis_kode(
    kode: str,
    *,
    bahasa: str = "python",
    apakah_ai: bool | None = None,
    lewati_aturan_khusus_ai_jika_bukan_ai: bool = True,
    pengaturan: PengaturanAplikasi | None = None,
) -> HasilAnalisis:
    """
    Menganalisis cuplikan untuk risiko keamanan/kualitas.

    Bila `apakah_ai` None, inferensi cepat memakai `deteksi_ai` tanpa LLM.
    """

    if not kode.strip():
        return HasilAnalisis(
            daftar_temuan=[],
            apakah_ai_inferensi=False,
            apakah_ai_efektif=False,
            bahasa=bahasa,
        )

    pengaturan_jalan = pengaturan or dapatkan_pengaturan()
    inferensi = apakah_ai is None
    if inferensi:
        ringkas_deteksi = deteksi_ai(
            kode,
            gunakan_llm=False,
            pengaturan=pengaturan_jalan,
        )
        apakah_jelas = ringkas_deteksi.apakah_ai
    else:
        apakah_jelas = bool(apakah_ai)

    aturan_semua = daftar_aturan_regex_bawaan()
    aturan_terpilih = filter_aturan_oleh_lingkup(aturan_semua, bahasa)

    aturan_dipakai: list[AturanRegex] = []
    for aturan in aturan_terpilih:
        if (
            lewati_aturan_khusus_ai_jika_bukan_ai
            and aturan.khusus_ai
            and not apakah_jelas
        ):
            continue
        aturan_dipakai.append(aturan)

    temuan_gabungan = terapkan_aturan_regex(kode, aturan_dipakai)

    bahasa_normal = bahasa.strip().lower()
    if bahasa_normal in {"python", "py"}:
        try:
            pohon = ast.parse(kode)
            temuan_gabungan.extend(temuan_dari_ast_python(pohon))
        except SyntaxError:
            # Kode tidak valid — lewati AST; regex tetap berguna.
            pass

    temuan_bersih = deduplikasi_temuan(temuan_gabungan)
    hasil = HasilAnalisis(
        daftar_temuan=temuan_bersih,
        apakah_ai_inferensi=inferensi,
        apakah_ai_efektif=apakah_jelas,
        bahasa=bahasa,
    )
    hasil.urutkan()
    return hasil


def jumlah_semua_aturan_harian() -> int:
    """Total aturan regex bawaan + pemeriksaan AST Python (untuk tes roadmap)."""

    return len(daftar_aturan_regex_bawaan()) + jumlah_pemeriksaan_ast_bawaan()


__all__ = [
    "analisis_kode",
    "deduplikasi_temuan",
    "jumlah_semua_aturan_harian",
    "HasilAnalisis",
    "TemuanRisiko",
]
