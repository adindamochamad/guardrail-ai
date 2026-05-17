"""Tes persistensi model ORM harian (scan + berkas)."""

from src.database import pembuat_sesi
from src.models import CodeFile, Scan


def test_scan_dan_berkas_ter_simpan(klien_api):
    sesi_basis_data = pembuat_sesi()
    try:
        scan_baru = Scan(sumber="unit_test")
        sesi_basis_data.add(scan_baru)
        sesi_basis_data.flush()
        berkas_baru = CodeFile(scan_induk=scan_baru, path_berkas="demo/halo.py")
        sesi_basis_data.add(berkas_baru)
        sesi_basis_data.commit()
    finally:
        sesi_basis_data.close()

    balasan = klien_api.get("/db/ping")
    assert balasan.status_code == 200
    isi = balasan.json()
    assert isi["scans_count"] == 1
    assert isi["code_files_count"] == 1
