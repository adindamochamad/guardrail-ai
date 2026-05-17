"""Tipe data untuk temuan risiko dan hasil analisis aturan."""

from __future__ import annotations

from dataclasses import dataclass, field

BOBOT_KEPARAHAN: dict[str, int] = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
}


@dataclass(frozen=True)
class TemuanRisiko:
    """Satu temuan yang bisa dipetakan ke baris sumber."""

    id_aturan: str
    kategori: str
    tingkat_keparahan: str
    nomor_baris: int | None
    deskripsi: str
    saran_perbaikan: str | None
    cuplikan: str | None = None
    dari_ast: bool = False


@dataclass
class HasilAnalisis:
    """Kumpulan temuan terurut dari parah ke ringan."""

    daftar_temuan: list[TemuanRisiko] = field(default_factory=list)
    apakah_ai_inferensi: bool = False
    apakah_ai_efektif: bool = False
    bahasa: str = "python"

    def urutkan(self) -> None:
        """Menyusun ulang temuan berdasarkan tingkat keparahan lalu id aturan."""

        self.daftar_temuan.sort(
            key=lambda t: (
                -BOBOT_KEPARAHAN.get(t.tingkat_keparahan, 0),
                t.id_aturan,
                t.nomor_baris or 0,
            )
        )

    @property
    def jumlah_temuan(self) -> int:
        return len(self.daftar_temuan)

    def ringkasan_keparahan(self) -> dict[str, int]:
        """Menghitung jumlah temuan per tingkat."""

        keluaran: dict[str, int] = {}
        for temuan in self.daftar_temuan:
            keluaran[temuan.tingkat_keparahan] = keluaran.get(temuan.tingkat_keparahan, 0) + 1
        return keluaran
