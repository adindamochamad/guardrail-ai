"""Tes agregasi dan pipeline `deteksi_ai`."""

from src.ai_detector.mesin_deteksi import deteksi_ai, hitung_skor_gabungan
from tests.pengaturan_uji import buat_pengaturan_uji


def test_gabungan_llm_memberi_bobot_skor():
    gabung = hitung_skor_gabungan(
        skor_git=0.0,
        skor_pola=0.5,
        skor_llm=1.0,
        minta_llm=True,
    )
    assert 0.65 < gabung < 0.85


def test_deteksi_copilot_mengalahkan_pola_manusia():
    kode_manusia = "def f(x):\n    return x + 1\n"
    pesan = "ok\n\nCo-authored-by: GitHub Copilot <copilot@users.noreply.github.com>"
    hasil = deteksi_ai(
        kode_manusia,
        pesan_commit=pesan,
        gunakan_llm=False,
        pengaturan=buat_pengaturan_uji(ambang_deteksi_ai=0.5),
    )
    assert hasil.apakah_ai is True
    assert hasil.skor_keyakinan >= 0.5


def test_stub_llm_terintegrasi():
    def stub_llm(_kode: str) -> float:
        return 0.95

    kode = "print('hello')\n"
    hasil = deteksi_ai(
        kode,
        gunakan_llm=True,
        pengaturan=buat_pengaturan_uji(ambang_deteksi_ai=0.5),
        fungsi_llm=stub_llm,
    )
    assert hasil.sinyal["llm"]["digunakan"] is True
    assert hasil.skor_keyakinan > 0.5
