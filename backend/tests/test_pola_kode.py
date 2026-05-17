"""Tes skor pola statis."""

from src.ai_detector.pola_kode import hitung_skor_pola


def test_kode_kosong_nol():
    skor, rincian = hitung_skor_pola("")
    assert skor == 0.0
    assert rincian["keterangan"] == "kode_kosong"


def test_kode_banyak_polanya_naik():
    kode = '''
def process_payment_result(response):
    """Handle payment processing result payload"""
    item = response["data"]
    try:
        execute_validate_item(item)
    except Exception:
        pass
    return item
'''
    skor, rincian = hitung_skor_pola(kode)
    assert skor > 0.2
    assert len(rincian["kecocokan"]) >= 1


def test_minimal_pola_roadmap_duapuluh():
    from src.ai_detector.pola_kode import daftar_pola_bawaan

    assert len(daftar_pola_bawaan()) >= 20
