"""Tes HTTP untuk `/analyze` dan `/scan`."""


def test_analyze_ok(klien_api):
    balasan = klien_api.post(
        "/analyze",
        json={
            "kode": 'key = "AKIAIOSFODNN7EXAMPLE"\n',
            "bahasa": "python",
            "apakah_ai": True,
        },
    )
    assert balasan.status_code == 200
    isi = balasan.json()
    assert isi["jumlah_temuan"] >= 1
    assert "ringkasan_keparahan" in isi


def test_scan_menggabungkan_deteksi_dan_analisis(klien_api):
    balasan = klien_api.post(
        "/scan",
        json={
            "kode": "import os\nos.system('echo hi')\n",
            "gunakan_llm": False,
            "bahasa": "python",
        },
    )
    assert balasan.status_code == 200
    isi = balasan.json()
    assert "deteksi" in isi and "analisis" in isi
    assert "apakah_ai" in isi["deteksi"]
    assert isi["jumlah_total_aturan_sistem"] >= 40


def test_analyze_kode_kosong_ringan():
    """Kode kosong dikembalikan 422 oleh FastAPI min_length — uji mesin langsung."""

    from src.analisis_risiko import analisis_kode
    from tests.pengaturan_uji import buat_pengaturan_uji

    hasil = analisis_kode("   \n", pengaturan=buat_pengaturan_uji())
    assert hasil.jumlah_temuan == 0
