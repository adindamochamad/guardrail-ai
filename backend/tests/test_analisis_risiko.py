"""Tes mesin analisis risiko Day 3."""

from src.analisis_risiko import analisis_kode
from src.analisis_risiko.daftar_aturan import daftar_aturan_regex_bawaan
from src.analisis_risiko.mesin import jumlah_semua_aturan_harian
from tests.pengaturan_uji import buat_pengaturan_uji


def test_jumlah_aturan_melebihi_target_roadmap():
    assert len(daftar_aturan_regex_bawaan()) >= 30
    assert jumlah_semua_aturan_harian() >= 40


def test_sql_fstring_terdeteksi_bila_ai():
    kode = 'sql = f"SELECT * FROM users WHERE id = {user_id}"\n'
    hasil = analisis_kode(
        kode,
        apakah_ai=True,
        lewati_aturan_khusus_ai_jika_bukan_ai=True,
        pengaturan=buat_pengaturan_uji(),
    )
    assert any(t.id_aturan == "GR_SEC_SQL_FMT_001" for t in hasil.daftar_temuan)


def test_aturan_khusus_ai_dilewati_bila_bukan_ai():
    kode = 'sql = f"SELECT * FROM users WHERE id = {user_id}"\n'
    hasil = analisis_kode(
        kode,
        apakah_ai=False,
        lewati_aturan_khusus_ai_jika_bukan_ai=True,
        pengaturan=buat_pengaturan_uji(),
    )
    assert not any(t.id_aturan == "GR_SEC_SQL_FMT_001" for t in hasil.daftar_temuan)


def test_eval_menghasilkan_temuan():
    hasil = analisis_kode(
        "y = eval('1+1')\n",
        apakah_ai=True,
        pengaturan=buat_pengaturan_uji(),
    )
    id_ditemukan = {t.id_aturan for t in hasil.daftar_temuan}
    assert "GR_AST_EVAL_001" in id_ditemukan or "GR_SEC_EVAL_001" in id_ditemukan
